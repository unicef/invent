from import_export import resources
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

from project.models import Project, UNICEFSector, UNICEFGoal, InnovationCategory, CPD, Stage, TechnologyPlatform, \
    HardwarePlatform, NontechPlatform, ISC, PlatformFunction, UNICEFResultArea, InnovationWay
from import_export.fields import Field
from django.utils.translation import ugettext_lazy as _

from country.models import Country, CountryOffice, Currency

from project.serializers import LinkSerializer, PartnerSerializer


class ProjectResource(resources.ModelResource):  # pragma: no cover
    """
    This class is basically a serializer for the django-import-export module
    TODO: write unit tests if necessary
    """
    # General Overview
    published = Field(column_name=_('Published?'))
    contact = Field(column_name=_('Contact'))
    team = Field(column_name=_('Team'))
    overview = Field(column_name=_('Overview'))
    narrative = Field(column_name=_('Narrative'))
    country = Field(column_name=_('Country'))
    unicef_office = Field(column_name=_('UNICEF Office'))

    # Categorization
    sector = Field(column_name=_('Sector'))
    goal_area = Field(column_name=_('Goal Area'))
    result_area = Field(column_name=_('Result Area'))
    innovations = Field(column_name=_('Innovation(s)'))
    innovation_categories = Field(column_name=_('Innovation category(ies)'))

    # Implementation Overview
    program_targets = Field(column_name=_('Program targets'))
    program_targets_achieved = Field(column_name=_('Program targets achieved'))
    beneficiaries_number = Field(column_name=_('Number of beneficiaries reached'))
    current_achievements = Field(column_name=_('Current achievements'))
    cpd = Field(column_name=_('Country Programme Document inclusion'))
    awp_note = Field(column_name=_('Outcome in Annual Work Plan'))
    wbs = Field(column_name=_('Work Breakdown Structure (WBS) number'))
    budget = Field(column_name=_('Budget'))
    total_budget_narrative = Field(column_name=_('Activities covered by budget'))
    funding_needs = Field(column_name=_('Funding gaps'))
    partnership_needs = Field(column_name=_('Partnership needs'))
    links = Field(column_name=_('Links'))

    # Completion of initiative phases (stages)
    stages = Field(column_name=_('Completion of initiative phases'))
    current_phase = Field(column_name=_('Current phase'))

    # Partners
    partners = Field(column_name=_('Partners'))

    # Technology
    software_platforms = Field(column_name=_('Software Platform(s)'))
    hardware_platforms = Field(column_name=_('Hardware Platform(s)'))
    nontech_platforms = Field(column_name=_('Non-technology Platform(s)'))
    platform_functions = Field(column_name=_('Platform functions'))
    isc = Field(column_name=_('Information security classification'))

    class Meta:
        model = Project
        fields = ('id', 'name', 'published', 'contact', 'team', 'modified')
        export_order = ('id', 'name', 'published', 'modified', 'contact', 'team', 'overview')

    def export_field(self, field, obj):
        data = super().export_field(field, obj)
        if isinstance(data, str):
            data = ILLEGAL_CHARACTERS_RE.sub('', data)
        return data

    def get_data_member(self, project):
        """
        shorthand for getting the data member
        """
        return project.data if project.public_id != '' else project.draft

    def dehydrate_published(self, project):
        return "True" if project.public_id != '' else "False"

    def dehydrate_contact(self, project):
        data = self.get_data_member(project)
        return f'{data.get("contact_name", "None")} <{data.get("contact_email", "None")}>'

    def dehydrate_team(self, project):
        return ", ".join([str(p) for p in project.team.all()])

    def dehydrate_overview(self, project):
        return self.get_data_member(project).get('overview', None)

    def dehydrate_narrative(self, project):
        return self.get_data_member(project).get('implementation_overview', None)

    def dehydrate_unicef_office(self, project):
        try:
            return CountryOffice.objects.get(id=self.get_data_member(project).get('country_office')).name
        except CountryOffice.DoesNotExist:
            return None

    def dehydrate_country(self, project):
        try:
            return Country.objects.get(id=self.get_data_member(project).get('country')).name
        except Country.DoesNotExist:
            return None

    def dehydrate_sector(self, project):
        sector = self.get_data_member(project).get('unicef_sector')
        qs = UNICEFSector.objects.filter(id__in=sector)
        return ", ".join(res.name for res in qs) if qs.count() else None

    def dehydrate_goal_area(self, project):
        try:
            return UNICEFGoal.objects.get(id=self.get_data_member(project).get('goal_area')).name
        except UNICEFGoal.DoesNotExist:
            return None

    def dehydrate_result_area(self, project):
        try:
            return UNICEFResultArea.objects.get(id=self.get_data_member(project).get('result_area')).name
        except UNICEFResultArea.DoesNotExist:
            return None

    def dehydrate_innovations(self, project):
        ids = self.get_data_member(project).get('innovation_ways')
        if ids:
            names = InnovationWay.objects.filter(id__in=self.get_data_member(project).get('innovation_ways')).\
                values_list('name', flat=True)
            return ', '.join(names) if names else None
        return None

    def dehydrate_innovation_categories(self, project):
        category = self.get_data_member(project).get('innovation_categories')
        qs = InnovationCategory.objects.filter(id__in=category)
        return ", ".join(res.name for res in qs) if qs.count() else None

    def dehydrate_program_targets(self, project):
        return self.get_data_member(project).get('program_targets')

    def dehydrate_program_targets_achieved(self, project):
        return self.get_data_member(project).get('program_targets_achieved')

    def dehydrate_beneficiaries_number(self, project):
        return self.get_data_member(project).get('target_group_reached', 0)

    def dehydrate_current_achievements(self, project):
        return self.get_data_member(project).get('current_achievements')

    def dehydrate_cpd(self, project):
        cpd = self.get_data_member(project).get('cpd')
        try:
            return ', '.join(CPD.objects.filter(id__in=cpd).values_list('name', flat=True))
        except CPD.DoesNotExist:
            return None

    def dehydrate_awp_note(self, project):
        return self.get_data_member(project).get('awp')

    def dehydrate_wbs(self, project):
        wbs_list = self.get_data_member(project).get('wbs')
        return ", ".join(wbs for wbs in wbs_list) if wbs_list else None

    def dehydrate_budget(self, project):
        data = self.get_data_member(project)
        try:
            currency_code = Currency.objects.get(id=data.get('currency')).code
        except Currency.DoesNotExist:
            currency_code = ""
        budget = data['total_budget'] if 'total_budget' in data else 0
        return " ".join([str(budget), currency_code])

    def dehydrate_total_budget_narrative(self, project):
        return self.get_data_member(project).get('total_budget_narrative')

    def dehydrate_funding_needs(self, project):
        return self.get_data_member(project).get('funding_needs', 0)

    def dehydrate_partnership_needs(self, project):
        return self.get_data_member(project).get('partnership_needs')

    def dehydrate_links(self, project):
        links_list = self.get_data_member(project).get('links')
        link_types = {link[0]: link[1] for link in LinkSerializer.LINK_TYPE}
        link_types[''] = "unknown"
        links = []
        for link_data in links_list:
            l_type = link_types[link_data.get("link_type", "")]
            l_url = link_data.get('link_url', "unknown")
            links.append(f'{l_type}: {l_url}')
        return ', '.join(links) if links else None

    def dehydrate_stages(self, project):
        stages = []
        start_date = self.get_data_member(project).get('start_date')
        if start_date:
            stages.append(f'Start ({start_date})')
        stages_data = self.get_data_member(project).get('stages')
        if stages_data:
            for stage in stages_data:
                try:
                    stages.append(f'{Stage.objects.get(id=stage["id"]).name} ({stage.get("date", "")})')
                except Stage.DoesNotExist:
                    continue
        end_date = self.get_data_member(project).get('end_date')
        if end_date:
            stages.append(f'End ({end_date})')
        return ', '.join(stages)

    def dehydrate_current_phase(self, project):
        stage_id = self.get_data_member(project).get('current_phase')
        try:
            return Stage.objects.get(id=stage_id).name
        except Exception:
            return _('No phase data')

    def dehydrate_partners(self, project):
        if 'partners' not in self.get_data_member(project):
            return None
        p_type_lookup = {p[0]: p[1] for p in PartnerSerializer.PARTNER_TYPE}
        partners = []
        for partner in self.get_data_member(project)['partners']:
            p_type = p_type_lookup[partner['partner_type']] if 'partner_type' in partner else "n/a"
            p_string = f'{p_type}: {partner.get("partner_name")} ({partner.get("partner_contact")} - ' \
                       f'{partner.get("partner_email")} - {partner.get("partner_website")})'
            partners.append(p_string)
        return ', '.join(partners)

    def dehydrate_software_platforms(self, project):
        ids = self.get_data_member(project).get('platforms')
        if not ids:
            return None
        qs = TechnologyPlatform.objects.filter(id__in=ids)
        return ", ".join(res.name for res in qs) if qs.count() else None

    def dehydrate_hardware_platforms(self, project):
        ids = self.get_data_member(project).get('hardware')
        if not ids:
            return None
        qs = HardwarePlatform.objects.filter(id__in=ids)
        return ", ".join(res.name for res in qs) if qs.count() else None

    def dehydrate_nontech_platforms(self, project):
        ids = self.get_data_member(project).get('nontech')
        if not ids:
            return ""
        qs = NontechPlatform.objects.filter(id__in=ids)
        return ", ".join(res.name for res in qs) if qs.count() else None

    def dehydrate_platform_functions(self, project):
        ids = self.get_data_member(project).get('functions')
        if not ids:
            return ""
        qs = PlatformFunction.objects.filter(id__in=ids)
        return ", ".join(res.name for res in qs) if qs.count() else None

    def dehydrate_isc(self, project):
        id = self.get_data_member(project).get('isc')
        if not id:
            return None
        try:
            return ISC.objects.get(id=id).name
        except ISC.DoesNotExist:
            return None
