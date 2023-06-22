import copy
from collections import OrderedDict
from datetime import date

from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.viewsets import ViewSet, GenericViewSet

from country.models import Donor, CountryOffice, RegionalOffice, Currency
from core.views import TokenAuthMixin, TeamTokenAuthMixin, get_object_or_400, get_object_or_404, GPOAccessMixin, PortfolioAccessMixin, \
    ReviewScoreReviewerAccessMixin, ReviewScoreAccessMixin, ProjectPortfolioStateAccessMixin, SolutionAccessMixin
from project.cache import cache_structure
from project.models import HSCGroup, ProjectApproval, ProjectImportV2, ImportRow, UNICEFGoal, UNICEFResultArea, \
    UNICEFCapabilityLevel, UNICEFCapabilityCategory, UNICEFCapabilitySubCategory, UNICEFSector, RegionalPriority, \
    HardwarePlatform, NontechPlatform, PlatformFunction, CPD, InnovationCategory, InnovationWay, ISC, \
    ApprovalState, Stage, Phase,  ProjectVersion, ProblemStatement, Solution
from project.permissions import InCountryAdminForApproval
from search.views import ResultsSetPagination
from .models import Project, TechnologyPlatform, DigitalStrategy, CountrySolution, \
    HealthCategory, HSCChallenge, Portfolio, ProjectPortfolioState, ReviewScore
from user.models import UserProfile
from .resources import ProjectResource
from .serializers import ProjectDraftSerializer, ProjectGroupSerializer, ProjectPublishedSerializer, \
    MapProjectCountrySerializer, CountryCustomAnswerSerializer, DonorCustomAnswerSerializer, \
    ProjectApprovalSerializer, ProjectImportV2Serializer, ImportRowSerializer, PortfolioListSerializer, \
    ReviewScoreSerializer, ReviewScoreFillSerializer, ReviewScoreBriefSerializer, \
    ProjectPortfolioStateManagerSerializer, PortfolioSerializer, \
    PortfolioStateChangeSerializer, ReviewScoreDetailedSerializer, TechnologyPlatformCreateSerializer, \
    HardwarePlatformCreateSerializer, NontechPlatformCreateSerializer, PlatformFunctionCreateSerializer, \
    ProjectCardSerializer, ProjectImageUploadSerializer, ProblemStatementSerializer, SolutionSerializer, \
    ProjectVersionHistorySerializer
from user.serializers import UserProfileSerializer
from .tasks import notify_superusers_about_new_pending_approval


