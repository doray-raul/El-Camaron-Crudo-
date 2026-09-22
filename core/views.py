from decimal import Decimal

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from productos.models import Producto
from ventas.models import Pedido
from crm.access import is_admin, is_internal_user
from crm.models import Cliente
from .forms import RegistroPublicoForm


def home(request):
    return render(request, 'index.html')


def ubicacion_view(request):
    return render(request, 'ubicacion.html')


@user_passes_test(is_admin, login_url='core_login')
def admin_panel_view(request):
    pedidos = Pedido.objects.prefetch_related('detalles').all()
    context = {
        'total_usuarios': User.objects.count(),
        'total_productos': Producto.objects.count(),
        'total_pedidos': pedidos.count(),
        'ingresos': pedidos.filter(estado=Pedido.Estado.PAGADO).aggregate(total=Sum('total'))['total'] or Decimal('0.00'),
        'ultimos_pedidos': pedidos[:5],
    }
    return render(request, 'admin_panel.html', context)


def login_view(request):
    if request.user.is_authenticated:
        if is_internal_user(request.user):
            return redirect('dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)

            next_url = request.POST.get('next') or request.GET.get('next')

            if is_internal_user(usuario) and next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
                return redirect(next_url)

            if is_internal_user(usuario):
                return redirect('dashboard')

            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('core_login')

def registro(request):
    if request.user.is_authenticated:
        if is_internal_user(request.user):
            return redirect('dashboard')
        return redirect('home')

    form = RegistroPublicoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        # A public account is a customer profile, never an internal CRM role.
        Cliente.objects.get_or_create(
            usuario=user,
            defaults={
                'nombre': user.get_full_name() or user.username,
                'correo': user.email,
                'telefono': form.cleaned_data.get('telefono', ''),
            },
        )
        login(request, user)
        return redirect('home')

    return render(request, 'registro.html', {'form': form})

def politicas_privacidad(request):
    return render(request, 'politicas.html')


def carrito_view(request):
    return render(request, 'carrito.html')


def pago_view(request):
    return render(request, 'pago.html')
