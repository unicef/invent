from django.contrib import admin
from django.db.models import JSONField
from jsoneditor.forms import JSONEditor

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


admin.site.register(SolutionLog, SolutionLogAdmin)
admin.site.register(CountryInclusionLog, CountryInclusionLogAdmin)