class ProjectPublicViewSet(ViewSet):

    def project_structure(self, request):
        """
        Terminology and taxonomy endpoint - List all the available taxonomies and terminologies

        Reponse:  
        `technology_platforms` = WHO's Software list  
        `goal_areas`  
        `result_areas`  
        `capability_levels`  
        `capability_categories`  
        `capability_subcategories`  
        `health_focus_areas` = WHO's Health Focus Areas  
        `hsc_challenges` = WHO's Health System Challanges  
        `strategies` = WHO's Digital Health Interventions  
        `regional_offices`  
        `currencies`  
        `sectors` = UNICEF Sectors  
        `regional_priorities` = Regional Priorities  
        `hardware` = Hardware Platform(s) and Physical Product(s)  
        `nontech` = Programme Innovation(s) and Non-Technology Platform(s)  
        `functions` = Function(s) of Platform  
        `cpd` = CPD and annual work plan  
        `innovation_categories` = Innovation Categories  
        `innovation_ways` = Innovation ways  
        `isc` = Information Security Classification  
        `phases` = [DEPRECATED] Phase of Initiative  
        `stages` = [New] Phases of initiative  
        `phases_stages` = [New] Mapping Phases and Stages of initiative  

        """

        return Response(self._get_project_structure())

    @cache_structure
    def _get_project_structure(self):

        # create a mapping for phases and stages
        mapping = {
            1: {'phase_name': 'Opportunity and Ideation', 'stage_no': 1, 'stage_name': 'Initiation'},
            2: {'phase_name': 'Preparation and Scoping', 'stage_no': 1, 'stage_name': 'Initiation'},
            3: {'phase_name': 'Analysis and Design', 'stage_no': 2, 'stage_name': 'Analysis and Design'},
            4: {'phase_name': 'Implementation Planning', 'stage_no': 2, 'stage_name': 'Analysis and Design'},
            5: {'phase_name': 'Developing or Adapting Solution', 'stage_no': 3, 'stage_name': 'Develop and Pilot'},
            6: {'phase_name': 'Piloting and Evidence Generation', 'stage_no': 3, 'stage_name': 'Develop and Pilot'},
            7: {'phase_name': 'Package and Advocacy', 'stage_no': 4, 'stage_name': 'Package and Deploy'},
            8: {'phase_name': 'Deploying', 'stage_no': 4, 'stage_name': 'Package and Deploy'},
            9: {'phase_name': 'Scaling Up', 'stage_no': 4, 'stage_name': 'Package and Deploy'},
            10: {'phase_name': 'Handover or Complete', 'stage_no': 5, 'stage_name': 'Completion'},
            11: {'phase_name': 'Discontinued', 'stage_no': 5, 'stage_name': 'Completion'}
        }

        strategies = []
        for group, group_name in DigitalStrategy.GROUP_CHOICES:
            sub_groups = []
            for parent in DigitalStrategy.objects.filter(group=group, parent=None).all():
                sub_groups.append(dict(
                    id=parent.id,
                    name=parent.name,
                    strategies=parent.strategies.filter(
                        is_active=True).values('id', 'name')
                ))
            strategies.append(dict(
                name=group_name,
                subGroups=sub_groups
            ))

        health_focus_areas = []
        for category in HealthCategory.objects.all():
            health_focus_areas.append(dict(
                id=category.id,
                name=category.name,
                health_focus_areas=category.health_focus_areas.filter(
                    is_active=True).values('id', 'name')
            ))

        hsc_challenges = []
        for group in HSCGroup.objects.values('id', 'name'):
            hsc_challenges.append(dict(
                name=group['name'],
                challenges=[{'id': c['id'], 'challenge': c['name']}
                            for c in HSCChallenge.objects.filter(group__id=group['id']).values('id', 'name')]
            ))

        # create a list grouping the phases under their respective stages
        grouped_phases = []
        for phase_number, phase_info in mapping.items():
            stage_number = phase_info['stage_no']
            stage_name = phase_info['stage_name']
            phase_name = phase_info['phase_name']

            # create and initialize a flag for grouping phases and avoiding creating duplicate stages
            found_stage = False
            for stage_info in grouped_phases:
                # compare if current phase belongs to an existing stage--> add only corresponding phases
                if stage_info['stage_number'] == stage_number and stage_info['stage_name'] == stage_name:
                    stage_info['phases'].append(
                        {'phase_number': phase_number, 'phase_name': phase_name})
                    found_stage = True
                    break
            # compare if current phase belongs to new stage-> add stages and corrresponding phases
            if not found_stage:
                grouped_phases.append({
                    'stage_number': stage_number,
                    'stage_name': stage_name,
                    'phases': [{'phase_number': phase_number, 'phase_name': phase_name}]
                })

        return dict(
            result_areas=UNICEFResultArea.objects.values(
                'id', 'name', 'goal_area_id').custom_ordered(),
            goal_areas=UNICEFGoal.objects.values('id', 'name', 'capability_level_question',
                                                 'capability_category_question', 'capability_subcategory_question')
                .custom_ordered(),  # noqa: E131
            capability_levels=UNICEFCapabilityLevel.objects.values(
                'id', 'name', 'goal_area_id').custom_ordered(),
            capability_categories=UNICEFCapabilityCategory.objects.values(
                'id', 'name', 'goal_area_id')
                .custom_ordered(),
            capability_subcategories=UNICEFCapabilitySubCategory.objects.values(
                'id', 'name', 'goal_area_id')
                .custom_ordered(),
            health_focus_areas=health_focus_areas,
            hsc_challenges=hsc_challenges,
            strategies=strategies,
            regional_offices=RegionalOffice.objects.values('id', 'name'),
            currencies=Currency.objects.values('id', 'name', 'code'),
            sectors=UNICEFSector.objects.values('id', 'name').custom_ordered(),
            regional_priorities=RegionalPriority.objects.values(
                'id', 'name', 'region').custom_ordered(),
            technology_platforms=TechnologyPlatform.objects.exclude(
                state=ApprovalState.DECLINED)
                .values('id', 'name', 'state').custom_ordered(),
            hardware=HardwarePlatform.objects.exclude(
                state=ApprovalState.DECLINED)
                .values('id', 'name', 'state').custom_ordered(),
            nontech=NontechPlatform.objects.exclude(
                state=ApprovalState.DECLINED)
                .values('id', 'name', 'state').custom_ordered(),
            functions=PlatformFunction.objects.exclude(
                state=ApprovalState.DECLINED)
                .values('id', 'name', 'state').custom_ordered(),
            cpd=CPD.objects.values('id', 'name').custom_ordered(),
            innovation_categories=InnovationCategory.objects.values(
                'id', 'name').custom_ordered(),
            innovation_ways=InnovationWay.objects.values(
                'id', 'name').custom_ordered(),
            isc=ISC.objects.values('id', 'name').custom_ordered(),
            stages=Stage.objects.values('id', 'name', 'tooltip', 'order'),
            phases=Phase.objects.values('id', 'name').custom_ordered(),
            phases_stages=grouped_phases


        )


