from rest_framework.permissions import BasePermission, SAFE_METHODS
from config.settings import GENERAL_USER, BUSINESS_USER


class IsQualified(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.first_name)


class IsGeneralUser(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.type == GENERAL_USER)


class IsPublicPlace(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.type == BUSINESS_USER)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS) or
            (request.user.is_authenticated and request.user.is_staff and request.user.first_name)
        )
