from rest_framework import serializers

from project.models import Portfolio
from project.serializers import ProjectPortfolioStateManagerSerializer, PartnerSerializer, LinkSerializer

from project.models import CPD
from country.models import Currency


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
    capability_levels = serializers.ReadOnlyField(source="project.data.capability_levels")
    capability_categories = serializers.ReadOnlyField(source="project.data.capability_categories")
    capability_subcategories = serializers.ReadOnlyField(source="project.data.capability_subcategories")
    innovation_categories = serializers.ReadOnlyField(source="project.data.innovation_categories")
    innovation_ways = serializers.ReadOnlyField()
    unicef_sector = serializers.ReadOnlyField()
    unicef_leading_sector = serializers.ReadOnlyField()
    unicef_supporting_sectors = serializers.ReadOnlyField()
    hardware = serializers.ReadOnlyField()
    nontech = serializers.ReadOnlyField()
    functions = serializers.ReadOnlyField()
    isc = serializers.ReadOnlyField(source="project.data.isc")
    regional_priorities = serializers.ReadOnlyField()
    regional_office = serializers.ReadOnlyField(source='country_office.regional_office.id')
    stages = serializers.ReadOnlyField(source="project.data.stages")
    current_phase = serializers.ReadOnlyField(source="project.data.current_phase")
    start_date = serializers.ReadOnlyField(source="project.data.start_date")
    end_date = serializers.ReadOnlyField(source="project.data.end_date")
    target_group_reached = serializers.ReadOnlyField(source="project.data.target_group_reached")
    program_targets = serializers.ReadOnlyField(source="project.data.program_targets")
    program_targets_achieved = serializers.ReadOnlyField(source="project.data.program_targets_achieved")
    awp = serializers.ReadOnlyField(source="project.data.awp")
    currency = serializers.SerializerMethodField()
    current_achievements = serializers.ReadOnlyField(source="project.data.current_achievements")
    funding_needs = serializers.ReadOnlyField(source="project.data.funding_needs")
    cpd = serializers.SerializerMethodField()
    overview = serializers.ReadOnlyField(source="project.data.overview")
    links = serializers.SerializerMethodField()
    partners = serializers.SerializerMethodField()
    partnership_needs = serializers.ReadOnlyField(source="project.data.partnership_needs")
    total_budget = serializers.ReadOnlyField(source="project.data.total_budget")
    total_budget_narrative = serializers.ReadOnlyField(source="project.data.total_budget_narrative")
    wbs = serializers.ReadOnlyField(source="project.data.wbs")

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

    def get_currency(self, obj):  # pragma: no cover
        if 'currency' in obj.project.data:
            try:
                return Currency.objects.get(id=obj.project.data.get('currency')).name
            except Currency.DoesNotExist:
                pass

    def get_cpd(self, obj):
        if 'cpd' in obj.project.data:
            return CPD.objects.filter(id__in=obj.project.data.get('cpd')).values_list('name', flat=True)

    def get_links(self, obj):
        if obj.project.data.get('links'):
            return [f"{LinkSerializer.LINK_TYPE[x['link_type']][1]}: {x.get('link_url')}"
                    for x in obj.project.data.get('links') if x.get('link_url')]

    def get_partners(self, obj):
        partners_list = []
        if obj.project.data.get('partners'):
            for p in obj.project.data.get('partners'):
                data = [str(PartnerSerializer.PARTNER_TYPE[p.pop('partner_type')][1])]
                data.extend(p.values())
                partners_list.append(", ".join(data))
        return partners_list


class PortfolioResultSerializer(ListResultSerializer):
    portfolio = serializers.SerializerMethodField()
    review_states = serializers.SerializerMethodField()

    def get_portfolio(self, obj):
        return int(self.context['portfolio_id'])

    def get_review_states(self, obj):
        profile = self.context.get('profile')
        if self.context.get('portfolio_page') in ['review', 'portfolio'] \
                and profile \
                and (profile.global_portfolio_owner
                     or Portfolio.objects.get(id=self.context['portfolio_id']).managers.filter(id=profile.id)):
            return ProjectPortfolioStateManagerSerializer(
                obj.project.review_states.get(portfolio_id=self.context['portfolio_id'])
            ).data
