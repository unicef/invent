from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Organisation


@admin.register(Organisation)
class OrganisationAdmin(ModelAdmin):
    pass
