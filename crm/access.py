from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def is_admin(user):
    return bool(user.is_authenticated and (
        user.is_superuser or user.groups.filter(name='admin').exists()
    ))


def is_internal_user(user):
    return bool(user.is_authenticated and (
        user.is_superuser or user.groups.filter(name__in=('admin', 'empleado')).exists()
    ))


def crm_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=' + request.get_full_path())
        if not is_internal_user(request.user):
            raise PermissionDenied('No tienes acceso al CRM.')
        return view(request, *args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=' + request.get_full_path())
        if not is_admin(request.user):
            raise PermissionDenied('No tienes permisos administrativos.')
        return view(request, *args, **kwargs)
    return wrapped
