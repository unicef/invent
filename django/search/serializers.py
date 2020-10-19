from rest_framework import serializers

from project.serializers import ProjectPortfolioStateManagerSerializer


class MapResultSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField(source="project_id")
    name = serializers.ReadOnlyField(source="project.name")
    organisation = serializers.ReadOnlyField(source="organisation_id")
    country = serializers.ReadOnlyField(source="country_id")
    country_office = serializers.ReadOnlyField(source="country_office_id")
    approved = serializers.ReadOnlyField(source="project.approval.approved")


class ListResultSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField(source="project_id")
    name = serializers.ReadOnlyField(source="project.name")
    modified = serializers.ReadOnlyField(source="project.modified")
    organisation = serializers.ReadOnlyField(source="organisation_id")
    country = serializers.ReadOnlyField(source="country_id")
    country_office = serializers.ReadOnlyField(source="country_office_id")
    implementation_overview = serializers.ReadOnlyField(source="project.data.implementation_overview")
    contact_name = serializers.ReadOnlyField(source="project.data.contact_name")
    contact_email = serializers.ReadOnlyField(source="project.data.contact_email")
    platforms = serializers.ReadOnlyField(source="project.data.platforms")
    health_focus_areas = serializers.ReadOnlyField(source="project.data.health_focus_areas")
    hsc_challenges = serializers.ReadOnlyField(source="project.data.hsc_challenges")
    region = serializers.ReadOnlyField(source="country_office.region")
    donors = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField(source="project.approval.approved")
    country_custom_answers = serializers.SerializerMethodField()
    country_custom_answers_private = serializers.SerializerMethodField()
    donor_custom_answers = serializers.SerializerMethodField()
    donor_custom_answers_private = serializers.SerializerMethodField()
    # UNICEF FIELDS
    goal_area = serializers.ReadOnlyField(source="project.data.goal_area")
    result_area = serializers.ReadOnlyField(source="project.data.result_area")
    field_office = serializers.ReadOnlyField(source="project.data.field_office")
    capability_levels = serializers.ReadOnlyField(source="project.data.capability_levels")
    capability_categories = serializers.ReadOnlyField(source="project.data.capability_categories")
    capability_subcategories = serializers.ReadOnlyField(source="project.data.capability_subcategories")
    innovation_categories = serializers.ReadOnlyField(source="project.data.innovation_categories")

    def get_country_custom_answers(self, obj):
        if self.context.get('has_country_permission'):
            return obj.project.data.get('country_custom_answers')

    def get_country_custom_answers_private(self, obj):
        if self.context.get('has_country_permission'):
            return obj.project.data.get('country_custom_answers_private')

    def get_donor_custom_answers(self, obj):
        if self.context.get('has_donor_permission'):
            return obj.project.data.get('donor_custom_answers')

    def get_donor_custom_answers_private(self, obj):
        if self.context.get('has_donor_permission'):
            private_fields = obj.project.data.get('donor_custom_answers_private')
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
