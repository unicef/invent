from django.contrib import admin
from django import forms
from django.contrib.admin import SimpleListFilter
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from adminsortable2.admin import SortableAdminMixin
from core.admin import AllObjectsAdmin
from .models import TechnologyPlatform, DigitalStrategy, HealthFocusArea, \
    HealthCategory, HSCChallenge, Project, HSCGroup, ProblemStatement, \
    UNICEFGoal, UNICEFResultArea, UNICEFCapabilityLevel, UNICEFCapabilityCategory, \
    UNICEFCapabilitySubCategory, UNICEFSector, RegionalPriority, HardwarePlatform, NontechPlatform, \
    PlatformFunction, Portfolio, InnovationCategory, CPD, ProjectImportV2, InnovationWay, ISC, ApprovalState, Stage, \
    Phase, ProjectVersion, Solution, CountrySolution, UserProfile
from country.models import CountryOffice
from core.utils import make_admin_list
from core.admin.custom_admin import custom_admin_site

from project.admin_filters import IsPublishedFilter, UserFilter, OverViewFilter, CountryFilter, DescriptionFilter, \
    RegionFilter

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery  # noqa

from import_export.admin import ExportActionMixin
from import_export_celery.admin_actions import create_export_job_action
from .resources import ProjectResource, ProblemStatementResource, PortfolioResource, SolutionsResource
from .utils import project_status_change, project_status_change_str


class ViewOnlyPermissionMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ViewOnlyInlineMixin:
    fields = ('name',)
    readonly_fields = ('name',)
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj):  # pragma: no cover
        return False


def approve(modeladmin, request, queryset):
    for obj in queryset:
        obj.state = ApprovalState.APPROVED
        obj.save()


approve.short_description = "Approve selected items"


def decline(modeladmin, request, queryset):
    for obj in queryset:
        obj.state = ApprovalState.DECLINED
        obj.save()


decline.short_description = "Decline selected items"


class ApprovalStateFilter(SimpleListFilter):
    title = 'State'

    parameter_name = 'state'

    def lookups(self, request, model_admin):
        return (ApprovalState.APPROVED, ApprovalState.STATES[0][1]), \
               (ApprovalState.PENDING, ApprovalState.STATES[1][1]), \
               (ApprovalState.DECLINED, ApprovalState.STATES[2][1])

    def choices(self, cl):  # pragma: no cover
        for lookup, title in self.lookup_choices:
            try:
                selected = int(self.value()) == lookup
            except TypeError:
                selected = None

            yield {
                'selected': selected,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() is None:
            self.used_parameters[self.parameter_name] = ApprovalState.PENDING
        return queryset.filter(state=self.value())


class ApprovalStateAdmin(AllObjectsAdmin):
    list_display = [
        'name', 'state', 'added_by'
    ]
    autocomplete_fields = ['added_by']
    ordering = search_fields = ['name']
    list_filter = [ApprovalStateFilter]
    actions = (approve, decline)


class TechnologyPlatformAdmin(ApprovalStateAdmin):
    pass


class HardwarePlatformAdmin(ApprovalStateAdmin):
    pass


class NontechPlatformAdmin(ApprovalStateAdmin):
    pass


class PlatformFunctionAdmin(ApprovalStateAdmin):
    pass


class ParentFilter(admin.SimpleListFilter):
    title = 'Parent Filter'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):  # pragma: no cover
        return (
            ('Parent Only', _('Parent Only')),
            ('Children Only', _('Children Only'))
        )

    def queryset(self, request, queryset):  # pragma: no cover
        if self.value() is None:
            return queryset.all()
        elif self.value() == 'Parent Only':
            return queryset.filter(parent=None)
        else:
            return queryset.exclude(parent=None)


class DigitalStrategyAdmin(ViewOnlyPermissionMixin, AllObjectsAdmin):
    list_filter = [ParentFilter]
    list_display = [
        '__str__'
    ]


class HealthFocusAreaAdmin(ViewOnlyPermissionMixin, AllObjectsAdmin):
    pass


class HealthCategoryAdmin(ViewOnlyPermissionMixin, AllObjectsAdmin):
    pass


class HSCGroupAdmin(ViewOnlyPermissionMixin, AllObjectsAdmin):
    pass


class HSCChallengeAdmin(ViewOnlyPermissionMixin, AllObjectsAdmin):
    pass


class ProjectVersionInline(admin.TabularInline):
    model = ProjectVersion
    readonly_fields = ('version', 'id', 'name', 'data', 'user', 'published')
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


