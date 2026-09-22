from rest_framework.permissions import BasePermission
from .access import is_admin, is_internal_user


class EsAdminOEmpleado(BasePermission):
    def has_permission(self, request, view):
        return is_internal_user(request.user)


class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_admin(request.user)


class EsAdminOEmpleadoSinEliminar(BasePermission):
    def has_permission(self, request, view):
        if not is_internal_user(request.user):
            return False
        if is_admin(request.user):
            return True
        return request.method != 'DELETE'
