from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ReadOnlyField
from rest_framework.validators import UniqueValidator
from dateutil.parser import parse, ParserError

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery  # noqa
from django.utils.translation import ugettext_lazy as _

from core.utils import send_mail_wrapper
from country.models import CustomQuestion, CountryOffice, Country
from country.serializers import UserProfileSerializer
from project.utils import remove_keys
from tiip.validators import EmailEndingValidator
from user.models import UserProfile
from .models import (
    Project,
    ProjectApproval,
    ImportRow,
    ProjectImportV2,
    Portfolio,
    ProblemStatement,
    ProjectPortfolioState,
    ReviewScore,
    TechnologyPlatform,
    HardwarePlatform,
    NontechPlatform,
    PlatformFunction,
    Stage,
    Solution,
    CountrySolution,
    ProjectVersion,
)


class PartnerSerializer(serializers.Serializer):
    PARTNER_TYPE = [
        (0, _("Investment")),
        (1, _("Government")),
        (2, _("Programme")),
        (3, _("Technology")),
    ]

    partner_type = serializers.ChoiceField(choices=PARTNER_TYPE)
    partner_name = serializers.CharField(max_length=100)
    partner_contact = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    partner_email = serializers.EmailField(required=False, allow_blank=True)
    partner_website = serializers.URLField(
        max_length=2048, required=False, allow_blank=True
    )


class LinkSerializer(serializers.Serializer):
    LINK_TYPE = [
        (0, _("Website")),
        (1, _("SharePoint Repository ")),
        (2, _("External Advocacy/Communications")),
        (3, _("Monitoring, Evaluation or Learning")),
        (4, _("Other Documents/Resources")),
    ]

    link_type = serializers.ChoiceField(choices=LINK_TYPE)
    link_url = serializers.URLField(max_length=2048, required=False, allow_blank=True)


class StageSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    date = serializers.CharField(required=True, max_length=10)
    note = serializers.CharField(required=False, max_length=256, allow_null=True)