class ProjectListViewSet(TokenAuthMixin, GenericViewSet):
    pagination_class = ResultsSetPagination

    def member_list(self, user):
        data = []
        qs = Project.objects.member_of(user).order_by('-modified')
        page = self.paginate_queryset(qs)
        for project in page:
            published = project.to_representation()
            draft = project.to_representation(draft_mode=True)
            data.append(project.to_response_dict(
                published=published, draft=draft))
        return data

    def favorite_list(self, user):
        data = []
        qs = Project.objects.published_only().filter(
            favorited_by=user.userprofile).order_by('-modified')
        page = self.paginate_queryset(qs)
        for project in page:
            published = project.to_representation()
            data.append(project.to_response_dict(
                published=published, draft=None))
        return data

    def country_manager_list(self, user):
        data = []
        qs = Project.objects.country_managers_projects(user)
        page = self.paginate_queryset(qs)
        for project in page:
            published = project.to_representation()
            draft = project.to_representation(draft_mode=True)
            data.append(project.to_response_dict(
                published=published, draft=draft))
        return data

    def list(self, request, *args, **kwargs):
        """
        Retrieves list of projects user's projects.
        """
        list_name = kwargs.get('list_name')
        if list_name == 'member-of':
            data = self.member_list(request.user)
        elif list_name == 'favorite':
            data = self.favorite_list(request.user)
        elif list_name == 'country-manager':
            data = self.country_manager_list(request.user)
        elif list_name == 'review':
            # Bug: Reverse lookup does not work here for filtering
            qs = ReviewScore.objects.exclude(status=ReviewScore.STATUS_COMPLETE).\
                filter(portfolio_review__is_active=True, reviewer=request.user.userprofile). \
                exclude(portfolio_review__project__public_id__exact='').order_by(
                    '-id')
            page = self.paginate_queryset(qs)
            data_serializer = ReviewScoreDetailedSerializer(page, many=True)
            data = data_serializer.data
        else:
            raise ValidationError(
                {'list_name': 'Unknown list type'})  # pragma: no cover

        return self.get_paginated_response(data)


class ProjectLandingBlocks(TokenAuthMixin, ViewSet):
    """
    Provides data for the project blocks on the landing page:
    1. My initiatives block
    2. Recent updates block
    3. Featured initiatives block
    """

    def list(self, request, *args, **kwargs):
        my_initiatives_qs = Project.objects.member_of(request.user)
        my_initiatives_count = my_initiatives_qs.count()
        my_initiatives = my_initiatives_qs.order_by('-modified')[:3]
        recently_updated = Project.objects.published_only().exclude(
            id__in=my_initiatives_qs.values('id')).order_by('-modified')[:3]
        featured = Project.objects.published_only().filter(
            featured=True).order_by('-featured_rank')

        data = dict(my_initiatives=ProjectCardSerializer(my_initiatives, many=True, context=dict(request=request)).data,
                    my_initiatives_count=my_initiatives_count,
                    recents=ProjectCardSerializer(
                        recently_updated, many=True, context=dict(request=request)).data,
                    featured=ProjectCardSerializer(featured, many=True, context=dict(request=request)).data)

        return Response(data)


class ProjectRetrieveViewSet(TeamTokenAuthMixin, ViewSet):
    def _get_permission_based_data(self, project):
        draft = None

        if not self.request.user.is_authenticated:  # ANON
            data = project.get_anon_data()
        else:  # LOGGED IN
            data = project.get_member_data()
            draft = project.get_member_draft()

        if draft:
            draft = project.to_representation(data=draft, draft_mode=True)
        published = project.to_representation(data=data)

        return project.to_response_dict(published=published, draft=draft)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a project.
        """
        project = get_object_or_400(
            Project, "No such project", id=kwargs.get("pk"))

        return Response(self._get_permission_based_data(project))


class SolutionRetrieveViewSet(TeamTokenAuthMixin, ViewSet):
    def _get_permission_based_data(self, solution):
        published = solution.to_representation()

        return published

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a solution.
        """
        solution = get_object_or_404(
            Solution, "No such solution", id=kwargs.get("pk"))

        return Response(self._get_permission_based_data(solution))


