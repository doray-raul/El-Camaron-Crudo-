from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Max, Count
from django.utils import timezone

from .models import Cliente, Interaccion
from .forms import ClienteForm, UsuarioForm


def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=correo,
            password=password
        )

        if usuario is not None:
            login(request, usuario)
            return redirect('dashboard')

        messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'crm/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def dashboard_view(request):
    total_clientes = Cliente.objects.count()

    clientes_activos = Cliente.objects.filter(
        estado='ACTIVO'
    ).count()

    ahora = timezone.now()

    inicio_mes = ahora.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    interacciones = Interaccion.objects.filter(
        fecha__gte=inicio_mes
    ).count()

    fecha_limite = ahora - timedelta(days=30)

    clientes_con_ultima_interaccion = Cliente.objects.annotate(
        ultima_interaccion=Max('interacciones__fecha')
    )

    clientes_en_riesgo = clientes_con_ultima_interaccion.filter(
        Q(ultima_interaccion__isnull=True) |
        Q(ultima_interaccion__lt=fecha_limite)
    ).count()

    porcentaje_activos = (
        round((clientes_activos / total_clientes) * 100)
        if total_clientes > 0
        else 0
    )

    clientes_por_etapa = Cliente.objects.values(
        'etapa_crm'
        ).annotate(
            total=Count('id')
        ).order_by('-total')

    context = {
        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
        'interacciones': interacciones,
        'clientes_en_riesgo': clientes_en_riesgo,
        'porcentaje_activos': porcentaje_activos,
        'clientes_por_etapa': list(clientes_por_etapa),
    }

    return render(request, 'crm/dashboard.html', context)


@login_required(login_url='/login/')
def clientes_view(request):
    clientes = Cliente.objects.all()

    busqueda = request.GET.get('busqueda', '').strip()

    if busqueda:
        clientes = clientes.filter(
            Q(nombre__icontains=busqueda) |
            Q(correo__icontains=busqueda) |
            Q(telefono__icontains=busqueda)
        )

    etapa = request.GET.get('etapa', '')

    if etapa:
        clientes = clientes.filter(etapa_crm=etapa)

    estado = request.GET.get('estado', '')

    if estado:
        clientes = clientes.filter(estado=estado)

    context = {
        'clientes': clientes,
        'busqueda': busqueda,
        'etapa_seleccionada': etapa,
        'estado_seleccionado': estado,
    }

    return render(request, 'crm/clientes.html', context)


@login_required(login_url='/login/')
def detalle_cliente_view(request, cliente_id):
    cliente = get_object_or_404(
        Cliente,
        id=cliente_id
    )

    interacciones = Interaccion.objects.filter(
        cliente=cliente
    ).select_related(
        'usuario'
    ).order_by('-fecha')

    context = {
        'cliente': cliente,
        'interacciones': interacciones,
    }

    return render(
        request,
        'crm/detalle_cliente.html',
        context
    )

