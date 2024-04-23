from rest_framework.permissions import BasePermission
from random import randint
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

    def has_permission(self, request, view):
        return True


class IsLibrarianOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name='librarians').exists() or request.user.is_staff)


class IsBorrowerOrAdminOrLibrarian(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.borrower == request.user or request.user.is_staff or request.user.groups.filter(name='librarians').exists()

class IsRecipientOrAdminOrLibrarian(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.borrow_request.borrower == request.user or request.user.is_staff or request.user.groups.filter(name='librarians').exists()