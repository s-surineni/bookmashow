from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, reqest, view, obj):
        if reqest.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == reqest.user
