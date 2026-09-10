from decimal import Decimal

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Pedido, Producto


def home(request):
    return render(request, 'index.html')


def productos_view(request):
    productos = Producto.objects.filter(disponible=True)
    return render(request, 'productos.html', {'productos': productos})


def ubicacion_view(request):
    return render(request, 'ubicacion.html')


@user_passes_test(lambda user: user.is_staff, login_url='core_login')
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
        return redirect('core_login')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)

            next_url = request.POST.get('next') or request.GET.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('core_login')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('core_login')

def registro(request):
    if request.user.is_authenticated:
        return redirect('core_login')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('core_login')
    return render(request, 'registro.html', {'form': form})

def politicas_privacidad(request):
    return render(request, 'politicas.html')


def carrito_view(request):
    return render(request, 'carrito.html')


def pago_view(request):
    return render(request, 'pago.html')
