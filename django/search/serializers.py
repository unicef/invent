from rest_framework import serializers

from project.models import ProjectPortfolioState
from project.serializers import ProjectPortfolioStateSerializer, ProjectPortfolioStateManagerSerializer


class MapResultSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField(source="project_id")
    name = serializers.ReadOnlyField(source="project.name")
    organisation = serializers.ReadOnlyField(source="organisation_id")
    country = serializers.ReadOnlyField(source="country_id")
    country_office = serializers.ReadOnlyField(source="country_office_id")
    approved = serializers.ReadOnlyField(source="project.approval.approved")


class ListResultSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField(source="project_id")
    name = serializers.ReadOnlyField(source="project__name")
    modified = serializers.ReadOnlyField(source="project__modified")
    organisation = serializers.ReadOnlyField(source="organisation_id")
    country = serializers.ReadOnlyField(source="country_id")
    country_office = serializers.ReadOnlyField(source="country_office_id")
    implementation_overview = serializers.ReadOnlyField(source="project__data__implementation_overview")
    contact_name = serializers.ReadOnlyField(source="project__data__contact_name")
    contact_email = serializers.ReadOnlyField(source="project__data__contact_email")
    platforms = serializers.ReadOnlyField(source="project__data__platforms")
    health_focus_areas = serializers.ReadOnlyField(source="project__data__health_focus_areas")
    hsc_challenges = serializers.ReadOnlyField(source="project__data__hsc_challenges")
    region = serializers.ReadOnlyField(source="country_office__region")
    donors = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField(source="project__approval__approved")
    country_custom_answers = serializers.ReadOnlyField(source="project__data__country_custom_answers")
    country_custom_answers_private = serializers.ReadOnlyField(source="project__data__country_custom_answers_private")
    donor_custom_answers = serializers.ReadOnlyField(source="project__data__donor_custom_answers")
    donor_custom_answers_private = serializers.SerializerMethodField()
    # UNICEF FIELDS
    goal_area = serializers.ReadOnlyField(source="project__data__goal_area")
    result_area = serializers.ReadOnlyField(source="project__data__result_area")
    field_office = serializers.ReadOnlyField(source="project__data__field_office")
    capability_levels = serializers.ReadOnlyField(source="project__data__capability_levels")
    capability_categories = serializers.ReadOnlyField(source="project__data__capability_categories")
    capability_subcategories = serializers.ReadOnlyField(source="project__data__capability_subcategories")
    innovation_categories = serializers.ReadOnlyField(source="project__data__innovation_categories")

    def get_donor_custom_answers_private(self, obj):
        private_fields = obj.get("project__data__donor_custom_answers_private")
        if private_fields and self.context['donor']:
            return {donor_id: private_fields[donor_id]
                    for donor_id in private_fields if donor_id == str(self.context['donor'].id)}


class PortfolioResultSerializer(ListResultSerializer):
    portfolio = serializers.ReadOnlyField(source="project__review_states__portfolio")
    portfolio_name = serializers.ReadOnlyField(source="project__review_states__portfolio__name")
    scale_phase = serializers.ReadOnlyField(source="project__review_states__scale_phase")


class PortfolioReviewSerializer(PortfolioResultSerializer):
    review_states = serializers.SerializerMethodField()

    def get_review_states(self, obj):
        try:
            pps = ProjectPortfolioState.objects.get(id=obj.get('project__review_states__id'))
        except ProjectPortfolioState.DoesNotExist:  # pragma: no cover
            return
        else:
            return ProjectPortfolioStateSerializer(pps).data
