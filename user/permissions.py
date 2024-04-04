from rest_framework import permissions


class UserIsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return request.user.pk == obj.user_pk