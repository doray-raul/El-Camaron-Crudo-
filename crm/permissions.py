from rest_framework.permissions import BasePermission


class EsAdminOEmpleado(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(
                name__in=['admin', 'empleado']
            ).exists()
        )


class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='admin').exists()
        )


class EsAdminOEmpleadoSinEliminar(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name='admin').exists():
            return True

        if request.user.groups.filter(name='empleado').exists():
            return request.method != 'DELETE'

        return False