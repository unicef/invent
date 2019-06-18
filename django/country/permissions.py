from rest_framework import permissions

from .models import Country, Donor


class InAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser \
            or obj.admins.filter(id=request.user.userprofile.id).exists() \
            or obj.super_admins.filter(id=request.user.userprofile.id).exists()


class InSuperAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        else:
            return obj.super_admins.filter(id=request.user.userprofile.id).exists()


class InCountryAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.is_superuser:
                return True
            country = request.data.get('country')
            return Country.objects.get(pk=country).admins.filter(id=request.user.userprofile.id).exists()
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser \
            or obj.country.admins.filter(id=request.user.userprofile.id).exists()


class InCountrySuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.is_superuser:
                return True
            country = request.data.get('country')
            return Country.objects.get(pk=country).super_admins.filter(id=request.user.userprofile.id).exists()
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        else:
            return obj.country.super_admins.filter(id=request.user.userprofile.id).exists()


class InDonorSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.is_superuser:
                return True
            donor = request.data.get('donor')
            return Donor.objects.get(pk=donor).super_admins.filter(id=request.user.userprofile.id).exists()
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        else:
            return obj.donor.super_admins.filter(id=request.user.userprofile.id).exists()
