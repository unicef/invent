import uuid
from collections import namedtuple
from typing import List, Union

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from django.conf import settings

from core.models import ExtendedModel, ExtendedNameOrderedSoftDeletedModel, ActiveQuerySet, SoftDeleteModel, \
    ParentByIDMixin
from country.models import Country, Donor, CountryOffice
from project.cache import InvalidateCacheMixin
from project.utils import remove_keys
from toolkit.toolkit_data import toolkit_default
from user.models import UserProfile
from django.db.models import Count, Case, When, IntegerField, F, Q


class ProjectManager(models.Manager):
    use_in_migrations = True

    def owner_of(self, user):
        return self.filter(team=user.userprofile)

    def viewer_of(self, user):
        return self.filter(viewers=user.userprofile)

    def member_of(self, user):
        return self.filter(Q(team=user.userprofile)
                           | Q(viewers=user.userprofile)).distinct().order_by('id')

    def favorited_by(self, user):
        return self.filter(favorited_by=user.userprofile)

    # WARNING: this method is used in migration project.0016_auto_20160601_0928
    def by_organisation(self, organisation_id):  # pragma: no cover
        return self.filter(data__organisation=organisation_id)

    def published_only(self):
        return self.exclude(public_id='')

    def draft_only(self):
        return self.filter(public_id='')


class ProjectQuerySet(ActiveQuerySet, ProjectManager):
    pass


class Project(SoftDeleteModel, ExtendedModel):
    FIELDS_FOR_MEMBERS_ONLY = ("country_custom_answers_private",
                               "last_version", "last_version_date", "start_date", "end_date")
    FIELDS_FOR_LOGGED_IN = ("contact_email", "contact_name")

    name = models.CharField(max_length=255)
    data = JSONField(default=dict)
    draft = JSONField(default=dict)
    team = models.ManyToManyField(UserProfile, related_name="team", blank=True)
    viewers = models.ManyToManyField(UserProfile, related_name="viewers", blank=True)
    public_id = models.CharField(
        max_length=64, default="", help_text="<CountryCode>-<uuid>-x-<ProjectID> eg: HU9fa42491x1")
    odk_etag = models.CharField(null=True, blank=True, max_length=64)
    odk_id = models.CharField(null=True, blank=True, max_length=64)
    odk_extra_data = JSONField(default=dict)

    projects = ProjectManager  # deprecated, use objects instead
    objects = ProjectQuerySet.as_manager()
    # added here to avoid circular imports
    favorited_by = models.ManyToManyField(UserProfile, related_name='favorite_projects', blank=True)

    def __str__(self):  # pragma: no cover
        return self.name

    def get_country_id(self, draft_mode=False):
        return self.draft.get('country') if draft_mode else self.data.get('country')

    def get_country(self, draft_mode=False):
        country_id = self.get_country_id(draft_mode)
        return Country.objects.get(id=int(country_id)) if country_id else None

    def is_member(self, user):
        return self.team.filter(id=user.userprofile.id).exists() or self.viewers.filter(id=user.userprofile.id).exists()

    def is_country_user_or_admin(self, user):
        return self.get_country().user_in_groups(user.userprofile) if self.get_country() else False

    def get_member_data(self):
        return self.data

    def get_member_draft(self):
        return self.draft

    def get_non_member_data(self):
        return remove_keys(data_dict=self.data, keys=self.FIELDS_FOR_MEMBERS_ONLY)

    def get_anon_data(self):
        return remove_keys(data_dict=self.data, keys=self.FIELDS_FOR_MEMBERS_ONLY + self.FIELDS_FOR_LOGGED_IN)

    def to_representation(self, data=None, draft_mode=False):
        if data is None:
            data = self.get_member_draft() if draft_mode else self.get_member_data()

        if not data:
            return {}

        extra_data = dict(
            id=self.pk,
            name=self.draft.get('name', '') if draft_mode else self.name,
            approved=self.approval.approved if hasattr(self, 'approval') else None,
            modified=self.modified,
        )

        data.update(extra_data)

        if not draft_mode:
            last_version = CoverageVersion.objects.filter(project_id=self.pk).order_by("-version").first()
            if last_version:
                data.update(last_version=last_version.version, last_version_date=last_version.modified)

        return data

    def to_response_dict(self, published, draft):
        return dict(id=self.pk, public_id=self.public_id, published=published, draft=draft)

    def make_public_id(self, country_id):
        if self.public_id:
            return

        project_country = Country.objects.filter(id=country_id).first()
        if project_country:
            self.public_id = project_country.code + str(uuid.uuid1()).split('-')[0]

    def approve(self):
        self.approval.approved = True
        self.approval.save()

    def disapprove(self):
        self.approval.approved = False
        self.approval.save()

    def reset_approval(self):
        if self.approval.approved is not None:
            self.approval.user = None
            self.approval.approved = None
            self.approval.reason = "Project has been republished"
            self.approval.save()

    @classmethod
    def remove_stale_donors(cls):
        from country.models import Donor

        stale_ids = []
        donor_ids = set(Donor.objects.values_list('id', flat=True))

        for p in Project.objects.all():
            if p.data and 'donors' in p.data:
                published_donors = set(p.data.get('donors', []))
                stale_ids.extend(list(published_donors - donor_ids))
                p.data['donors'] = list(published_donors & donor_ids)
            if p.draft and 'donors' in p.draft:
                draft_donors = set(p.draft.get('donors', []))
                stale_ids.extend(list(draft_donors - donor_ids))
                p.draft['donors'] = list(draft_donors & donor_ids)
            p.save()
        return stale_ids

    def unpublish(self):
        self.public_id = ''
        self.data = {}
        self.save()
        self.search.reset()


