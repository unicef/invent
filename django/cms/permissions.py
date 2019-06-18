from rest_framework import permissions

from cms.models import Post


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # TODO REVIEW THIS AND CREATE TEST, before this it was impossible to report post not 'owned'
        if request.method.lower() == 'patch':
            return True

        # Instance must have an attribute named `owner`.
        sentinel = object()
        owner = getattr(obj, 'user', sentinel)
        if owner == sentinel:
            owner = getattr(obj, 'author', False)

        return owner == request.user.userprofile


class OnlyAdminForLessons(permissions.BasePermission):
    """
    Object-level permission to only allow admins to CRUD lessons.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.type == Post.LESSON:
            return request.user.is_superuser
        return True
