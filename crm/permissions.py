from rest_framework.permissions import BasePermission


class EsAdminOEmpleado(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.groups.filter(name__in=['admin', 'empleado']).exists()
            )
        )


class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.groups.filter(name='admin').exists()
            )
        )


class EsAdminOEmpleadoSinEliminar(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        if request.user.groups.filter(name='empleado').exists():
            return request.method != 'DELETE'

        return False