@receiver(post_save, sender=Project)
def on_create_init(sender, instance, created, **kwargs):
    if created:
        from toolkit.models import Toolkit
        Toolkit.objects.get_or_create(project_id=instance.id, defaults=dict(data=toolkit_default))
        ProjectApproval.objects.get_or_create(project_id=instance.id)


class PortfolioManager(models.Manager):
    use_in_migrations = True

    def is_manager(self, user: User):
        if user.userprofile.global_portfolio_owner:  # global portfolio owners have full rights
            return self.all()
        return self.filter(managers=user.userprofile)  # otherwise we filter for managed portfolios


class PortfolioQuerySet(ActiveQuerySet, PortfolioManager):
    pass


class Portfolio(ExtendedNameOrderedSoftDeletedModel):
    description = models.CharField(max_length=1000)
    icon = models.CharField(max_length=3, blank=True)
    managers = models.ManyToManyField(UserProfile, related_name="portfolios", blank=True)
    STATUS_DRAFT = 'DR'
    STATUS_ACTIVE = 'ACT'
    STATUS_ARCHIVED = 'ARC'
    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_ACTIVE, _('Active')),
        (STATUS_ARCHIVED, _('Archived'))
    )

    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )
    objects = PortfolioQuerySet.as_manager()

    def get_ambition_matrix(self, project_ids: Union[List[int], None] = None):
        """
        Returns with a list of coordinates and assigned project ids for the risk impact matrix
        """
        filtered_reviews = self.review_states.filter(approved=True)
        if project_ids:
            filtered_reviews = filtered_reviews.filter(project_id__in=project_ids)
        if not filtered_reviews:
            return None  # pragma: no cover

        blobs = {}
        for review in filtered_reviews:
            hash = review.get_ambition_hash()

            if hash:
                if hash not in blobs:
                    blobs[hash] = {'x': review.nst, 'y': review.nc, 'projects': [review.project_id]}
                else:
                    blobs[hash]['projects'].append(review.project_id)
        # generate blob ratio
        blob_list = list(blobs.values())
        max_blob_size = max([len(x['projects']) for x in blob_list])
        for blob in blob_list:
            blob['ratio'] = round(len(blob['projects']) / max_blob_size, 2)
            blob['projects'].sort()
        return blob_list

    def get_risk_impact_matrix(self, project_ids: Union[List[int], None] = None):
        """
        Returns with a list of coordinates and assigned project ids for the risk-impact matrix
        """
        filtered_reviews = self.review_states.filter(approved=True)
        if project_ids:
            filtered_reviews = filtered_reviews.filter(project_id__in=project_ids)
        if not filtered_reviews:
            return None  # pragma: no cover

        blobs = {}
        for review in filtered_reviews:
            hash = review.get_impact_hash()
            if hash:
                if hash not in blobs:
                    blobs[hash] = {'x': review.impact, 'y': review.ra, 'projects': [review.project_id]}
                else:
                    blobs[hash]['projects'].append(review.project_id)
        # generate blob ratio
        blob_list = list(blobs.values())
        max_blob_size = max([len(x['projects']) for x in blob_list])
        for blob in blob_list:
            blob['ratio'] = round(len(blob['projects']) / max_blob_size, 2)
            blob['projects'].sort()
        return blob_list

    def get_problem_statement_matrix(self):
        tresholds = settings.PORTFOLIO_PROBLEMSTATEMENT_TRESHOLDS

        neglected_filter = Q(num_projects__lt=tresholds['MODERATE'])
        moderate_filter = Q(num_projects__gte=tresholds['MODERATE'], num_projects__lt=tresholds['HIGH'])
        high_filter = Q(num_projects__gte=tresholds['HIGH'])

        when_statement = dict(
            projectportfoliostate__approved=True,
            then=F('projectportfoliostate__id'))

        base_qs = self.problem_statements.annotate(num_projects=Count(Case(When(**when_statement),
                                                   output_field=IntegerField()), distinct=True))

        neglected_qs = base_qs.filter(neglected_filter)
        moderate_qs = base_qs.filter(moderate_filter)
        high_qs = base_qs.filter(high_filter)

        return {
            'neglected': list(neglected_qs.values_list('pk', flat=True)),
            'moderate': list(moderate_qs.values_list('pk', flat=True)),
            'high_activity': list(high_qs.values_list('pk', flat=True)),
        }


