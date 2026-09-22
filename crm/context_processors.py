from .access import is_admin, is_internal_user


def crm_roles(request):
    return {
        'crm_is_admin': is_admin(request.user),
        'crm_is_internal': is_internal_user(request.user),
    }
