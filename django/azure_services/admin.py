from django.contrib import admin
from .models import DeltaLink

class DeltaLinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'created')

admin.site.register(DeltaLink, DeltaLinkAdmin)