class ProjectPublishedSerializer(serializers.Serializer):
    # UNICEF Office and co
    country_office = serializers.IntegerField(
        min_value=1, max_value=100000, required=True
    )
    country = serializers.ReadOnlyField()
    regional_office = serializers.ReadOnlyField()

    # SECTION 1 General
    name = serializers.CharField(
        max_length=128, validators=[UniqueValidator(queryset=Project.objects.all())]
    )
    organisation = serializers.CharField(max_length=128)
    overview = serializers.CharField(max_length=300, required=True)
    implementation_overview = serializers.CharField(max_length=1024, required=False)
    start_date = serializers.CharField(max_length=256, required=True)
    end_date = serializers.CharField(max_length=256, required=False, allow_blank=True)
    end_date_note = serializers.CharField(
        max_length=256, required=False, allow_blank=True
    )
    contact_name = serializers.CharField(max_length=256)
    contact_email = serializers.EmailField()

    # UNICEF SECTION
    goal_area = serializers.IntegerField()
    result_area = serializers.IntegerField(required=False)
    capability_levels = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    capability_categories = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    capability_subcategories = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )

    # NEW FIELDS
    innovation_categories = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    unicef_sector = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=1, required=True
    )
    unicef_supporting_sectors = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    unicef_leading_sector = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    regional_priorities = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    program_targets = serializers.CharField(max_length=1024, required=False)
    program_targets_achieved = serializers.CharField(max_length=1024, required=False)
    target_group_reached = serializers.IntegerField(required=False)
    current_achievements = serializers.CharField(max_length=2048, required=False)
    cpd = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    awp = serializers.CharField(max_length=500, required=False)
    wbs = serializers.ListField(
        child=serializers.CharField(max_length=30),
        max_length=50,
        min_length=0,
        required=False,
        allow_empty=True,
    )
    total_budget = serializers.IntegerField(required=False)
    total_budget_narrative = serializers.CharField(max_length=500, required=False)
    funding_needs = serializers.CharField(max_length=500, required=False)
    partnership_needs = serializers.CharField(max_length=500, required=False)
    currency = serializers.IntegerField(required=False)
    hardware = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    nontech = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    functions = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )

    links = LinkSerializer(many=True, required=False, allow_empty=True)
    partners = PartnerSerializer(many=True, required=False, allow_empty=True)

    # ITERATION 2 Fields
    innovation_ways = serializers.ListField(
        child=serializers.IntegerField(),
        max_length=64,
        min_length=0,
        allow_empty=True,
        required=False,
    )
    isc = serializers.IntegerField(required=False)

    # SECTION 2 Implementation Overview
    platforms = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    dhis = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    health_focus_areas = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    hsc_challenges = serializers.ListField(
        child=serializers.IntegerField(),
        max_length=64,
        min_length=0,
        allow_empty=True,
        required=False,
    )
    donors = serializers.ListField(
        child=serializers.IntegerField(), max_length=32, required=False
    )

    stages = StageSerializer(many=True, required=False, allow_empty=True)
    phase = serializers.IntegerField(required=False)
    current_phase = serializers.IntegerField(required=False)

    class Meta:
        model = Project

    def validate_country_office(self, value):
        try:
            self.co = CountryOffice.objects.get(id=value)
        except CountryOffice.DoesNotExist:
            raise serializers.ValidationError("Country office does not exist.")

        if self.instance:
            project = Project.objects.get(id=self.instance.id)
            if (
                project.public_id
                and "country_office" in project.data
                and project.data["country_office"]
                != self.initial_data["country_office"]
            ):
                raise serializers.ValidationError(
                    "Country office cannot be altered on published projects."
                )
        return value

    @staticmethod
    def validate_date(value):
        try:
            parse(value)
        except ParserError:
            raise serializers.ValidationError("Wrong date format")
        return value

    def validate_start_date(self, value):
        return self.validate_date(value)

    def validate_end_date(self, value):
        return self.validate_date(value)

    def validate(self, attrs):
        if attrs.get("end_date"):
            if parse(attrs.get("end_date")) < parse(attrs.get("start_date")):
                raise serializers.ValidationError(
                    {"end_date": "End date cannot be earlier than start date"}
                )
        return attrs

    def update(self, instance, validated_data):
        validated_data["country"] = self.co.country.id
        validated_data["regional_office"] = (
            self.co.regional_office.id if self.co.regional_office else ""
        )
        validated_data["current_phase"] = Stage.calc_current_phase(
            validated_data.get("stages", [])
        )
        instance.name = validated_data["name"]
        instance.data = validated_data
        instance.draft = validated_data
        instance.make_public_id(validated_data["country"])
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
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    unicef_supporting_sectors = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )
    unicef_leading_sector = serializers.ListField(
        child=serializers.IntegerField(), max_length=64, min_length=0, allow_empty=True
    )

    def create(self, validated_data):
        validated_data["country"] = self.co.country.id
        validated_data["regional_office"] = (
            self.co.regional_office.id if self.co.regional_office else ""
        )
        validated_data["current_phase"] = Stage.calc_current_phase(
            validated_data.get("stages", [])
        )
        return self.Meta.model(
            name=validated_data["name"],
            draft=validated_data,
        )

    def update(self, instance, validated_data):
        if not instance.public_id:
            instance.name = validated_data["name"]

        validated_data["country"] = self.co.country.id
        validated_data["regional_office"] = (
            self.co.regional_office.id if self.co.regional_office else ""
        )
        validated_data["current_phase"] = Stage.calc_current_phase(
            validated_data.get("stages", [])
        )
        instance.draft = validated_data
        return instance