class SolutionUpdateViewSet(SolutionAccessMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()


class CheckRequiredMixin:
    def check_required(self, queryset: QuerySet, answers: OrderedDict):
        required_ids = set(queryset.filter(
            required=True).values_list('id', flat=True))
        present_ids = {answer['question_id'] for answer in answers}
        missing_ids = required_ids - present_ids
        if missing_ids:
            return {i: ['This field is required'] for i in missing_ids}


class ProjectPublishViewSet(CheckRequiredMixin, TeamTokenAuthMixin, ViewSet):
    @transaction.atomic
    def update(self, request, project_id, country_office_id):
        """
        Publish a project
        Takes project data and custom question-answers in one go.
        """
        project = get_object_or_400(
            Project, select_for_update=True, error_message="No such project", id=project_id)
        country_office = get_object_or_400(
            CountryOffice, error_message="No such country office", id=country_office_id)
        country = country_office.country

        project_data = copy.deepcopy(
            request.data['project']) if 'project' in request.data else {}
        project_data['country'] = country.id
        project.data['country_office'] = country_office_id

        country_answers = None
        all_donor_answers = []
        errors = {}

        if 'project' not in request.data:
            raise ValidationError({'project': 'Project data is missing'})

        data_serializer = ProjectPublishedSerializer(
            project, data=project_data)

        data_serializer.fields.get('name').validators = \
            [v for v in data_serializer.fields.get(
                'name').validators if not isinstance(v, UniqueValidator)]
        data_serializer.fields.get('name').validators \
            .append(UniqueValidator(queryset=project.__class__.objects.all().exclude(id=project.id)))

        self.check_object_permissions(self.request, project)
        data_serializer.is_valid()
        if data_serializer.errors:
            errors['project'] = data_serializer.errors

        if country.country_questions.exists():
            if 'country_custom_answers' not in request.data:
                raise ValidationError(
                    {'non_field_errors': 'Country answers are missing'})
            else:
                country_answers = CountryCustomAnswerSerializer(data=request.data['country_custom_answers'], many=True,
                                                                context=dict(
                                                                    question_queryset=country.country_questions,
                                                                    is_draft=False))

                if country_answers.is_valid():
                    required_errors = self.check_required(
                        country.country_questions, country_answers.validated_data)
                    if required_errors:
                        errors['country_custom_answers'] = required_errors
                else:
                    errors['country_custom_answers'] = country_answers.errors

        for donor_id in data_serializer.validated_data.get('donors', []):
            donor = Donor.objects.get(id=donor_id)
            if donor and donor.donor_questions.exists():
                if 'donor_custom_answers' not in request.data:
                    raise ValidationError(
                        {'non_field_errors': 'Donor answers are missing'})
                if str(donor_id) not in request.data['donor_custom_answers']:
                    raise ValidationError(
                        {'non_field_errors': 'Donor answers are missing'})
                donor_answers = DonorCustomAnswerSerializer(data=request.data['donor_custom_answers'][str(donor_id)],
                                                            many=True,
                                                            context=dict(question_queryset=donor.donor_questions,
                                                                         is_draft=False))

                if not donor_answers.is_valid():
                    errors.setdefault('donor_custom_answers', {})
                    errors['donor_custom_answers'].setdefault(donor_id, {})
                    errors['donor_custom_answers'][donor_id] = donor_answers.errors
                else:
                    required_errors = self.check_required(
                        donor.donor_questions, donor_answers.validated_data)
                    if required_errors:
                        errors.setdefault('donor_custom_answers', {})
                        errors['donor_custom_answers'].setdefault(donor_id, {})
                        errors['donor_custom_answers'][donor_id] = required_errors
                    else:
                        all_donor_answers.append((donor_id, donor_answers))

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            original_data = {
                'name': project.name,
                'data': copy.deepcopy(project.data)
            }

            instance = data_serializer.save()
            if country_answers:
                country_answers.context['project'] = instance
                instance = country_answers.save()
            for donor_id, donor_answers in all_donor_answers:
                donor_answers.context['project'] = instance
                donor_answers.context['donor_id'] = donor_id
                instance = donor_answers.save()
            instance.save()

            project.refresh_from_db()  # need to do this due to JSONfield
            if project.name != original_data['name'] or project.data != original_data['data']:
                ProjectVersion.objects.create(project=project, user=request.user.userprofile, name=project.name,
                                              data=project.data, published=True)

        project.reset_approval()

        draft = instance.to_representation(draft_mode=True)
        published = instance.to_representation()
        return Response(instance.to_response_dict(published=published, draft=draft))


class ProjectUnPublishViewSet(CheckRequiredMixin, TeamTokenAuthMixin, ViewSet):
    @transaction.atomic
    def update(self, request, project_id):
        project = get_object_or_400(
            Project, select_for_update=True, error_message="No such project", id=project_id)
        project.unpublish()
        data = project.to_representation(draft_mode=True)

        ProjectVersion.objects.create(project=project, user=request.user.userprofile, name=project.name,
                                      data=project.draft, published=False)
        return Response(project.to_response_dict(published={}, draft=data), status=status.HTTP_200_OK)


class ProjectPublishAsLatestViewSet(TeamTokenAuthMixin, ViewSet):
    @transaction.atomic
    def update(self, request, project_id):
        project = get_object_or_400(
            Project, select_for_update=True, error_message="No such project", id=project_id)

        if not project.public_id:
            raise ValidationError({'project': 'Project is not published'})

        project.save()  # modification date is updated here

        draft = project.to_representation(draft_mode=True)
        published = project.to_representation()
        return Response(project.to_response_dict(published=published, draft=draft))


class ProjectDraftViewSet(TeamTokenAuthMixin, ViewSet):
    def create(self, request, country_office_id):
        """
        Creates a Draft project.
        """
        country_office = get_object_or_400(
            CountryOffice, error_message="No such country office", id=country_office_id)
        country = country_office.country

        project_data = copy.deepcopy(
            request.data['project']) if 'project' in request.data else {}
        project_data['country'] = country.id

        instance = country_answers = None
        all_donor_answers = []
        errors = {}

        if 'project' not in request.data:
            raise ValidationError({'project': 'Project data is missing'})

        data_serializer = ProjectDraftSerializer(data=project_data)
        data_serializer.is_valid()

        if data_serializer.errors:
            errors['project'] = data_serializer.errors
        else:
            instance = data_serializer.save()

        if country.country_questions.exists():
            if 'country_custom_answers' not in request.data:
                raise ValidationError(
                    {'non_field_errors': 'Country answers are missing'})
            else:
                country_answers = CountryCustomAnswerSerializer(data=request.data['country_custom_answers'], many=True,
                                                                context=dict(
                                                                    question_queryset=country.country_questions,
                                                                    is_draft=True))

                if not country_answers.is_valid():
                    errors['country_custom_answers'] = country_answers.errors

        for donor_id in data_serializer.validated_data.get('donors', []):
            donor = Donor.objects.filter(id=donor_id).first()
            if donor and donor.donor_questions.exists():
                if 'donor_custom_answers' not in request.data:
                    raise ValidationError(
                        {'non_field_errors': 'Donor answers are missing'})
                if str(donor_id) not in request.data['donor_custom_answers']:
                    raise ValidationError(
                        {'non_field_errors': 'Donor answers are missing'})
                donor_answers = DonorCustomAnswerSerializer(data=request.data['donor_custom_answers'][str(donor_id)],
                                                            many=True,
                                                            context=dict(question_queryset=donor.donor_questions,
                                                                         is_draft=True))

                if not donor_answers.is_valid():
                    errors.setdefault('donor_custom_answers', {})
                    errors['donor_custom_answers'].setdefault(donor_id, {})
                    errors['donor_custom_answers'][donor_id] = donor_answers.errors
                else:
                    all_donor_answers.append((donor_id, donor_answers))

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if country_answers:
                country_answers.context['project'] = instance
                instance = country_answers.save()
            for donor_id, donor_answers in all_donor_answers:
                donor_answers.context['project'] = instance
                donor_answers.context['donor_id'] = donor_id
                instance = donor_answers.save()
            instance.save()
            instance.team.add(request.user.userprofile)

        data = instance.to_representation(draft_mode=True)

        instance.refresh_from_db()
        ProjectVersion.objects.create(project=instance, user=request.user.userprofile, name=instance.name,
                                      data=instance.draft, published=False)

        return Response(instance.to_response_dict(published={}, draft=data), status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, project_id, country_office_id):
        """
        Updates a draft project.
        """
        project = get_object_or_400(
            Project, select_for_update=True, error_message="No such project", id=project_id)
        country_office = get_object_or_400(
            CountryOffice, error_message="No such country office", id=country_office_id)
        country = country_office.country

        project_data = copy.deepcopy(
            request.data['project']) if 'project' in request.data else {}
        project_data['country'] = country.id

        country_answers = None
        all_donor_answers = []
        errors = {}

        if 'project' not in request.data:
            raise ValidationError({'project': 'Project data is missing'})

        data_serializer = ProjectDraftSerializer(
            project, data=request.data['project'])
        self.check_object_permissions(self.request, project)
        data_serializer.is_valid()
        if data_serializer.errors:
            errors['project'] = data_serializer.errors

        if country.country_questions.exists():
            if 'country_custom_answers' not in request.data:
                raise ValidationError(
                    {'non_field_errors': 'Country answers are missing'})
            else:
                country_answers = CountryCustomAnswerSerializer(data=request.data['country_custom_answers'], many=True,
                                                                context=dict(
                                                                    question_queryset=country.country_questions,
                                                                    is_draft=True))

                if not country_answers.is_valid():
                    errors['country_custom_answers'] = country_answers.errors

        for donor_id in data_serializer.validated_data.get('donors', []):
            donor = Donor.objects.get(id=donor_id)
            if donor and donor.donor_questions.exists():
                if 'donor_custom_answers' not in request.data:
                    raise ValidationError(
                        {'non_field_errors': 'Donor answers are missing'})
                if str(donor_id) not in request.data['donor_custom_answers']:
                    raise ValidationError(
                        {'non_field_errors': 'Donor answers are missing'})

                donor_answers = DonorCustomAnswerSerializer(data=request.data['donor_custom_answers'][str(donor_id)],
                                                            many=True,
                                                            context=dict(question_queryset=donor.donor_questions,
                                                                         is_draft=True))

                if not donor_answers.is_valid():
                    errors.setdefault('donor_custom_answers', {})
                    errors['donor_custom_answers'].setdefault(donor_id, {})
                    errors['donor_custom_answers'][donor_id] = donor_answers.errors
                else:
                    all_donor_answers.append((donor_id, donor_answers))

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            original_data = {
                'name': project.name,
                'data': copy.deepcopy(project.draft),
            }
            instance = data_serializer.save()
            if country_answers:
                country_answers.context['project'] = instance
                instance = country_answers.save()
            for donor_id, donor_answers in all_donor_answers:
                donor_answers.context['project'] = instance
                donor_answers.context['donor_id'] = donor_id
                instance = donor_answers.save()
            instance.save()

        draft = instance.to_representation(draft_mode=True)
        published = instance.to_representation()

        instance.refresh_from_db()
        if instance.name != original_data['name'] or instance.draft != original_data['data']:
            ProjectVersion.objects.create(project=instance, user=request.user.userprofile, name=instance.name,
                                          data=instance.draft, published=False)
        return Response(instance.to_response_dict(published=published, draft=draft), status=status.HTTP_200_OK)


class ProjectGroupViewSet(TeamTokenAuthMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectGroupSerializer

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = get_object_or_400(
            Project, select_for_update=True, error_message="No such project", id=kwargs["pk"])
        self.check_object_permissions(self.request, instance)
        serializer = ProjectGroupSerializer(
            instance, data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MapProjectCountryViewSet(ListModelMixin, GenericViewSet):
    queryset = Project.objects.published_only()
    serializer_class = MapProjectCountrySerializer


class ProjectApprovalViewSet(TokenAuthMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, InCountryAdminForApproval)
    serializer_class = ProjectApprovalSerializer
    queryset = ProjectApproval.objects.all() \
        .select_related('project', 'project__search', 'project__search__country').exclude(project__public_id='')

    def list(self, request, country_id):
        queryset = self.filter_queryset(
            self.get_queryset().filter(project__search__country=country_id))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProjectImportV2ViewSet(TokenAuthMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, ListModelMixin,
                             GenericViewSet):
    serializer_class = ProjectImportV2Serializer
    queryset = ProjectImportV2.objects.all()

    # TODO: NEEDS COVER
    def get_queryset(self):  # pragma: no cover
        return ProjectImportV2.objects.filter(user=self.request.user)


class ImportRowViewSet(TokenAuthMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = ImportRowSerializer
    queryset = ImportRow.objects.all()

    # TODO: NEEDS COVER
    def get_queryset(self):  # pragma: no cover
        return ImportRow.objects.filter(parent__user=self.request.user)


class ApprovalRequestViewSet(CreateModelMixin, GenericViewSet):
    model = None

    def perform_create(self, serializer) -> None:
        serializer.save(added_by=self.request.user.userprofile,
                        state=ApprovalState.PENDING)
        notify_superusers_about_new_pending_approval.apply_async(
            (self.model._meta.model_name, serializer.instance.id,))


class TechnologyPlatformRequestViewSet(ApprovalRequestViewSet):
    model = TechnologyPlatform
    queryset = TechnologyPlatform.objects.all()
    serializer_class = TechnologyPlatformCreateSerializer
    permission_classes = (IsAuthenticated,)


class HardwarePlatformRequestViewSet(ApprovalRequestViewSet):
    model = HardwarePlatform
    queryset = HardwarePlatform.objects.all()
    serializer_class = HardwarePlatformCreateSerializer
    permission_classes = (IsAuthenticated,)


class NontechPlatformRequestViewSet(ApprovalRequestViewSet):
    model = NontechPlatform
    queryset = NontechPlatform.objects.all()
    serializer_class = NontechPlatformCreateSerializer
    permission_classes = (IsAuthenticated,)


class PlatformFunctionRequestViewSet(ApprovalRequestViewSet):
    model = PlatformFunction
    queryset = PlatformFunction.objects.all()
    serializer_class = PlatformFunctionCreateSerializer
    permission_classes = (IsAuthenticated,)


class PortfolioActiveListViewSet(TokenAuthMixin, ListModelMixin, GenericViewSet):
    serializer_class = PortfolioListSerializer
    queryset = Portfolio.objects.filter(status=Portfolio.STATUS_ACTIVE)


class PortfolioUserListViewSet(TokenAuthMixin, ListModelMixin, GenericViewSet):
    serializer_class = PortfolioListSerializer

    def get_queryset(self):
        return Portfolio.objects.is_manager(self.request.user)


class PortfolioCreateViewSet(GPOAccessMixin, CreateModelMixin, GenericViewSet):
    serializer_class = PortfolioSerializer


class PortfolioUpdateViewSet(PortfolioAccessMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()

    def _check_ps_status(self, request, *args, **kwargs) -> bool:
        instance = self.get_object()

        if 'problem_statements' in request.data:
            r_ps_ids = {ps['id'] for ps in request.data.get(
                'problem_statements', []) if 'id' in ps}

            non_modifiable_ps = instance.problem_statements.filter(
                projectportfoliostate__approved=True)
            ps_removed = instance.problem_statements.exclude(id__in=r_ps_ids)

            if non_modifiable_ps.intersection(ps_removed):
                raise PermissionDenied("Problem Statements linked to approved projects may not be deleted: [{}]".format(
                    ", ".join([str(x) for x in non_modifiable_ps.intersection(
                        ps_removed).values_list('id', flat=True)])
                ))

    def update(self, request, *args, **kwargs):
        self._check_ps_status(request, *args, **kwargs)
        return super(PortfolioUpdateViewSet, self).update(request, *args, **kwargs)


class PortfolioProjectChangeReviewStatusViewSet(PortfolioAccessMixin, GenericViewSet):
    serializer_class = PortfolioStateChangeSerializer

    def _check_input_and_permissions(self, request, *args, **kwargs):
        # check if portfolio exists
        portfolio = get_object_or_400(
            Portfolio, "No such portfolio", id=kwargs.get("pk"))

        self.check_object_permissions(request, portfolio)
        if 'project' not in request.data or len(request.data['project']) == 0:
            raise ValidationError({'project': 'Project data is missing'})
        return portfolio

    def move_from_inventory_to_review(self, request, *args, **kwargs):
        portfolio = self._check_input_and_permissions(request, *args, **kwargs)
        # For some reason the reverse lookup for ActiveQuerySet fails at this point
        projects_in_portfolio = list(
            portfolio.review_states.all().values_list('project', flat=True))
        projects = Project.objects.filter(id__in=request.data['project']).\
            exclude(id__in=projects_in_portfolio)
        if len(projects) == 0:
            raise ValidationError({'project': 'Project data is incorrect'})
        # create a new review for each project if needed
        for project in projects:
            qs_pps = ProjectPortfolioState.all_objects.filter(
                portfolio=portfolio, project=project, is_active=False)
            if qs_pps:
                ReviewScore.all_objects.filter(
                    portfolio_review=qs_pps[0]).update(is_active=True)
            qs_pps.update(is_active=True)
            ProjectPortfolioState.objects.get_or_create(
                portfolio=portfolio, project=project)

        return Response(PortfolioStateChangeSerializer(portfolio).data, status=status.HTTP_201_CREATED)

    def move_to_inventory(self, request, *args, **kwargs):
        portfolio = self._check_input_and_permissions(request, *args, **kwargs)

        review_states = portfolio.review_states.filter(
            project__in=request.data['project'], approved=False)
        if len(review_states) == 0:
            raise ValidationError({'project': 'Projects are not in review'})

        # Remove each review_state from portfolio
        for rev_state in review_states:
            rev_state.review_scores.all().update(
                is_active=False)  # disable reviews linked to pps
            rev_state.delete()
        return Response(PortfolioStateChangeSerializer(portfolio).data, status=status.HTTP_200_OK)

    def approve(self, request, *args, **kwargs):
        portfolio = self._check_input_and_permissions(request, *args, **kwargs)
        # only completed and unapproved projects can be approved
        review_states = portfolio.review_states.filter(project__in=request.data['project'],
                                                       reviewed=True, approved=False)
        if len(review_states) == 0:
            raise ValidationError(
                {'project': 'Status change not valid for provided projects'})

        # Approve each review state
        for rev_state in review_states:
            rev_state.approved = True
            rev_state.save()

        return Response(PortfolioStateChangeSerializer(portfolio).data, status=status.HTTP_200_OK)

    def disapprove(self, request, *args, **kwargs):
        portfolio = self._check_input_and_permissions(request, *args, **kwargs)
        # only approved projects can be disapproved
        review_states = portfolio.review_states.filter(
            project__in=request.data['project'], approved=True)
        if len(review_states) == 0:
            raise ValidationError(
                {'project': 'Status change not valid for provided projects'})  # pragma: no cover

        # Disapprove each review state
        for rev_state in review_states:
            rev_state.approved = False
            rev_state.save()

        return Response(PortfolioStateChangeSerializer(portfolio).data, status=status.HTTP_200_OK)


class PortfolioReviewAssignQuestionnaireViewSet(PortfolioAccessMixin, GenericViewSet):
    serializer_class = ReviewScoreBriefSerializer

    def get_project_and_portfolio(self):
        portfolio = get_object_or_400(
            Portfolio, "No such portfolio", id=self.kwargs.get("portfolio"))

        pps = portfolio.review_states.get(
            project=self.kwargs.get('project_id'))
        return portfolio, pps

    def create_questionnaire(self, request, *args, **kwargs):
        portfolio, pps = self.get_project_and_portfolio()
        self.check_object_permissions(request, portfolio)

        if 'userprofile' not in request.data:
            raise ValidationError(
                {'userprofile': 'UserProfile data is missing'})  # pragma: no cover
        userprofiles = UserProfile.objects.filter(
            pk__in=request.data.get('userprofile'))
        scores = list()
        for profile in userprofiles:
            score, created = pps.assign_questionnaire(user=profile)
            scores.append(score)
            if created:
                from project.tasks import project_review_requested_on_create_notification
                project_review_requested_on_create_notification.apply_async(args=[score.id,
                                                                                  request.data.get('message', None)], )
        # return with scores
        data_serializer = ReviewScoreBriefSerializer(scores, many=True)
        return Response(data_serializer.data, status=status.HTTP_200_OK)


class ReviewScoreAccessSet(ReviewScoreAccessMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """ Retrieve or destroy an user review

        Returns with a serialized ReviewScore object on success
    """
    serializer_class = ReviewScoreSerializer
    queryset = ReviewScore.objects.all()

    def perform_destroy(self, instance):
        """ Custom delete for ReviewScore API

            When we delete a review score, we need the hard delete
        """
        ReviewScore.objects.filter(id=instance.id).force_delete()


class ReviewScoreAnswerViewSet(ReviewScoreReviewerAccessMixin, UpdateModelMixin, GenericViewSet):
    """ Fill or complete an user review

    `status` is optional, can be used to set a review to complete. Edited `ReviewScore` objects will always have
    a *draft* status, unless they are set as *complete*

    Allowed values for `status` are:

    * `PD` - pending

    * `DR` - draft

    * `CMP` - complete

    """
    serializer_class = ReviewScoreFillSerializer
    queryset = ReviewScore.objects.all()


class ProjectPortfolioStateManagerViewSet(ProjectPortfolioStateAccessMixin, RetrieveModelMixin, UpdateModelMixin,
                                          GenericViewSet):
    serializer_class = ProjectPortfolioStateManagerSerializer

    def get_object(self):
        pps = get_object_or_400(ProjectPortfolioState,
                                pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, pps)

        if self.request.method == 'POST' and pps.approved:
            raise PermissionDenied(
                "Approved project reviews may not be edited")

        return pps


class ProjectModifyFavoritesViewSet(TokenAuthMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Project.objects.published_only()
    serializer_class = UserProfileSerializer

    def add(self, request, *args, **kwargs):
        """
        Adds the project in the POST request's body to the user's favorite projects

        Request body can be EMPTY
        """
        self.request.user.userprofile.favorite_projects.add(self.get_object())
        self.request.user.userprofile.save()

        data_serializer = UserProfileSerializer(self.request.user.userprofile)
        return Response(data_serializer.data, status=status.HTTP_200_OK)

    def remove(self, request, *args, **kwargs):
        """
        Removes the projects in the POST request's body to the user's favorite projects

        Request body can be EMPTY

        """
        self.request.user.userprofile.favorite_projects.remove(
            self.get_object())
        self.request.user.userprofile.save()

        data_serializer = UserProfileSerializer(self.request.user.userprofile)
        return Response(data_serializer.data, status=status.HTTP_200_OK)


class ProjectImageUploadViewSet(TokenAuthMixin, UpdateModelMixin, GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectImageUploadSerializer
    parser_classes = (MultiPartParser,)


class CountryManagerExportView(TokenAuthMixin, GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        queryset = Project.objects.country_managers_projects(request.user)
        project_resource = ProjectResource()
        project_resource.get_queryset = lambda: queryset
        dataset = project_resource.export()

        filename = f'country_manager_export_{str(date.today())}.xlsx'
        response = HttpResponse(
            dataset.xlsx,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


class ProblemStatementListViewSet(TokenAuthMixin, ListModelMixin, GenericViewSet):
    queryset = ProblemStatement.objects.all()
    serializer_class = ProblemStatementSerializer


class SolutionListViewSet(TokenAuthMixin, ListModelMixin, GenericViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer


class SolutionCreateViewSet(TokenAuthMixin, CreateModelMixin, GenericViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer


class ProjectVersionHistoryViewSet(TokenAuthMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectVersionHistorySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        is_country_manager = False
        co_id = instance.get_country_office_id()
        if co_id:
            is_country_manager = request.user.userprofile.manager_of.filter(
                id=co_id).exists()

        if request.user.is_superuser or instance.team.filter(id=request.user.userprofile.id).exists() or \
                instance.viewers.filter(id=request.user.userprofile.id).exists() or is_country_manager:
            serializer = self.serializer_class(
                instance.versions.all(), many=True)
        else:
            serializer = self.serializer_class(
                instance.versions.filter(published=True), many=True)

        return Response(serializer.data)


class PortfolioViewSet(TokenAuthMixin, GenericViewSet):

    queryset = Portfolio.objects.all()

    def retrieve(self, request, *args, **kwargs):
        portfolio = get_object_or_404(
            Portfolio, "No such portfolio", id=kwargs.get("pk"))
        response_data = {
            'id': portfolio.id,
            'solutions': []
        }

        for solution in portfolio.solutions.all():
            if solution.is_active == True:
                solution_data = {
                    'id': solution.pk,
                    'name': solution.name,
                    'problemStatements': [{'id': problem_statement.pk, 'name': problem_statement.name} for problem_statement in solution.problem_statements.filter(portfolio=portfolio)],
                    'phase': solution.phase,
                    'reach': solution.people_reached,
                }
                response_data['solutions'].append(solution_data)

        return Response(response_data)