@login_required(login_url='/login/')
def nuevo_cliente_view(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()

    return render(
        request,
        'crm/nuevo_cliente.html',
        {'form': form}
    )


@login_required(login_url='/login/')
def editar_cliente_view(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(
            request,
            'No tienes permisos para editar clientes.'
        )
        return redirect('detalle_cliente', cliente_id=cliente.id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Cliente actualizado correctamente.'
            )
            return redirect(
                'detalle_cliente',
                cliente_id=cliente.id
            )
    else:
        form = ClienteForm(instance=cliente)

    return render(
        request,
        'crm/editar_cliente.html',
        {
            'form': form,
            'cliente': cliente,
        }
    )
    
    
@login_required(login_url='/login/')
def mi_actividad_view(request):
    interacciones = Interaccion.objects.all().select_related(
        'cliente',
        'usuario'
    ).order_by('-fecha')

    context = {
        'interacciones': interacciones,
        'total_interacciones': interacciones.count(),
    }

    return render(
        request,
        'crm/mi_actividad.html',
        context
    )

@login_required(login_url='/login/')
def reportes_metricas_view(request):
    ahora = timezone.now()
    fecha_limite = ahora - timedelta(days=30)

    total_clientes = Cliente.objects.count()

    clientes_activos = Cliente.objects.filter(
        estado='ACTIVO'
    ).count()

    clientes_inactivos = Cliente.objects.filter(
        estado='INACTIVO'
    ).count()

    prospectos = Cliente.objects.filter(
        etapa_crm='PROSPECTO'
    ).count()

    clientes_frecuentes = Cliente.objects.filter(
        etapa_crm='FRECUENTE'
    ).count()

    interacciones_totales = Interaccion.objects.count()

    interacciones_mes = Interaccion.objects.filter(
        fecha__gte=ahora.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
    ).count()

    clientes_con_ultima_interaccion = Cliente.objects.annotate(
        ultima_interaccion=Max('interacciones__fecha')
    )

    clientes_en_riesgo = clientes_con_ultima_interaccion.filter(
        Q(ultima_interaccion__isnull=True) |
        Q(ultima_interaccion__lt=fecha_limite)
    ).count()

    clientes_por_etapa = Cliente.objects.values(
        'etapa_crm'
    ).annotate(
        total=Count('id')
    ).order_by('-total')

    context = {
        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos,
        'prospectos': prospectos,
        'clientes_frecuentes': clientes_frecuentes,
        'interacciones_totales': interacciones_totales,
        'interacciones_mes': interacciones_mes,
        'clientes_en_riesgo': clientes_en_riesgo,
        'clientes_por_etapa': clientes_por_etapa,
    }

    return render(
        request,
        'crm/reportes_metricas.html',
        context
    )
    
@login_required(login_url='/login/')
@login_required(login_url='/login/')
def usuarios_view(request):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(
            request,
            'No tienes permisos para acceder a esta sección.'
        )
        return redirect('dashboard')

    usuarios = User.objects.all().order_by('id')

    total_usuarios = User.objects.count()
    usuarios_activos = User.objects.filter(is_active=True).count()
    usuarios_inactivos = User.objects.filter(is_active=False).count()
    administradores = User.objects.filter(is_staff=True).count()

    context = {
        'usuarios': usuarios,
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'usuarios_inactivos': usuarios_inactivos,
        'administradores': administradores,
    }

    return render(
        request,
        'crm/usuarios.html',
        context
    )


@login_required(login_url='/login/')
def nuevo_usuario_view(request):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para crear usuarios.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Usuario creado correctamente.'
            )
        return redirect('usuarios')
    else:
        form = UsuarioForm()

    return render(
        request,
        'crm/nuevo_usuario.html',
        {'form': form}
    )


@login_required(login_url='/login/')
def editar_usuario_view(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)

    if request.user != usuario and not request.user.is_staff:
        messages.error(
            request,
            'No tienes permisos para editar este usuario.'
        )
        return redirect('dashboard')

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)

        if form.is_valid():
            usuario = form.save()
            usuario.refresh_from_db()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuarios')
    else:
        form = UsuarioForm(instance=usuario)

    return render(
        request,
        'crm/editar_usuario.html',
        {
            'form': form,
            'usuario': usuario,
        }
    )


@login_required(login_url='/login/')
def perfil_view(request):
    return render(
        request,
        'crm/perfil.html',
        {'usuario': request.user}
    )


@login_required(login_url='/login/')
def editar_perfil_view(request):
    usuario = request.user

    if request.method == 'POST':
        form = UsuarioForm(
            request.POST,
            instance=usuario
        )
        form.fields.pop('es_administrador', None)

        if form.is_valid():
                usuario = form.save()
                usuario.refresh_from_db()
                messages.success(request, 'Tu perfil fue actualizado correctamente.')
        return redirect('perfil')
    else:
        form = UsuarioForm(instance=usuario)
        form.fields.pop('es_administrador', None)

    return render(
        request,
        'crm/editar_perfil.html',
        {'form': form}
    )
    