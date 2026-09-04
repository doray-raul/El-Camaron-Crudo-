from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Cliente
from .forms import ClienteForm

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


def dashboard_view(request):
    context = {
        'total_clientes': 128,
        'clientes_activos': 96,
        'interacciones': 48,
        'clientes_en_riesgo': 15,
    }
    return render(request, 'crm/dashboard.html', context)

def clientes_view(request):
    clientes = Cliente.objects.all()

    context = {
        'clientes': clientes
    }

    return render(request, 'crm/clientes.html', context)

def detalle_cliente_view(request, cliente_id):
    # Simulamos los datos del cliente seleccionado
    cliente = {
        'id': cliente_id,
        'nombre': 'María López',
        'empresa': 'Cliente Frecuente - El Camarón Crudo',
        'correo': 'maria@email.com',
        'telefono': '449-123-4567',
        'fecha_registro': '10/01/2026',
        'etapa': 'Frecuente',
        'estado': 'Activo'
    }
    
    # Historial de interacciones (Timeline requerido por la profesora)
    interacciones = [
        {'tipo': 'Llamada', 'fecha': '15/08/2026', 'descripcion': 'Se confirmó pedido de tostilocos y se habló sobre próximos productos de temporada.', 'usuario': 'Admin'},
        {'tipo': 'Correo', 'fecha': '10/08/2026', 'descripcion': 'Se envió información y menú actualizado de litros de aguachile y ceviche.', 'usuario': 'Admin'},
        {'tipo': 'Reunión', 'fecha': '02/08/2026', 'descripcion': 'Reunión en sucursal para revisar opciones de servicio para evento especial.', 'usuario': 'Admin'},
    ]

    context = {
        'cliente': cliente,
        'interacciones': interacciones
    }
    return render(request, 'crm/detalle_cliente.html', context)

def nuevo_cliente_view(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()

    return render(request, 'crm/nuevo_cliente.html', {'form': form})

def editar_cliente_view(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(
        request,
        'crm/editar_cliente.html',
        {'form': form, 'cliente': cliente}
    )