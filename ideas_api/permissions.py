from rest_framework import permissions


class UpdateOwnUser(permissions.BasePermission):
    """Allow user to edit their own informations."""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class PostOwnIdea(permissions.BasePermission):
    """Allow user to update their own ideas."""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own ideas."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_id.id == request.user.id