class ProjectGroupSerializer(serializers.ModelSerializer):
    new_team_emails = serializers.ListField(
        child=serializers.EmailField(validators=[EmailEndingValidator()]),
        max_length=64,
        min_length=0,
        allow_empty=True,
        required=False,
    )
    new_viewer_emails = serializers.ListField(
        child=serializers.EmailField(validators=[EmailEndingValidator()]),
        max_length=64,
        min_length=0,
        allow_empty=True,
        required=False,
    )

    class Meta:
        model = Project
        fields = ("team", "viewers", "new_team_emails", "new_viewer_emails")
        read_only_fields = ("id",)

    def perform_create(self, email):
        user = User.objects.create_user(username=email[:150], email=email)
        UserProfile.objects.create(user=user, account_type=UserProfile.DONOR)
        return user

    def save(self, **kwargs):
        for email in self.validated_data.get("new_team_emails", []):
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = self.perform_create(email)
            self.validated_data["team"].append(user.userprofile)

        for email in self.validated_data.get("new_viewer_emails", []):
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = self.perform_create(email)
            self.validated_data["viewers"].append(user.userprofile)

        self.validated_data.pop("new_team_emails", None)
        self.validated_data.pop("new_viewer_emails", None)

        # remove duplicates
        self.validated_data["team"] = list(set(self.validated_data["team"]))
        self.validated_data["viewers"] = list(set(self.validated_data["viewers"]))

        return super().save(**kwargs)

    def update(self, instance, validated_data):
        self._send_notification(instance, validated_data)

        # don't allow empty team, so no orphan projects
        if "team" in validated_data and isinstance(validated_data["team"], list):
            instance.team.set(validated_data.get("team") or instance.team.all())

        # a project however can exist without viewers
        if "viewers" in validated_data and isinstance(validated_data["viewers"], list):
            instance.viewers.set(validated_data["viewers"])

        instance.save()

        return instance

    def _send_notification(self, instance, validated_data):
        new_team_members = [
            x for x in validated_data.get("team", []) if x not in instance.team.all()
        ]
        new_viewers = [
            x
            for x in validated_data.get("viewers", [])
            if x not in instance.viewers.all()
        ]

        for profile in new_team_members:
            context = {
                "user_name": profile.name if profile.name else profile.user.email,
                "project_id": instance.id,
                "project_name": instance.name,
                "role": "team member",
            }
            send_mail_wrapper(
                subject="You have been added to a project in the T4D & Innovation Inventory Portal",
                email_type="new_member",
                to=profile.user.email,
                language=profile.language,
                context=context,
            )

        for profile in new_viewers:
            context = {
                "user_name": profile.name if profile.name else profile.user.email,
                "project_id": instance.id,
                "project_name": instance.name,
                "role": "viewer",
            }
            send_mail_wrapper(
                subject="You have been added to a project in the T4D & Innovation Inventory Portal",
                email_type="new_member",
                to=profile.user.email,
                language=profile.language,
                context=context,
            )


class MapProjectCountrySerializer(serializers.ModelSerializer):
    country = ReadOnlyField(source="get_country_id")

    class Meta:
        model = Project
        fields = ("id", "name", "country")


class CustomAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)
    answer = serializers.ListField(
        child=serializers.CharField(max_length=512),
        max_length=50,
        min_length=0,
        required=True,
    )

    def validate_question_id(self, value):
        self.context["question"] = (
            self.context["question_queryset"].filter(id=int(value)).first()
        )
        if not self.context["question"]:
            raise ValidationError("This question_id does not exist.")
        return value

    def validate_required_answer(self, value):
        if not value:
            raise ValidationError({"answer": "This field is required."})

    def validate_numeric_answer(self, value):
        if value and isinstance(value[0], str) and not value[0].isnumeric():
            raise ValidationError({"answer": "This field must be numeric."})

    def validate_answer_length(self, value):
        if value and len(value) > 1:
            raise ValidationError({"answer": "There must be 1 answer only."})

    def validate(self, attrs):
        if not self.context["is_draft"]:
            if self.context["question"].required:
                self.validate_required_answer(attrs["answer"])
            if self.context["question"].type != CustomQuestion.MULTI:
                self.validate_answer_length(attrs["answer"])
            if self.context["question"].type == CustomQuestion.NUMBER:
                self.validate_numeric_answer(attrs["answer"])
        return attrs


class CountryCustomAnswerListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        instance = self.context["project"]
        custom_answers = {k["question_id"]: k["answer"] for k in validated_data}
        instance.draft["country_custom_answers"] = custom_answers
        if not self.context["is_draft"]:
            private_ids = (
                self.context["question_queryset"]
                .filter(private=True)
                .values_list("id", flat=True)
            )
            if private_ids:
                private_answers = {
                    k: custom_answers[k] for k in custom_answers if k in private_ids
                }
                instance.data["country_custom_answers_private"] = private_answers
                instance.data["country_custom_answers"] = remove_keys(
                    data_dict=custom_answers, keys=private_ids
                )
            else:
                instance.data["country_custom_answers"] = custom_answers
        return instance


class DonorCustomAnswerListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        instance = self.context["project"]
        donor_id = self.context["donor_id"]

        custom_answers = {k["question_id"]: k["answer"] for k in validated_data}
        instance.draft.setdefault("donor_custom_answers", {})
        instance.draft["donor_custom_answers"].setdefault(donor_id, {})
        instance.draft["donor_custom_answers"][donor_id] = custom_answers

        if not self.context["is_draft"]:
            private_ids = (
                self.context["question_queryset"]
                .filter(private=True)
                .values_list("id", flat=True)
            )
            if private_ids:
                private_answers = {
                    k: custom_answers[k] for k in custom_answers if k in private_ids
                }
                instance.data.setdefault("donor_custom_answers_private", {})
                instance.data["donor_custom_answers_private"].setdefault(donor_id, {})
                instance.data["donor_custom_answers_private"][
                    donor_id
                ] = private_answers
                instance.data["donor_custom_answers"][donor_id] = remove_keys(
                    data_dict=custom_answers, keys=private_ids
                )
            else:
                instance.data.setdefault("donor_custom_answers", {})
                instance.data["donor_custom_answers"].setdefault(donor_id, {})
                instance.data["donor_custom_answers"][donor_id] = custom_answers
        return instance


class CountryCustomAnswerSerializer(CustomAnswerSerializer):
    class Meta:
        list_serializer_class = CountryCustomAnswerListSerializer


class DonorCustomAnswerSerializer(CustomAnswerSerializer):
    class Meta:
        list_serializer_class = DonorCustomAnswerListSerializer


class ProjectApprovalSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source="project_id")
    project_name = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()
    legacy_approved_by = serializers.ReadOnlyField(source="user_id")

    class Meta:
        model = ProjectApproval
        fields = (
            "id",
            "project_name",
            "created",
            "modified",
            "approved",
            "reason",
            "project",
            "history",
            "legacy_approved_by",
        )

    def get_project_name(self, obj):
        return obj.project.name

    def get_history(self, obj):
        return obj.history.values(
            "history_user__userprofile", "approved", "reason", "modified"
        )


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
        fields = (
            "id",
            "user",
            "status",
            "header_mapping",
            "rows",
            "country",
            "country_office",
            "donor",
            "filename",
            "sheet_name",
            "draft",
        )

    # TODO: Need Coverage
    def create(self, validated_data):  # pragma: no cover
        rows = validated_data.pop("rows")
        instance = super().create(validated_data)
        for row_data in rows[0].get("data", []):
            ImportRow.objects.create(
                parent=instance, data=row_data, original_data=row_data
            )
        return instance

    # TODO: Need Coverage
    def update(self, instance, validated_data):  # pragma: no cover
        rows = validated_data.pop("rows", [])
        instance = super().update(instance, validated_data)
        for row in rows:
            ImportRow.objects.get(id=row["id"]).update(data=row.get("data"))
        return instance


class TechnologyPlatformCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=512,
        validators=[
            UniqueValidator(queryset=TechnologyPlatform.objects.all(), lookup="iexact")
        ],
    )

    class Meta:
        model = TechnologyPlatform
        fields = "__all__"
        read_only_fields = ("is_active", "state", "added_by")


class HardwarePlatformCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=512,
        validators=[
            UniqueValidator(queryset=HardwarePlatform.objects.all(), lookup="iexact")
        ],
    )

    class Meta:
        model = HardwarePlatform
        fields = "__all__"
        read_only_fields = ("is_active", "state", "added_by")


class NontechPlatformCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=512,
        validators=[
            UniqueValidator(queryset=NontechPlatform.objects.all(), lookup="iexact")
        ],
    )

    class Meta:
        model = NontechPlatform
        fields = "__all__"
        read_only_fields = ("is_active", "state", "added_by")


class PlatformFunctionCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=512,
        validators=[
            UniqueValidator(queryset=PlatformFunction.objects.all(), lookup="iexact")
        ],
    )

    class Meta:
        model = PlatformFunction
        fields = "__all__"
        read_only_fields = ("is_active", "state", "added_by")


class ProblemStatementSerializer(serializers.ModelSerializer):
    portfolio_name = serializers.StringRelatedField(source="portfolio.name")

    class Meta:
        model = ProblemStatement
        fields = ("id", "name", "description", "portfolio_name")
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }


class PortfolioListSerializer(serializers.ModelSerializer):
    project_count = serializers.SerializerMethodField()
    managers = UserProfileSerializer(many=True)

    problem_statements = ProblemStatementSerializer(many=True)

    class Meta:
        model = Portfolio
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "project_count",
            "managers",
            "status",
            "landscape_review",
            "problem_statements",
            "investment_to_date",
            "innovation_hub",
        )

    @staticmethod
    def get_project_count(obj):
        return len(
            Project.objects.published_only().filter(
                is_active=True, review_states__in=obj.review_states.all()
            )
        )


class ReviewScoreBriefSerializer(serializers.ModelSerializer):
    reviewer = UserProfileSerializer()

    class Meta:
        model = ReviewScore
        fields = (
            "id",
            "created",
            "modified",
            "reviewer",
            "portfolio_review",
            "status",
            "overall_reviewer_feedback",
        )


class ProjectPortfolioStateSerializer(serializers.ModelSerializer):
    review_scores = ReviewScoreBriefSerializer(many=True, required=False)

    class Meta:
        model = ProjectPortfolioState
        fields = "__all__"


class ReviewScoreSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=ReviewScore.STATUS_CHOICES)
    reviewer = UserProfileSerializer(read_only=True)

    class Meta:
        model = ReviewScore
        fields = "__all__"


class ProjectPortfolioStateManagerSerializer(serializers.ModelSerializer):
    impact = serializers.ChoiceField(
        required=True, choices=ProjectPortfolioState.BASE_CHOICES, allow_blank=False
    )
    scale_phase = serializers.ChoiceField(
        required=True, choices=ProjectPortfolioState.SCALE_CHOICES, allow_blank=False
    )
    project = serializers.IntegerField(read_only=True, source="project.id")
    portfolio = serializers.IntegerField(read_only=True, source="portfolio.id")
    review_scores = ReviewScoreSerializer(many=True, read_only=True, required=False)
    averages = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = ProjectPortfolioState
        fields = "__all__"

    def update(self, instance, validated_data):
        """
        Override serializer to set 'reviewed' to True
        """
        instance.reviewed = True
        instance = super().update(instance, validated_data)
        return instance

    @staticmethod
    def get_averages(obj):
        complete_scores = obj.review_scores.filter(status=ReviewScore.STATUS_COMPLETE)

        def calc_avg(in_list: list):
            return (sum(in_list) / len(in_list)) if in_list else None

        return {
            "rnci": calc_avg([score.rnci for score in complete_scores if score.rnci]),
            "ratp": calc_avg([score.ratp for score in complete_scores if score.ratp]),
            "ra": calc_avg([score.ra for score in complete_scores if score.ra]),
            "ee": calc_avg([score.ee for score in complete_scores if score.ee]),
            "nst": calc_avg([score.nst for score in complete_scores if score.nst]),
            "ps": calc_avg([score.ps for score in complete_scores if score.ps]),
            "nc": calc_avg([score.nc for score in complete_scores if score.nc]),
        }


