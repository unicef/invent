from django.contrib import admin


class CustomAdminSite(admin.AdminSite):
    enable_nav_sidebar = False  # Disables the navigation sidebar

custom_admin_site = CustomAdminSite(name='custom_admin_site')
