from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from cms.models import Post, State, Comment


def ban(modeladmin, request, queryset):
    queryset.update(state=State.BANNED)


ban.short_description = "Ban selected items"


def normalize(modeladmin, request, queryset):
    queryset.update(state=State.NORMAL)


normalize.short_description = "Mark selected items as normal"


class StateFilter(SimpleListFilter):
    title = 'State'

    parameter_name = 'state'

    def lookups(self, request, model_admin):
        return ((0, "All"),) + State.STATE_CHOICES

    def choices(self, cl):  # pragma: no cover
        for lookup, title in self.lookup_choices:
            try:
                selected = int(self.value()) == lookup
            except TypeError:
                selected = State.FLAGGED == lookup

            yield {
                'selected': selected,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() and int(self.value()) in (State.NORMAL, State.BANNED, State.FLAGGED):
            return queryset.filter(state=self.value())
        elif self.value() is not None and int(self.value()) == 0:
            return queryset
        else:
            return queryset.filter(state=State.FLAGGED)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('body', 'name', 'type', 'domain', 'state', 'modified', 'author')
    list_filter = (StateFilter, 'type')
    search_fields = ('name', 'body', 'author__name', 'author__user__email')
    ordering = ('name',)
    actions = (ban, normalize)

    def has_add_permission(self, request):
        return False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'state', 'modified')
    list_filter = (StateFilter,)
    search_fields = ('text', 'user__name', 'user__user__email')
    ordering = ('text',)
    actions = (ban, normalize)

    def has_add_permission(self, request):
        return False
