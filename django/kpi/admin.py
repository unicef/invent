from django.db.models import JSONField
from jsoneditor.forms import JSONEditor
from django.contrib import admin

from .models import SolutionLog, CountryInclusionLog


@admin.register(SolutionLog)
class SolutionLogAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'modified'
    ]
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }


@admin.register(CountryInclusionLog)
class CountryInclusionLogAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'modified'
    ]
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
