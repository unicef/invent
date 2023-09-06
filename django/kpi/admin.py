from django.contrib import admin
from django.db.models import JSONField
from jsoneditor.forms import JSONEditor

from core.admin.custom_admin import custom_admin_site
from .models import SolutionLog, CountryInclusionLog


class SolutionLogAdmin(admin.ModelAdmin):
    list_display = ["date", "modified"]
    formfield_overrides = {
        JSONField: {"widget": JSONEditor},
    }


class CountryInclusionLogAdmin(admin.ModelAdmin):
    list_display = ["date", "modified"]
    formfield_overrides = {
        JSONField: {"widget": JSONEditor},
    }


custom_admin_site.register(SolutionLog, SolutionLogAdmin)
custom_admin_site.register(CountryInclusionLog, CountryInclusionLogAdmin)