class ProblemStatement(ExtendedNameOrderedSoftDeletedModel):
    description = models.CharField(max_length=1024)
    portfolio = models.ForeignKey(Portfolio, blank=False, null=False, on_delete=models.CASCADE,
                                  related_name='problem_statements')

    # This is a workaround for some strange issue regarding ActiveQuerySet
    class Meta:
        default_manager_name = 'objects'
        ordering = ['name']


class ProjectApproval(ExtendedModel):
    project = models.OneToOneField('Project', related_name='approval', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, blank=True, null=True,
                             help_text="Administrator who approved the project", on_delete=models.CASCADE)
    approved = models.NullBooleanField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    history = HistoricalRecords(excluded_fields=['project', 'created'])

    def __str__(self):
        return "Approval for {}".format(self.project.name)


class CoverageVersion(ExtendedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    version = models.IntegerField()
    data = JSONField()


class File(ExtendedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    data = models.BinaryField()


class DigitalStrategy(ParentByIDMixin, InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    GROUP_CHOICES = (
        ('Client', _('Client')),
        ('Provider', _('Provider')),
        ('System', _('System')),
        ('Data service', _('Data service'))
    )
    group = models.CharField(max_length=255, choices=GROUP_CHOICES)
    parent = models.ForeignKey('DigitalStrategy', related_name='strategies',
                               blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        parent = ' [{}]'.format(self.parent.name) if self.parent else ''
        return '[{}]{} {}'.format(self.group, parent, self.name)

    class Meta:
        verbose_name = 'WHO Digital Health Intervention (DHI)'
        verbose_name_plural = 'WHO Digital Health Interventions (=UNICEF Health Capability Categories)'
        ordering = ['group', 'name']


class HSCGroup(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    class Meta:
        verbose_name = 'WHO Health System Challenge Group'
        ordering = ['name']


class HSCChallengeQuerySet(ActiveQuerySet):
    FakeChallenge = namedtuple('FakeChallenge', ['name', 'challenge'])


class HSCChallenge(ParentByIDMixin, InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    group = models.ForeignKey(HSCGroup, on_delete=models.CASCADE, related_name='challenges')

    def __str__(self):
        return '({}) {}'.format(self.group.name, self.name)

    class Meta:
        verbose_name = 'WHO Health System Challenge'
        verbose_name_plural = 'WHO Health System Challenges'
        ordering = ['group', 'name']

    objects = HSCChallengeQuerySet.as_manager()


class HealthCategory(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name = 'WHO Health Category'
        verbose_name_plural = 'WHO Health Categories'


class HealthFocusArea(ParentByIDMixin, InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    health_category = models.ForeignKey(HealthCategory, related_name='health_focus_areas', on_delete=models.CASCADE)

    def __str__(self):
        return '[{}] {}'.format(self.health_category.name, self.name)

    class Meta:
        verbose_name = 'WHO Health Focus Area'
        verbose_name_plural = 'WHO Health Focus Areas'
        ordering = ['health_category__name', 'name']


class ApprovalState(models.Model):
    APPROVED = 1
    PENDING = 2
    DECLINED = 3

    STATES = (
        (APPROVED, _("Approved")),
        (PENDING, _("Pending")),
        (DECLINED, _("Declined")),
    )

    state = models.IntegerField(choices=STATES, default=APPROVED)
    added_by = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__important_fields = ['state']
        for field in self.__important_fields:
            setattr(self, '__original_%s' % field, getattr(self, field))


class TechnologyPlatform(InvalidateCacheMixin, ApprovalState, ExtendedNameOrderedSoftDeletedModel):
    class Meta:
        verbose_name = 'Software'
        verbose_name_plural = 'Software'


class HardwarePlatform(InvalidateCacheMixin, ApprovalState, ExtendedNameOrderedSoftDeletedModel):
    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'Hardware Platform(s) and Physical Product(s)'


class NontechPlatform(InvalidateCacheMixin, ApprovalState, ExtendedNameOrderedSoftDeletedModel):
    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'Programme Innovation(s) and Non-Technology Platform(s)'


class PlatformFunction(InvalidateCacheMixin, ApprovalState, ExtendedNameOrderedSoftDeletedModel):
    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'Function(s) of Platform'


@receiver(post_save, sender=PlatformFunction)
@receiver(post_save, sender=NontechPlatform)
@receiver(post_save, sender=HardwarePlatform)
@receiver(post_save, sender=TechnologyPlatform)
def process_approval_states(sender, instance, created, **kwargs):
    if not created and instance.__original_state != instance.state:
        from project.tasks import notify_user_about_approval

        if sender == TechnologyPlatform:
            data_key = 'platforms'
        elif sender == HardwarePlatform:  # pragma: no cover
            data_key = 'hardware'
        elif sender == NontechPlatform:  # pragma: no cover
            data_key = 'nontech'
        elif sender == PlatformFunction:  # pragma: no cover
            data_key = 'functions'
        else:  # pragma: no cover
            return

        if instance.state == ApprovalState.DECLINED:
            projects = Project.objects.filter(Q(**{f"data__{data_key}__contains": [instance.id]}) |
                                              Q(**{f"draft__{data_key}__contains": [instance.id]}))

            for project in projects:
                if project.public_id and data_key in project.data:
                    project.data[data_key] = \
                        [item for item in project.data[data_key] if item != instance.id]
                if data_key in project.draft:
                    project.draft[data_key] = \
                        [item for item in project.draft[data_key] if item != instance.id]
                project.save(update_fields=['data', 'draft'])

            notify_user_about_approval.apply_async(args=('decline', instance._meta.model_name, instance.pk,))
        elif instance.state == ApprovalState.APPROVED:
            notify_user_about_approval.apply_async(args=('approve', instance._meta.model_name, instance.pk,))


class UNICEFResultArea(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    goal_area = models.ForeignKey('UNICEFGoal', related_name='result_areas', on_delete=models.CASCADE)

    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'UNICEF Result Areas'

    def __str__(self):  # pragma: no cover
        return '[{}] {}'.format(self.goal_area.name, self.name)


class UNICEFCapabilityLevel(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    goal_area = models.ForeignKey('UNICEFGoal', related_name='capability_levels', on_delete=models.CASCADE)

    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'UNICEF Capability Levels'

    def __str__(self):  # pragma: no cover
        return '[{} - {}] {}'.format(self.goal_area.name, self.goal_area.capability_level_question, self.name)


class UNICEFCapabilityCategory(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    goal_area = models.ForeignKey('UNICEFGoal', related_name='capability_categories', on_delete=models.CASCADE)

    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'UNICEF Capability Categories'

    def __str__(self):  # pragma: no cover
        return '[{} - {}] {}'.format(self.goal_area.name, self.goal_area.capability_category_question, self.name)


class UNICEFCapabilitySubCategory(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    goal_area = models.ForeignKey('UNICEFGoal', related_name='capability_subcategories', on_delete=models.CASCADE)

    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'UNICEF Capability Sub Categories'

    def __str__(self):  # pragma: no cover
        return '[{} - {}] {}'.format(self.goal_area.name, self.goal_area.capability_subcategory_question, self.name)


class UNICEFGoal(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    capability_level_question = models.CharField(max_length=512)
    capability_category_question = models.CharField(max_length=512)
    capability_subcategory_question = models.CharField(max_length=512)

    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'UNICEF Goal Areas'

    def __str__(self):  # pragma: no cover
        return '{}'.format(self.name)


class UNICEFSector(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'UNICEF Sectors'


class RegionalPriority(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    region = models.IntegerField(choices=Country.UNICEF_REGIONS, null=True, blank=True)

    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'Regional Priorities'


class InnovationCategory(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'Innovation Categories'


class InnovationWay(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'Innovation Ways'


class CPD(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'CPD and annual work plan'


class ISC(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    class Meta(ExtendedNameOrderedSoftDeletedModel.Meta):
        verbose_name_plural = 'Information Security Classification'


class ProjectImport(ExtendedModel):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    csv = models.FileField()
    headers = ArrayField(models.CharField(max_length=512), blank=True, null=True)
    mapping = JSONField(default=dict)
    imported = models.TextField(null=True, blank=True, default='')
    failed = models.TextField(null=True, blank=True, default='')
    status = models.NullBooleanField(null=True, blank=True)

    def __str__(self):  # pragma: no cover
        return self.csv.name


class ProjectImportV2(ExtendedModel):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.NullBooleanField(null=True, blank=True)  # TODO: maybe remove this
    header_mapping = JSONField(default=dict, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    country_office = models.ForeignKey(CountryOffice, null=True, blank=True, on_delete=models.SET_NULL)
    donor = models.ForeignKey(Donor, null=True, blank=True, on_delete=models.SET_NULL)
    filename = models.CharField(max_length=256, null=True, blank=True)
    sheet_name = models.CharField(max_length=256, null=True, blank=True)
    draft = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'filename', 'sheet_name')

    def __str__(self):  # pragma: no cover
        return self.filename if self.filename else self.pk


class ImportRow(models.Model):
    data = JSONField(default=dict)
    original_data = JSONField(default=dict)
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey(ProjectImportV2, null=True, related_name="rows", on_delete=models.SET_NULL)


class BaseScore(ExtendedModel):
    BASE_CHOICES = [(i, i) for i in range(1, 6)]
    psa = models.ManyToManyField(ProblemStatement, blank=True)  # Problem Statement Alignment
    rnci = models.IntegerField(choices=BASE_CHOICES, null=True, blank=True)  # Reach: Number of Children Impacted
    ratp = models.IntegerField(choices=BASE_CHOICES, null=True, blank=True)  # Reach: Addressing Target Populations
    ra = models.IntegerField(choices=BASE_CHOICES, null=True, blank=True)  # Risk Assessment
    ee = models.IntegerField(choices=BASE_CHOICES, null=True, blank=True)  # Evidence of Effectiveness
    nst = models.IntegerField(choices=BASE_CHOICES, null=True, blank=True)  # Newness of Solution (Tool)
    nc = models.IntegerField(choices=BASE_CHOICES, null=True, blank=True)  # Newness of Challenge
    ps = models.IntegerField(choices=BASE_CHOICES, null=True, blank=True)  # Path to Scale

    class Meta:
        abstract = True


class ProjectPortfolioState(BaseScore):
    SCALE_CHOICES = (
        (1, _('1 - Ideation')),
        (2, _('2 - Research & Development')),
        (3, _('3 - Proof of Concept')),
        (4, _('4 - Transition to Scale')),
        (5, _('5 - Scaling')),
        (6, _('6 - Sustainable Scale'))
    )

    impact = models.IntegerField(choices=BaseScore.BASE_CHOICES, null=True, blank=True)
    scale_phase = models.IntegerField(choices=SCALE_CHOICES, null=True, blank=True)
    portfolio = models.ForeignKey(Portfolio, related_name='review_states', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='review_states', on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('portfolio', 'project')

    def __str__(self):  # pragma: no cover
        return f"{self.portfolio}: {self.project}"

    def assign_questionnaire(self, user: UserProfile):
        return ReviewScore.objects.get_or_create(reviewer=user, portfolio_review=self)

    def get_impact_hash(self):
        return f'{self.impact}-{self.ra}' if self.reviewed else None

    def get_ambition_hash(self):
        return f'{self.nst}-{self.nc}' if self.reviewed else None


class ReviewScore(BaseScore):
    reviewer = models.ForeignKey(UserProfile, related_name='review_scores', on_delete=models.CASCADE)
    portfolio_review = models.ForeignKey(ProjectPortfolioState, related_name='review_scores', on_delete=models.CASCADE)
    psa_comment = models.CharField(max_length=255, null=True, blank=True)  # PSA - reviewer's comment field
    rnci_comment = models.CharField(max_length=255, null=True, blank=True)  # RNCI - reviewer's comment field
    ratp_comment = models.CharField(max_length=255, null=True, blank=True)  # RATP - reviewer's comment field
    ra_comment = models.CharField(max_length=255, null=True, blank=True)  # Risk Assessment - reviewer's comment field
    ee_comment = models.CharField(max_length=255, null=True, blank=True)  # EE - reviewer's comment field
    nst_comment = models.CharField(max_length=255, null=True, blank=True)  # NST - reviewer's comment field
    nc_comment = models.CharField(max_length=255, null=True, blank=True)  # NC - reviewer's comment field
    ps_comment = models.CharField(max_length=255, null=True, blank=True)  # PS - reviewer's comment field

    complete = models.BooleanField(default=False)

    def __str__(self):  # pragma: no cover
        return f'{self.reviewer} - {self.portfolio_review.project} - {self.portfolio_review.portfolio}'

    class Meta:
        unique_together = ('reviewer', 'portfolio_review')

    def get_project_data(self):
        return self.portfolio_review.project.to_representation()

    def get_portfolio(self):
        return self.portfolio_review.portfolio


class Stage(InvalidateCacheMixin, ExtendedNameOrderedSoftDeletedModel):
    name = models.CharField(max_length=128)
    order = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    tooltip = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Phase of initiative'
        verbose_name_plural = 'Phases of initiative'

    def __str__(self):  # pragma: no cover
        return self.name
