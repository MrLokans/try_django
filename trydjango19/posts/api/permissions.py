from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = 'You are not the owner of this object.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
