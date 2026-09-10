from decimal import Decimal

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import redirect, render

from .models import Pedido, Producto


def home(request):
    return render(request, 'index.html')


def productos_view(request):
    return render(request, 'productos.html', {'productos': Producto.objects.filter(disponible=True)})


def ubicacion_view(request):
    return render(request, 'ubicacion.html')


@user_passes_test(lambda user: user.is_staff, login_url='login')
def admin_panel_view(request):
    pedidos = Pedido.objects.prefetch_related('detalles').all()
    return render(request, 'admin_panel.html', {
        'total_usuarios': User.objects.count(), 'total_productos': Producto.objects.count(),
        'total_pedidos': pedidos.count(),
        'ingresos': pedidos.filter(estado=Pedido.Estado.PAGADO).aggregate(total=Sum('total'))['total'] or Decimal('0.00'),
        'ultimos_pedidos': pedidos[:5],
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.POST.get('next') or request.GET.get('next') or 'home')
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')


def registro(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.save())
        return redirect('home')
    return render(request, 'registro.html', {'form': form})


def politicas_privacidad(request):
    return render(request, 'politicas.html')


def carrito_view(request):
    return render(request, 'carrito.html')


def pago_view(request):
    return render(request, 'pago.html')