class ProjectAdmin(ExportActionMixin, AllObjectsAdmin):
    create_export_job_action.short_description = _(
        "Generate export in the background")
    actions = (create_export_job_action,)
    list_display = ['__str__', 'modified', 'get_country', 'get_team', 'get_published', 'is_active', 'versions',
                    'featured', 'featured_rank']
    list_filter = ('featured', IsPublishedFilter, UserFilter, OverViewFilter, DescriptionFilter,
                   RegionFilter, CountryFilter)

    readonly_fields = ['name', 'team', 'viewers', 'link',
                       'created', 'modified', 'data', 'draft', 'versions_detailed']
    fields = ['is_active', 'featured', 'featured_rank'] + readonly_fields
    search_fields = ['name']
    resource_class = ProjectResource
    inlines = [ProjectVersionInline]

    def get_country(self, obj):
        return obj.get_country() if obj.public_id else obj.get_country(draft_mode=True)
    get_country.short_description = "Country"

    def get_team(self, obj):
        return ", ".join([str(p) for p in obj.team.all()])
    get_team.short_description = 'Team members'

    def get_published(self, obj):
        return True if obj.public_id else False
    get_published.short_description = "Is published?"
    get_published.boolean = True

    def link(self, obj):
        if obj.id is None:
            return '-'
        return mark_safe(f"<a target='_blank' href='/en/-/initiatives/{obj.id}/edit/'>Edit initiative</a>")

    def has_add_permission(self, request):
        return False

    @staticmethod
    def versions(obj):
        return ProjectVersion.objects.filter(project=obj).count()

    @staticmethod
    def versions_detailed(obj):
        results_list = list()
        prev_version = None
        for version in ProjectVersion.objects.filter(project=obj):
            if prev_version is None:
                results_list.append(
                    f'{version.version} - {version.created} - Initial version')
            else:
                status_change = project_status_change(prev_version, version)
                results_list.append(
                    f'{version.version} - {version.created} - {project_status_change_str(status_change)}')
            prev_version = version
        return '\n'.join(results_list)


class ProjectVersionAdmin(admin.ModelAdmin):
    model = ProjectVersion
    fields = ['modified', 'project', 'user', 'version', 'data', 'published']
    readonly_fields = fields
    search_fields = ['project__name']

    list_display = ['modified', 'project', 'published', 'version']

    def get_project_name(self, obj):  # pragma: no cover
        return obj.project.name

    def has_add_permission(self, request):
        return False


class ProblemStatementsInline(admin.TabularInline):
    model = ProblemStatement
    extra = 1


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'description', 'status', 'is_active',
                  'managers', 'icon', 'innovation_hub', 'landscape_review', 'investment_to_date']
        labels = {'investment_to_date': 'Cumulative investment.',
                  'landscape_review': 'Completed landscape review'}
        widgets = {'innovation_hub': forms.CheckboxInput,
                   'icon': forms.Select(choices=[(1, 'education'),
                                                 (2, 'nutrition'),
                                                 (3, 'health'),
                                                 (4, 'child_protection'),
                                                 (5, 'wash'),
                                                 (6, 'aids'),
                                                 (7, 'social_inclusion'),
                                                 (8, 'food_health'),
                                                 (9, 'affected_population'),
                                                 (10, 'children'),
                                                 (11, 'gender_balance'),
                                                 (14, 'infant'),
                                                 (15, 'breast_feeding'),
                                                 (16, 'children_with_disabilities'),
                                                 (27, 'pregnant'),
                                                 (29, 'mental_health'),
                                                 (30, 'mother_and_baby'),
                                                 (34, '5year_old_girl'),
                                                 (38, 'conflict'),
                                                 (42, 'tsunami'),
                                                 (45, 'epidemic'),
                                                 (52, 'tent'),
                                                 (69, 'medical_supplies'),
                                                 (70, 'vaccines'),
                                                 (71, 'psychosocial_support'),
                                                 (72, 'headquarters'),
                                                 (73, 'regional_office'),
                                                 (92, 'partnership'),
                                                 (97, 'advocacy'),
                                                 (113, 'innovation'),
                                                 (116, 'community_building'),
                                                 (164, 'emergency')])}


class PortfolioAdmin(ExportActionMixin, AllObjectsAdmin):
    resource_class = PortfolioResource
    list_display = ['__str__', 'description', 'status', 'landscape_review',
                    'created', 'icon', 'managers_list', 'is_active', 'innovation_hub', 'investment_to_date']
    inlines = [ProblemStatementsInline]
    form = PortfolioForm
    autocomplete_fields = ['managers']
    filter_horizontal = ['managers']

    def managers_list(self, obj):
        return make_admin_list(obj.managers.all())

    managers_list.short_description = "Assigned managers"


class ProblemStatementAdmin(ExportActionMixin, admin.ModelAdmin):
    model = ProblemStatement
    resource_class = ProblemStatementResource
    list_display = ['id', 'name', 'description', 'portfolio', 'is_active']

    def get_queryset(self, request):  # pragma: no cover
        return self.model.all_objects.all()


class ResultAreaInline(ViewOnlyInlineMixin, admin.TabularInline):
    model = UNICEFResultArea


class CapabilityLevelInline(ViewOnlyInlineMixin, admin.TabularInline):
    model = UNICEFCapabilityLevel


class CapabilityCategoryInline(ViewOnlyInlineMixin, admin.TabularInline):
    model = UNICEFCapabilityCategory


class CapabilitySubCategoryInline(ViewOnlyInlineMixin, admin.TabularInline):
    model = UNICEFCapabilitySubCategory


