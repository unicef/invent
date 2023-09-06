from django.contrib import admin

from core.admin.custom_admin import custom_admin_site
from .models import Organisation


class OrganisationAdmin(admin.ModelAdmin):
    pass


custom_admin_site.register(Organisation, OrganisationAdmin)
