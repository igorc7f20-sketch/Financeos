from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Object-level permission: Only the owner of an object can access it.
    The object must have a 'user' attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
