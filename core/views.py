from django.shortcuts import redirect, render


def home(request):
    return render(request, 'index.html')


def productos_view(request):
    productos = [
        {
            'nombre': 'Ceviche de Camarón',
            'descripcion': 'Fresco y picante, con nuestro toque especial.',
            'precio': '120.00',
            'imagen': 'img/Logo.jpeg',
        },
        {
            'nombre': 'Camarones al Ajillo',
            'descripcion': 'Salteados con ajo y mantequilla, una delicia.',
            'precio': '150.00',
            'imagen': 'img/Producto1.jpeg',
        },
        {
            'nombre': 'Producto Fresco',
            'descripcion': 'Selección de mariscos frescos del día.',
            'precio': '180.00',
            'imagen': 'img/Producto2.jpeg',
        },
    ]
    return render(request, 'productos.html', {'productos': productos})


def ubicacion_view(request):
    return render(request, 'ubicacion.html')


def admin_panel_view(request):
    return render(request, 'admin_panel.html')


def login_view(request):
    # Por ahora esta pantalla es únicamente visual. No hay usuarios ni BD.
    return render(request, 'login.html')


def logout_view(request):
    return redirect('home')

def registro(request):
    # Por ahora esta pantalla es únicamente visual. No hay usuarios ni BD.
    return render(request, 'registro.html')

def politicas_privacidad(request):
    return render(request, 'politicas.html')


def carrito_view(request):
    return render(request, 'carrito.html')


def pago_view(request):
    return render(request, 'pago.html')
