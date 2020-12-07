from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from core.admin import AllObjectsAdmin
from country.models import Country
from .models import TechnologyPlatform, DigitalStrategy, HealthFocusArea, \
    HealthCategory, HSCChallenge, Project, HSCGroup, \
    UNICEFGoal, UNICEFResultArea, UNICEFCapabilityLevel, UNICEFCapabilityCategory, \
    UNICEFCapabilitySubCategory, UNICEFSector, RegionalPriority, Phase, HardwarePlatform, NontechPlatform, \
    PlatformFunction, Portfolio, InnovationCategory, CPD, ProjectImportV2, InnovationWay, ISC, ApprovalState
from core.utils import make_admin_list

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery # noqa


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


class ProjectAdmin(AllObjectsAdmin):
    list_display = ['__str__', 'created', 'get_country', 'get_team', 'get_published', 'is_active']
    readonly_fields = ['name', 'team', 'viewers', 'link', 'odk_etag', 'odk_id', 'odk_extra_data']
    fields = ['is_active', 'name', 'team', 'viewers', 'link', 'odk_etag', 'odk_id', 'odk_extra_data']
    search_fields = ['name']

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
        version = 'publish' if obj.public_id else 'draft'
        return mark_safe("<a target='_blank' href='/app/{}/edit-project/{}/'>See project</a>"
                         .format(obj.id, version))

    def get_queryset(self, request):
        qs = super(ProjectAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            country_id_qs = Country.objects.filter(users=request.user.userprofile).values_list('id', flat=True)
            qs = qs.filter(Q(data__country__contained_by=list(country_id_qs)) |
                           Q(draft__country__contained_by=list(country_id_qs)))
        return qs

    def has_add_permission(self, request):
        return False


class PortfolioAdmin(AllObjectsAdmin):
    list_display = ['__str__', 'description', 'status', 'created', 'icon', 'managers_list', 'is_active']
    fields = ['name', 'description', 'status', 'managers', 'icon', 'is_active']

    def managers_list(self, obj):
        return make_admin_list(obj.managers.all())

    managers_list.short_description = "Assigned managers"


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
    inlines = [ResultAreaInline, CapabilityLevelInline, CapabilityCategoryInline, CapabilitySubCategoryInline]


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


class PhaseAdmin(admin.ModelAdmin):
    ordering = search_fields = ['name']


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


admin.site.register(TechnologyPlatform, TechnologyPlatformAdmin)
admin.site.register(DigitalStrategy, DigitalStrategyAdmin)
admin.site.register(HealthFocusArea, HealthFocusAreaAdmin)
admin.site.register(HealthCategory, HealthCategoryAdmin)
admin.site.register(HSCGroup, HSCGroupAdmin)
admin.site.register(HSCChallenge, HSCChallengeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(UNICEFGoal, UNICEFGoalAdmin)
admin.site.register(UNICEFResultArea, UNICEFResultAreaAdmin)
admin.site.register(UNICEFCapabilityLevel, UNICEFCapabilityLevelAdmin)
admin.site.register(UNICEFCapabilityCategory, UNICEFCapabilityCategoryAdmin)
admin.site.register(UNICEFCapabilitySubCategory, UNICEFCapabilitySubCategoryAdmin)
admin.site.register(UNICEFSector, UNICEFSectorAdmin)
admin.site.register(RegionalPriority, RegionalPriorityAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(HardwarePlatform, HardwarePlatformAdmin)
admin.site.register(NontechPlatform, NontechPlatformAdmin)
admin.site.register(PlatformFunction, PlatformFunctionAdmin)
admin.site.register(InnovationWay, InnovationWayAdmin)
admin.site.register(InnovationCategory, InnovationCategoryAdmin)
admin.site.register(CPD, CPDAdmin)
admin.site.register(ISC, ISCAdmin)
admin.site.register(ProjectImportV2, ProjectImportAdmin)