class UNICEFGoalAdmin(admin.ModelAdmin):
    ordering = search_fields = ['name']
    inlines = [ResultAreaInline, CapabilityLevelInline,
               CapabilityCategoryInline, CapabilitySubCategoryInline]


class UNICEFResultAreaAdmin(admin.ModelAdmin):
    ordering = search_fields = ['goal_area__name', 'name']


class UNICEFCapabilityLevelAdmin(admin.ModelAdmin):
    ordering = search_fields = ['goal_area__name', 'name']


class UNICEFCapabilityCategoryAdmin(admin.ModelAdmin):
    ordering = search_fields = ['goal_area__name', 'name']


class UNICEFCapabilitySubCategoryAdmin(admin.ModelAdmin):
    ordering = search_fields = ['goal_area__name', 'name']


class UNICEFSectorAdmin(admin.ModelAdmin):
    ordering = search_fields = ['name']


class RegionalPriorityAdmin(admin.ModelAdmin):
    ordering = search_fields = ['name']
    list_display = ['name', 'region']


class InnovationCategoryAdmin(admin.ModelAdmin):
    ordering = search_fields = ['name']


class InnovationWayAdmin(admin.ModelAdmin):
    ordering = search_fields = ['name']


class CPDAdmin(admin.ModelAdmin):
    ordering = search_fields = ['name']


class ISCAdmin(admin.ModelAdmin):
    ordering = search_fields = ['name']


class ProjectImportAdmin(admin.ModelAdmin):
    pass


class StageAdmin(SortableAdminMixin, AllObjectsAdmin):
    pass


class PhaseAdmin(ViewOnlyPermissionMixin, admin.ModelAdmin):
    ordering = search_fields = ['name']


class CountrySolutionInline(admin.TabularInline):
    model = CountrySolution
    extra = 1


class SolutionAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = SolutionsResource

    ordering = search_fields = ['name']
    list_display = ['__str__', 'portfolio_list', 'phase', 'open_source_frontier_tech',
                    'learning_investment', 'people_reached', 'list_of_countries']
    list_filter = ['portfolios',
                   'open_source_frontier_tech', 'learning_investment']
    filter_horizontal = ['portfolios', 'problem_statements']
    readonly_fields = ['people_reached', 'regions_display']
    inlines = (CountrySolutionInline,)

    def portfolio_list(self, obj):  # pragma: no cover
        return list(obj.portfolios.all())
    portfolio_list.short_description = 'Portfolios'

    def list_of_countries(self, obj):  # pragma: no cover
        countries_with_data = obj.countrysolution_set.all()
        countries_with_people_reached = ['{} - {} - {}'.format(cwd.country, CountryOffice.REGIONS[cwd.region][1],
                                                               cwd.people_reached) for cwd in countries_with_data]
        return ', '.join(countries_with_people_reached)


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['name']


custom_admin_site.register(UserProfile, UserProfileAdmin)


custom_admin_site.register(TechnologyPlatform, TechnologyPlatformAdmin)
custom_admin_site.register(DigitalStrategy, DigitalStrategyAdmin)
custom_admin_site.register(HealthFocusArea, HealthFocusAreaAdmin)
custom_admin_site.register(HealthCategory, HealthCategoryAdmin)
custom_admin_site.register(HSCGroup, HSCGroupAdmin)
custom_admin_site.register(HSCChallenge, HSCChallengeAdmin)
custom_admin_site.register(Project, ProjectAdmin)
custom_admin_site.register(ProjectVersion, ProjectVersionAdmin)
custom_admin_site.register(Portfolio, PortfolioAdmin)
custom_admin_site.register(UNICEFGoal, UNICEFGoalAdmin)
custom_admin_site.register(UNICEFResultArea, UNICEFResultAreaAdmin)
custom_admin_site.register(UNICEFCapabilityLevel, UNICEFCapabilityLevelAdmin)
custom_admin_site.register(UNICEFCapabilityCategory,
                           UNICEFCapabilityCategoryAdmin)
custom_admin_site.register(UNICEFCapabilitySubCategory,
                           UNICEFCapabilitySubCategoryAdmin)
custom_admin_site.register(UNICEFSector, UNICEFSectorAdmin)
custom_admin_site.register(RegionalPriority, RegionalPriorityAdmin)
custom_admin_site.register(HardwarePlatform, HardwarePlatformAdmin)
custom_admin_site.register(NontechPlatform, NontechPlatformAdmin)
custom_admin_site.register(PlatformFunction, PlatformFunctionAdmin)
custom_admin_site.register(InnovationWay, InnovationWayAdmin)
custom_admin_site.register(InnovationCategory, InnovationCategoryAdmin)
custom_admin_site.register(CPD, CPDAdmin)
custom_admin_site.register(ISC, ISCAdmin)
custom_admin_site.register(ProjectImportV2, ProjectImportAdmin)
custom_admin_site.register(Stage, StageAdmin)
custom_admin_site.register(Phase, PhaseAdmin)
custom_admin_site.register(ProblemStatement, ProblemStatementAdmin)
custom_admin_site.register(Solution, SolutionAdmin)
