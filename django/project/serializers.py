from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ReadOnlyField
from rest_framework.validators import UniqueValidator

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery  # noqa
from django.utils.translation import ugettext_lazy as _

from core.utils import send_mail_wrapper
from country.models import CustomQuestion, CountryOffice
from project.utils import remove_keys
from tiip.validators import EmailEndingValidator
from user.models import UserProfile
from .models import Project, ProjectApproval, ImportRow, ProjectImportV2, Portfolio, ProblemStatement, ScalePhase, \
    ProjectPortfolioState, ReviewScore


class PartnerSerializer(serializers.Serializer):
    PARTNER_TYPE = [(0, _('Investment')),
                    (1, _('Government')),
                    (2, _('Programme')),
                    (3, _('Technology'))]

    partner_type = serializers.ChoiceField(choices=PARTNER_TYPE)
    partner_name = serializers.CharField(max_length=100)
    partner_email = serializers.EmailField(required=False)
    partner_website = serializers.URLField(required=False)


class ProjectPublishedSerializer(serializers.Serializer):
    # UNICEF Office and co
    country_office = serializers.IntegerField(min_value=1, max_value=100000, required=True)
    country = serializers.ReadOnlyField()
    regional_office = serializers.ReadOnlyField()

    # SECTION 1 General
    name = serializers.CharField(max_length=128, validators=[UniqueValidator(queryset=Project.objects.all())])
    organisation = serializers.CharField(max_length=128)
    overview = serializers.CharField(max_length=300, required=True)
    implementation_overview = serializers.CharField(max_length=1024, required=False)
    start_date = serializers.CharField(max_length=256, required=True)
    end_date = serializers.CharField(max_length=256, required=False, allow_blank=True)
    contact_name = serializers.CharField(max_length=256)
    contact_email = serializers.EmailField()

    # UNICEF SECTION
    field_office = serializers.IntegerField(required=False)
    goal_area = serializers.IntegerField()
    result_area = serializers.IntegerField(required=False)
    capability_levels = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    capability_categories = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    capability_subcategories = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)

    # NEW FIELDS
    innovation_categories = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    unicef_sector = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=1, required=True)
    regional_priorities = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    program_targets = serializers.CharField(max_length=1024, required=False)
    program_targets_achieved = serializers.CharField(max_length=1024, required=False)
    target_group_reached = serializers.IntegerField(required=False)
    current_achievements = serializers.CharField(max_length=2048, required=False)
    cpd = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    awp = serializers.CharField(max_length=500, required=False)
    wbs = serializers.ListField(
        child=serializers.CharField(max_length=30), max_length=50, min_length=0, required=False, allow_empty=True)
    total_budget = serializers.IntegerField(required=False)
    total_budget_narrative = serializers.CharField(max_length=500, required=False)
    funding_needs = serializers.CharField(max_length=500, required=False)
    partnership_needs = serializers.CharField(max_length=500, required=False)
    currency = serializers.IntegerField(required=False)
    phase = serializers.IntegerField()
    hardware = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    nontech = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    functions = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)

    website_url = serializers.URLField(required=False)
    sharepoint_url = serializers.URLField(required=False)
    eacom_url = serializers.URLField(required=False)
    mel_url = serializers.URLField(required=False)
    other_url = serializers.URLField(required=False)

    partner = PartnerSerializer(many=True, required=False, allow_empty=True)

    # SECTION 2 Implementation Overview
    platforms = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    dhis = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    health_focus_areas = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    hsc_challenges = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True, required=False)
    donors = serializers.ListField(child=serializers.IntegerField(), max_length=32, required=False)

    class Meta:
        model = Project

    def validate_country_office(self, value):
        try:
            self.co = CountryOffice.objects.get(id=value)
        except CountryOffice.DoesNotExist:
            raise serializers.ValidationError('Country office does not exist.')

        if self.instance:
            project = Project.objects.get(id=self.instance.id)
            if project.public_id and 'country_office' in project.data and \
                    project.data['country_office'] != self.initial_data['country_office']:
                raise serializers.ValidationError('Country office cannot be altered on published projects.')
        return value

    def update(self, instance, validated_data):
        validated_data['country'] = self.co.country.id
        validated_data['regional_office'] = self.co.regional_office.id if self.co.regional_office else ""
        instance.name = validated_data["name"]
        instance.data = validated_data
        instance.draft = validated_data
        instance.make_public_id(validated_data['country'])

        instance.save()

        return instance


