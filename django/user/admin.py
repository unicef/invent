from django.contrib import admin

from .models import Organisation


class OrganisationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Organisation, OrganisationAdmin)
