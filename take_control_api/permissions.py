from rest_framework import permissions


class OwnerOnly(permissions.BasePermission):
    """
    Overrides the base permission and checks that the user is the owner
    of the object. If not permission will be denied.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