class ProjectDraftSerializer(ProjectPublishedSerializer):
    """
    Override fields that are not required for draft project.
    """
    # SECTION 1 General Overview
    name = serializers.CharField(max_length=128)
    organisation = serializers.CharField(max_length=128, required=False)
    implementation_overview = serializers.CharField(max_length=1024, required=False)
    contact_name = serializers.CharField(max_length=256, required=False)
    contact_email = serializers.EmailField(required=False)
    start_date = serializers.CharField(max_length=256, required=False)

    # UNICEF SECTION
    goal_area = serializers.IntegerField(required=False)

    # NEW FIELDS
    overview = serializers.CharField(max_length=300, required=False)
    unicef_sector = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True)
    phase = serializers.IntegerField(required=False)

    def create(self, validated_data):
        validated_data['country'] = self.co.country.id
        validated_data['regional_office'] = self.co.regional_office.id if self.co.regional_office else ""
        return self.Meta.model(
            name=validated_data["name"],
            draft=validated_data,
        )

    def update(self, instance, validated_data):
        if not instance.public_id:
            instance.name = validated_data["name"]

        validated_data['country'] = self.co.country.id
        validated_data['regional_office'] = self.co.regional_office.id if self.co.regional_office else ""
        instance.draft = validated_data
        return instance


class ProjectGroupSerializer(serializers.ModelSerializer):
    new_team_emails = serializers.ListField(
        child=serializers.EmailField(validators=[EmailEndingValidator()]),
        max_length=64, min_length=0, allow_empty=True, required=False)
    new_viewer_emails = serializers.ListField(
        child=serializers.EmailField(validators=[EmailEndingValidator()]),
        max_length=64, min_length=0, allow_empty=True, required=False)

    class Meta:
        model = Project
        fields = ("team", "viewers", "new_team_emails", "new_viewer_emails")
        read_only_fields = ("id",)

    def perform_create(self, email):
        user = User.objects.create_user(username=email[:150], email=email)
        UserProfile.objects.create(user=user, account_type=UserProfile.IMPLEMENTER)
        return user

    def save(self, **kwargs):
        for email in self.validated_data.get('new_team_emails', []):
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = self.perform_create(email)
            self.validated_data['team'].append(user.userprofile)

        for email in self.validated_data.get('new_viewer_emails', []):
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = self.perform_create(email)
            self.validated_data['viewers'].append(user.userprofile)

        self.validated_data.pop('new_team_emails', None)
        self.validated_data.pop('new_viewer_emails', None)

        # remove duplicates
        self.validated_data['team'] = list(set(self.validated_data['team']))
        self.validated_data['viewers'] = list(set(self.validated_data['viewers']))

        return super().save(**kwargs)

    def update(self, instance, validated_data):
        self._send_notification(instance, validated_data)

        # don't allow empty team, so no orphan projects
        if 'team' in validated_data and isinstance(validated_data['team'], list):
            instance.team.set(validated_data.get('team') or instance.team.all())

        # a project however can exist without viewers
        if 'viewers' in validated_data and isinstance(validated_data['viewers'], list):
            instance.viewers.set(validated_data['viewers'])

        instance.save()

        return instance

    def _send_notification(self, instance, validated_data):
        new_team_members = [x for x in validated_data.get('team', []) if x not in instance.team.all()]
        new_viewers = [x for x in validated_data.get('viewers', []) if x not in instance.viewers.all()]

        for profile in new_team_members:
            context = {
                "user_name": profile.name,
                "project_id": instance.id,
                "project_name": instance.name,
                "role": "team member",
            }
            send_mail_wrapper(subject="You have been added to a project in the T4D & Innovation Inventory Portal",
                              email_type="new_member",
                              to=profile.user.email,
                              language=profile.language,
                              context=context)

        for profile in new_viewers:
            context = {
                "user_name": profile.name,
                "project_id": instance.id,
                "project_name": instance.name,
                "role": "viewer",
            }
            send_mail_wrapper(subject="You have been added to a project in the T4D & Innovation Inventory Portal",
                              email_type="new_member",
                              to=profile.user.email,
                              language=profile.language,
                              context=context)


class MapProjectCountrySerializer(serializers.ModelSerializer):
    country = ReadOnlyField(source='get_country_id')

    class Meta:
        model = Project
        fields = ("id", "name", "country")


class CustomAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)
    answer = serializers.ListField(
        child=serializers.CharField(max_length=512), max_length=50, min_length=0, required=True)

    def validate_question_id(self, value):
        self.context['question'] = self.context['question_queryset'].filter(id=int(value)).first()
        if not self.context['question']:
            raise ValidationError('This question_id does not exist.')
        return value

    def validate_required_answer(self, value):
        if not value:
            raise ValidationError({'answer': 'This field is required.'})

    def validate_numeric_answer(self, value):
        if value and isinstance(value[0], str) and not value[0].isnumeric():
            raise ValidationError({'answer': 'This field must be numeric.'})

    def validate_answer_length(self, value):
        if value and len(value) > 1:
            raise ValidationError({'answer': 'There must be 1 answer only.'})

    def validate(self, attrs):
        if not self.context['is_draft']:
            if self.context['question'].required:
                self.validate_required_answer(attrs['answer'])
            if self.context['question'].type != CustomQuestion.MULTI:
                self.validate_answer_length(attrs['answer'])
            if self.context['question'].type == CustomQuestion.NUMBER:
                self.validate_numeric_answer(attrs['answer'])
        return attrs


class CountryCustomAnswerListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        instance = self.context['project']
        custom_answers = {k['question_id']: k['answer'] for k in validated_data}
        instance.draft['country_custom_answers'] = custom_answers
        if not self.context['is_draft']:
            private_ids = self.context['question_queryset'].filter(private=True).values_list('id', flat=True)
            if private_ids:
                private_answers = {k: custom_answers[k] for k in custom_answers if k in private_ids}
                instance.data['country_custom_answers_private'] = private_answers
                instance.data['country_custom_answers'] = remove_keys(data_dict=custom_answers, keys=private_ids)
            else:
                instance.data['country_custom_answers'] = custom_answers
        return instance


class DonorCustomAnswerListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        instance = self.context['project']
        donor_id = self.context['donor_id']

        custom_answers = {k['question_id']: k['answer'] for k in validated_data}
        instance.draft.setdefault('donor_custom_answers', {})
        instance.draft['donor_custom_answers'].setdefault(donor_id, {})
        instance.draft['donor_custom_answers'][donor_id] = custom_answers

        if not self.context['is_draft']:
            private_ids = self.context['question_queryset'].filter(private=True).values_list('id', flat=True)
            if private_ids:
                private_answers = {k: custom_answers[k] for k in custom_answers if k in private_ids}
                instance.data.setdefault('donor_custom_answers_private', {})
                instance.data['donor_custom_answers_private'].setdefault(donor_id, {})
                instance.data['donor_custom_answers_private'][donor_id] = private_answers
                instance.data['donor_custom_answers'][donor_id] = remove_keys(data_dict=custom_answers,
                                                                              keys=private_ids)
            else:
                instance.data.setdefault('donor_custom_answers', {})
                instance.data['donor_custom_answers'].setdefault(donor_id, {})
                instance.data['donor_custom_answers'][donor_id] = custom_answers
        return instance


class CountryCustomAnswerSerializer(CustomAnswerSerializer):
    class Meta:
        list_serializer_class = CountryCustomAnswerListSerializer


class DonorCustomAnswerSerializer(CustomAnswerSerializer):
    class Meta:
        list_serializer_class = DonorCustomAnswerListSerializer


class ProjectApprovalSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project_id')
    project_name = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()
    legacy_approved_by = serializers.ReadOnlyField(source='user_id')

    class Meta:
        model = ProjectApproval
        fields = ('id', 'project_name', 'created', 'modified', 'approved',
                  'reason', 'project', 'history', 'legacy_approved_by')

    def get_project_name(self, obj):
        return obj.project.name

    def get_history(self, obj):
        return obj.history.values('history_user__userprofile', 'approved', 'reason', 'modified')


class ImportRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportRow
        fields = "__all__"


class ProjectImportV2Serializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.ReadOnlyField()
    rows = ImportRowSerializer(many=True)

    class Meta:
        model = ProjectImportV2
        fields = ('id', 'user', 'status', 'header_mapping',
                  'rows', 'country', 'country_office', 'donor', 'filename', 'sheet_name', 'draft')

    # TODO: Need Coverage
    def create(self, validated_data):  # pragma: no cover
        rows = validated_data.pop('rows')
        instance = super().create(validated_data)
        for row_data in rows[0].get('data', []):
            ImportRow.objects.create(parent=instance, data=row_data, original_data=row_data)
        return instance

    # TODO: Need Coverage
    def update(self, instance, validated_data):  # pragma: no cover
        rows = validated_data.pop('rows', [])
        instance = super().update(instance, validated_data)
        for row in rows:
            ImportRow.objects.get(id=row['id']).update(data=row.get('data'))
        return instance


class PortfolioListSerializer(serializers.ModelSerializer):
    project_count = serializers.SerializerMethodField()
    managers = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = ('id', 'name', 'description', 'icon', 'project_count', 'managers', 'status')

    @staticmethod
    def get_project_count(obj):
        return len(Project.objects.published_only().filter(is_active=True, review_states__in=obj.review_states.all()))

    @staticmethod
    def get_managers(obj):
        return obj.managers.all().values_list('id', flat=True)


class ProblemStatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemStatement
        fields = ('id', 'name', 'description')


class ProblemStatementUpdateSerializer(ProblemStatementSerializer):

    class Meta(ProblemStatementSerializer.Meta):
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }


class ScalePhaseBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScalePhase
        fields = ('pk', 'scale')  # This is to show in ProjectPortfolioState


class ProjectPortfolioStateSerializer(serializers.ModelSerializer):
    scale_phase = ScalePhaseBriefSerializer()

    class Meta:
        model = ProjectPortfolioState
        fields = ('id', 'impact', 'scale_phase', 'portfolio', 'project', 'review_scores')


class ProjectPortfolioStateFillSerializer(serializers.ModelSerializer):
    scale_phase = serializers.IntegerField(required=True, source='get_scale')
    impact = serializers.IntegerField(required=True)
    project = serializers.UUIDField(read_only=True)
    portfolio = serializers.UUIDField(read_only=True)

    class Meta:
        model = ProjectPortfolioState
        fields = ('__all__')

    def update(self, instance, validated_data):
        """
        Override serializer to set 'complete' to True (also set scale phase based on input int
        """
        scale_phase_value = validated_data.pop('get_scale')
        instance.complete = True
        instance.scale_phase = ScalePhase.objects.get(scale=scale_phase_value)
        instance = super().update(instance, validated_data)
        return instance


class PortfolioBaseSerializer(serializers.ModelSerializer):
    problem_statements = ProblemStatementSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Portfolio
        fields = ('id', 'name', 'description', 'icon', 'status', 'managers', 'problem_statements')


class PortfolioDetailsSerializer(PortfolioBaseSerializer):
    problem_statements = ProblemStatementSerializer(many=True, required=False, read_only=True)
    review_states = ProjectPortfolioStateSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Portfolio
        fields = ('id', 'name', 'description', 'icon', 'status', 'managers', 'problem_statements',
                  'review_states')


class PortfolioCreateSerializer(PortfolioBaseSerializer):
    problem_statements = ProblemStatementSerializer(many=True, required=False)

    class Meta:
        model = Portfolio
        fields = ('id', 'name', 'description', 'icon', 'status', 'managers', 'problem_statements')

    @staticmethod
    def _create_problem_statements(instance, problem_statements):
        for ps in problem_statements:
            ProblemStatement.objects.create(name=ps['name'], description=ps['description'], portfolio=instance)

    def create(self, validated_data):
        """
        Creates new portfolio - needs explicit serializer due to nested fields
        """
        problem_statements = validated_data.pop('problem_statements')
        instance = super().create(validated_data)

        self._create_problem_statements(instance, problem_statements)
        instance.save()
        return instance


class PortfolioUpdateSerializer(PortfolioBaseSerializer):
    """
    Used for update ONLY
    """
    problem_statements = ProblemStatementUpdateSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        """
        Override serializer due to nested Problem Statements
        """

        if 'problem_statements' in validated_data:  # this is to support PATCH update
            ps_data = validated_data.pop('problem_statements')
            instance = super().update(instance, validated_data)
            # Handle delete
            update_ids = {ps['id'] for ps in ps_data if 'id' in ps}
            existing_pss = instance.problem_statements.all()

            for ps_exist in existing_pss:
                if ps_exist.id not in update_ids:  # Delete problem statements not in update data
                    ps_exist.delete()
            for ps in ps_data:
                ps['portfolio_id'] = instance.id
                ProblemStatement.objects.update_or_create(
                    id=ps['id'] if 'id' in ps else None,
                    defaults=ps
                )
        else:
            instance = super().update(instance, validated_data)
        return instance


class ProjectInPortfolioSerializer(serializers.ModelSerializer):
    review_states = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'review_states')

    def get_review_states(self, obj):
        portfolio = self.context.get('kwargs').get('pk')
        try:
            pps = obj.review_states.get(portfolio=portfolio)
            return ProjectPortfolioStateSerializer(pps).data
        except ProjectPortfolioState.DoesNotExist:
            return None


class ReviewScoreBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewScore
        fields = ('id', 'created', 'modified', 'reviewer', 'portfolio_review')


class ReviewScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewScore
        fields = '__all__'


class ReviewScoreFillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewScore
        fields = ('psa', 'psa_comment', 'rnci', 'rnci_comment', 'ratp', 'ratp_comment', 'ra', 'ra_comment', 'ee',
                  'ee_comment', 'nst', 'nst_comment', 'nc', 'nc_comment', 'ps', 'ps_comment')

    def update(self, instance, validated_data):
        """
        Override serializer to set 'complete' to True
        """
        instance.complete = True
        instance = super().update(instance, validated_data)
        return instance
