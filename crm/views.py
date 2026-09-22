from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Max, Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access import admin_required, crm_required, is_admin, is_internal_user
from .forms import ClienteForm, InteraccionForm, UsuarioForm
from .models import Cliente, Interaccion


def _metrics():
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    total = Cliente.objects.count()
    active = Cliente.objects.filter(estado='ACTIVO').count()
    risk = Cliente.objects.annotate(last=Max('interacciones__fecha')).filter(
        Q(last__isnull=True) | Q(last__lt=now - timedelta(days=30))
    ).count()
    return {
        'total_clientes': total, 'clientes_activos': active,
        'clientes_inactivos': Cliente.objects.filter(estado='INACTIVO').count(),
        'prospectos': Cliente.objects.filter(etapa_crm='PROSPECTO').count(),
        'clientes_frecuentes': Cliente.objects.filter(etapa_crm='FRECUENTE').count(),
        'interacciones_totales': Interaccion.objects.count(),
        'interacciones_mes': Interaccion.objects.filter(fecha__gte=month_start).count(),
        'interacciones': Interaccion.objects.filter(fecha__gte=month_start).count(),
        'clientes_en_riesgo': risk,
        'porcentaje_activos': round(active * 100 / total) if total else 0,
        'clientes_por_etapa': list(Cliente.objects.values('etapa_crm').annotate(total=Count('id')).order_by('-total')),
    }


def login_view(request):
    if request.user.is_authenticated and is_internal_user(request.user):
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username', '').strip(), password=request.POST.get('password', ''))
        if user and is_internal_user(user):
            login(request, user)
            return redirect(request.POST.get('next') or 'dashboard')
        messages.error(request, 'Credenciales inválidas o sin acceso al CRM.')
    return render(request, 'crm/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('core_login')


@crm_required
def dashboard_view(request):
    return render(request, 'crm/dashboard.html', _metrics())


@crm_required
def clientes_view(request):
    clients = Cliente.objects.all().order_by('-fecha_registro')
    search, stage, state = request.GET.get('busqueda', '').strip(), request.GET.get('etapa', ''), request.GET.get('estado', '')
    if search:
        clients = clients.filter(Q(nombre__icontains=search) | Q(correo__icontains=search) | Q(telefono__icontains=search))
    if stage:
        clients = clients.filter(etapa_crm=stage)
    if state:
        clients = clients.filter(estado=state)
    return render(request, 'crm/clientes.html', {'clientes': clients, 'busqueda': search, 'etapa_seleccionada': stage, 'estado_seleccionado': state, 'etapas': Cliente.ETAPAS, 'estados': Cliente.ESTADOS})


@crm_required
def detalle_cliente_view(request, cliente_id):
    client = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'crm/detalle_cliente.html', {'cliente': client, 'interacciones': client.interacciones.select_related('usuario').order_by('-fecha')})


@admin_required
def nuevo_cliente_view(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cliente creado correctamente.')
        return redirect('clientes')
    return render(request, 'crm/nuevo_cliente.html', {'form': form})


@admin_required
def editar_cliente_view(request, cliente_id):
    client = get_object_or_404(Cliente, id=cliente_id)
    form = ClienteForm(request.POST or None, instance=client)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cliente actualizado correctamente.')
        return redirect('detalle_cliente', cliente_id=client.id)
    return render(request, 'crm/editar_cliente.html', {'form': form, 'cliente': client})


@admin_required
def eliminar_cliente_view(request, cliente_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    get_object_or_404(Cliente, id=cliente_id).delete()
    messages.success(request, 'Cliente eliminado correctamente.')
    return redirect('clientes')


@crm_required
def nueva_interaccion_view(request, cliente_id=None):
    client_id = cliente_id or request.GET.get('cliente') or request.POST.get('cliente')
    client = get_object_or_404(Cliente, id=client_id) if client_id else None
    form = InteraccionForm(request.POST or None, initial={'cliente': client})
    if request.method == 'POST' and form.is_valid():
        interaction = form.save(commit=False)
        interaction.usuario = request.user
        interaction.save()
        messages.success(request, 'Interacción registrada correctamente.')
        return redirect('detalle_cliente', cliente_id=interaction.cliente_id)
    return render(request, 'crm/nueva_interaccion.html', {'form': form, 'cliente_preseleccionado': client})


@crm_required
def mi_actividad_view(request):
    interactions = Interaccion.objects.filter(usuario=request.user).select_related('cliente').order_by('-fecha')
    return render(request, 'crm/mi_actividad.html', {'interacciones': interactions, 'total_interacciones': interactions.count()})


@crm_required
def reportes_metricas_view(request):
    return render(request, 'crm/reportes_metricas.html', _metrics())


def _role(user):
    return 'admin' if user.groups.filter(name='admin').exists() else 'empleado'


def _can_manage(actor, target=None, requested_role=None):
    if actor.is_superuser:
        return True
    return is_admin(actor) and requested_role != 'admin' and (target is None or not target.is_superuser and not target.groups.filter(name='admin').exists())


@admin_required
def usuarios_view(request):
    users = User.objects.filter(Q(is_superuser=True) | Q(groups__name__in=('admin', 'empleado'))).distinct().prefetch_related('groups').order_by('id')
    for user in users:
        user.crm_role = 'Superusuario' if user.is_superuser else ('Administrador' if user.groups.filter(name='admin').exists() else 'Empleado')
    return render(request, 'crm/usuarios.html', {'usuarios': users, 'total_usuarios': users.count(), 'usuarios_activos': users.filter(is_active=True).count(), 'usuarios_inactivos': users.filter(is_active=False).count(), 'administradores': users.filter(Q(is_superuser=True) | Q(groups__name='admin')).distinct().count()})


@admin_required
def nuevo_usuario_view(request):
    roles = ('admin', 'empleado') if request.user.is_superuser else ('empleado',)
    form = UsuarioForm(request.POST or None, allowed_roles=roles)
    if request.method == 'POST' and form.is_valid():
        if not _can_manage(request.user, requested_role=form.cleaned_data['rol']):
            raise PermissionDenied('No puedes crear administradores.')
        form.save()
        messages.success(request, 'Usuario creado correctamente.')
        return redirect('usuarios')
    return render(request, 'crm/nuevo_usuario.html', {'form': form})


@admin_required
def editar_usuario_view(request, usuario_id):
    user = get_object_or_404(User, id=usuario_id)
    if not _can_manage(request.user, target=user):
        raise PermissionDenied('No puedes modificar este usuario.')
    roles = ('admin', 'empleado') if request.user.is_superuser else ('empleado',)
    form = UsuarioForm(request.POST or None, instance=user, allowed_roles=roles)
    if request.method == 'POST' and form.is_valid():
        if not _can_manage(request.user, user, form.cleaned_data['rol']):
            raise PermissionDenied('No puedes asignar ese rol.')
        form.save()
        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect('usuarios')
    return render(request, 'crm/editar_usuario.html', {'form': form, 'usuario': user})


@admin_required
def eliminar_usuario_view(request, usuario_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    user = get_object_or_404(User, id=usuario_id)
    if user == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
    elif not _can_manage(request.user, target=user):
        raise PermissionDenied('No puedes eliminar este usuario.')
    else:
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('usuarios')


@crm_required
def perfil_view(request):
    return render(request, 'crm/perfil.html', {'usuario': request.user})


@crm_required
def editar_perfil_view(request):
    form = UsuarioForm(request.POST or None, instance=request.user, include_role=False, include_active=False)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tu perfil fue actualizado correctamente.')
        return redirect('perfil')
    return render(request, 'crm/editar_perfil.html', {'form': form})
