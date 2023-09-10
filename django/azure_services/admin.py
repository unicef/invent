from django.contrib import admin

from core.admin.custom_admin import custom_admin_site
from .models import DeltaLink


class DeltaLinkAdmin(admin.ModelAdmin):
    list_display = ("url", "created")


custom_admin_site.register(DeltaLink, DeltaLinkAdmin)
