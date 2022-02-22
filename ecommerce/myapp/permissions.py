# from rest_framework import permissions
#
#
# class IsStoreOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         # Write permissions are only allowed to the owner of the snippet.
#         return obj.user == request.user

from rest_framework import permissions


class IsStoreOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.groups)
        if request.user and request.user.groups.filter(name='StoreOwner'):
            return True
        return False


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