class PortfolioSerializer(serializers.ModelSerializer):
    problem_statements = ProblemStatementSerializer(many=True, required=False)

    class Meta:
        model = Portfolio
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "status",
            "managers",
            "landscape_review",
            "problem_statements",
            "investment_to_date",
            "innovation_hub",
        )

    @staticmethod
    def _create_problem_statements(instance, problem_statements):
        for ps in problem_statements:
            ProblemStatement.objects.create(
                name=ps["name"], description=ps["description"], portfolio=instance
            )

    def create(self, validated_data):
        """
        Creates new portfolio - needs explicit serializer due to nested fields
        """
        problem_statements = validated_data.pop("problem_statements")
        instance = super().create(validated_data)

        self._create_problem_statements(instance, problem_statements)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Override serializer due to nested Problem Statements
        """

        if "problem_statements" in validated_data:  # this is to support PATCH update
            ps_data = validated_data.pop("problem_statements")
            instance = super().update(instance, validated_data)
            # Handle delete
            update_ids = {ps["id"] for ps in ps_data if "id" in ps}
            existing_pss = instance.problem_statements.all()

            for ps_exist in existing_pss:
                if (
                    ps_exist.id not in update_ids
                ):  # Delete problem statements not in update data
                    ps_exist.delete()
            for ps in ps_data:
                ps["portfolio_id"] = instance.id
                ProblemStatement.objects.update_or_create(
                    id=ps["id"] if "id" in ps else None, defaults=ps
                )
        else:
            instance = super().update(instance, validated_data)
        return instance


class PortfolioStateChangeSerializer(PortfolioSerializer):
    review_states = ProjectPortfolioStateSerializer(
        many=True, required=False, read_only=True
    )

    class Meta:
        model = Portfolio
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "status",
            "managers",
            "review_states",
        )


class ReviewScoreFillSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        required=False, choices=ReviewScore.STATUS_CHOICES, allow_blank=False
    )

    class Meta:
        model = ReviewScore
        fields = (
            "psa",
            "psa_comment",
            "rnci",
            "rnci_comment",
            "ratp",
            "ratp_comment",
            "ra",
            "ra_comment",
            "ee",
            "ee_comment",
            "nst",
            "nst_comment",
            "nc",
            "nc_comment",
            "ps",
            "ps_comment",
            "overall_reviewer_feedback",
            "status",
        )

    def update(self, instance, validated_data):
        """
        Override serializer to set status
        """
        if instance.status != ReviewScore.STATUS_COMPLETE:
            instance.status = ReviewScore.STATUS_DRAFT
        instance = super().update(instance, validated_data)
        return instance


class ReviewScoreDetailedSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source="get_project_data")
    portfolio = PortfolioSerializer(read_only=True, source="get_portfolio")
    portfolio_review = ProjectPortfolioStateSerializer(read_only=True)
    status = serializers.ChoiceField(choices=ReviewScore.STATUS_CHOICES)

    class Meta:
        model = ReviewScore
        fields = "__all__"


class ProjectCardSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()
    is_draft = serializers.SerializerMethodField()
    unicef_office = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Project
        read_only_fields = (
            "id",
            "name",
            "modified",
            "is_draft",
            "description",
            "unicef_office",
            "country",
            "team",
            "thumbnail",
        )
        fields = read_only_fields

    @staticmethod
    def get_name(obj):
        return obj.name if obj.public_id else obj.draft.get("name", "")

    @staticmethod
    def get_is_draft(obj):
        return obj.public_id == ""

    @staticmethod
    def get_description(obj):
        data = obj.data if obj.public_id else obj.draft
        return data.get("implementation_overview", "")

    @staticmethod
    def get_unicef_office(obj):
        data = obj.data if obj.public_id else obj.draft
        return data.get("country_office", "")

    @staticmethod
    def get_country(obj):
        return obj.get_country_id(draft_mode=obj.public_id == "")

    def get_team(self, obj):
        qs = obj.team.all()
        request = self.context.get("request")
        user_in_team = (
            request
            and request.user
            and request.user.userprofile
            and obj.team.filter(id=request.user.userprofile.id).exists()
        )

        if user_in_team:
            my_index = list(qs.values_list("id", flat=True)).index(
                request.user.userprofile.id
            )
            team_list = list(qs)
            if my_index != 0:
                team_list.insert(0, team_list.pop(my_index))

            return UserProfileSerializer(team_list, many=True).data
        return UserProfileSerializer(qs, many=True).data

    @staticmethod
    def get_thumbnail(obj):
        return obj.thumbnail.url if obj.thumbnail else None


class ProjectImageUploadSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ("id", "image", "image_url", "thumbnail")

    @staticmethod
    def get_thumbnail(obj):
        return obj.thumbnail.url if obj.thumbnail else None


class CountrySolutionSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    class Meta:
        model = CountrySolution
        fields = ("country", "people_reached", "region")


class PortfolioProblemStatementSerializer(serializers.ModelSerializer):
    problem_statements = ProblemStatementSerializer(many=True)
    portfolio = serializers.IntegerField(read_only=True, source="portfolio.id")

    class Meta:
        model = CountrySolution
        fields = ("id", "people_reached", "region", "portfolio", "problem_statements")


class SolutionSerializer(serializers.ModelSerializer):
    countries = CountrySolutionSerializer(
        source="countrysolution_set", many=True, read_only=True
    )
    country_solutions = CountrySolutionSerializer(
        many=True, write_only=True, required=False
    )
    portfolio_problem_statements = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
    )
    people_reached = serializers.IntegerField(allow_null=True)
    problem_statements = ProblemStatementSerializer(many=True, required=False)
    portfolios = PortfolioSerializer(many=True, required=False)

    class Meta:
        model = Solution
        fields = (
            "id",
            "name",
            "portfolios",
            "countries",
            "problem_statements",
            "phase",
            "open_source_frontier_tech",
            "learning_investment",
            "people_reached",
            "is_active",
            "portfolio_problem_statements",
            "country_solutions",
        )

    def create(self, validated_data):
        country_solutions_data = validated_data.pop("country_solutions", [])
        portfolio_problem_statements_data = validated_data.pop(
            "portfolio_problem_statements", []
        )
        solution = Solution.objects.create(**validated_data)

        for pps_data in portfolio_problem_statements_data:
            portfolio_id = pps_data.pop("portfolio_id")
            problem_statements_ids = pps_data.pop("problem_statements")
            portfolio = Portfolio.objects.get(id=portfolio_id)
            solution.portfolios.add(portfolio)

            for ps_id in problem_statements_ids:
                problem_statement = ProblemStatement.objects.get(id=ps_id)
                solution.problem_statements.add(problem_statement)

        for country_data in country_solutions_data:
            country_solution = CountrySolution(solution=solution)
            for attr, value in country_data.items():
                setattr(country_solution, attr, value)
            country_solution.save()

        return solution

    def update(self, instance, validated_data):
        country_solutions_data = validated_data.pop("country_solutions", [])
        portfolio_problem_statements_data = validated_data.pop(
            "portfolio_problem_statements", []
        )
        instance = super().update(instance, validated_data)

        # Remove existing CountrySolution instances related to the current Solution instance
        instance.countrysolution_set.all().delete()

        for country_data in country_solutions_data:
            if "id" in country_data:
                # We don't need this anymore, as we are creating a new instance
                country_data.pop("id")
            country_solution = CountrySolution(solution=instance, **country_data)
            country_solution.save()

        # Clear existing problem_statements and portfolios
        instance.problem_statements.clear()
        instance.portfolios.clear()

        for pps_data in portfolio_problem_statements_data:
            portfolio_id = pps_data.pop("portfolio_id")
            problem_statements_ids = pps_data.pop("problem_statements")
            portfolio = Portfolio.objects.get(id=portfolio_id)
            instance.portfolios.add(portfolio)

            for ps_id in problem_statements_ids:
                problem_statement = ProblemStatement.objects.get(id=ps_id)
                instance.problem_statements.add(problem_statement)

        return instance


class ProjectVersionHistorySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    changes = serializers.SerializerMethodField()
    beyond_history = serializers.SerializerMethodField()
    was_unpublished = serializers.SerializerMethodField()

    class Meta:
        model = ProjectVersion
        fields = (
            "id",
            "version",
            "modified",
            "user",
            "changes",
            "published",
            "beyond_history",
            "was_unpublished",
        )

    def get_previous(self, obj):
        versions = list(self.instance)
        try:
            if obj.version == 1:
                return None
            elif versions.index(obj) == 0:
                return None
        except ValueError:  # pragma: no cover
            return None
        else:
            return versions[versions.index(obj) - 1]

    def get_changes(self, obj):
        previous = self.get_previous(obj)
        if not previous:
            return []
        else:
            prev = previous.data
        cur = obj.data

        if cur == prev:
            return []

        keys_added = set(cur.keys()) - set(prev.keys())
        keys_removed = set(prev.keys()) - set(cur.keys())
        keys_intersect = set(prev.keys()) & set(cur.keys())

        changes = []
        for k in keys_added:
            if (
                isinstance(cur[k], dict)
                or isinstance(cur[k], list)
                and len(cur[k]) > 0
                and (isinstance(cur[k][0], list) or isinstance(cur[k][0], dict))
            ):
                changes.append(dict(field=k, added=None, removed=None, special=True))
            else:
                changes.append(dict(field=k, added=cur[k], removed=None, special=False))

        for k in keys_removed:
            if (
                isinstance(prev[k], dict)
                or isinstance(prev[k], list)
                and len(prev[k]) > 0
                and (isinstance(prev[k][0], list) or isinstance(prev[k][0], dict))
            ):
                changes.append(dict(field=k, added=None, removed=None, special=True))
            else:
                changes.append(
                    dict(field=k, added=None, removed=prev[k], special=False)
                )

        for k in keys_intersect:
            if cur[k] != prev[k]:
                if isinstance(cur[k], list):
                    if len(cur[k]) > 0:
                        if isinstance(cur[k][0], list) or isinstance(cur[k][0], dict):
                            changes.append(
                                dict(field=k, added=None, removed=None, special=True)
                            )
                        elif isinstance(prev[k], list):
                            changes.append(
                                dict(
                                    field=k,
                                    added=list(set(cur[k]) - set(prev[k])),
                                    removed=list(set(prev[k]) - set(cur[k])),
                                    special=False,
                                )
                            )
                elif isinstance(
                    cur[k], dict
                ):  # eg: country_custom_answers, donor_custom_answers
                    changes.append(
                        dict(field=k, added=None, removed=None, special=True)
                    )
                else:
                    changes.append(
                        dict(field=k, added=cur[k], removed=prev[k], special=False)
                    )
        return changes

    def get_beyond_history(self, obj):
        first_version = list(self.instance)[0]
        inception_date = getattr(
            settings, "PROJECT_VERSIONING_INSTALLED_AT", datetime(2021, 11, 9)
        ).date()

        return (
            obj == first_version
            and obj.project.created.date() < inception_date
            and first_version.created.date() == inception_date
        )

    def get_was_unpublished(self, obj):
        previous = self.get_previous(obj)
        if not previous:
            return False
        else:
            if previous.published and not obj.published and previous.data == obj.data:
                return True
        return False
