from django.shortcuts import render

from .models import Producto


def productos_view(request):
    productos = Producto.objects.filter(disponible=True)
    return render(request, 'productos.html', {'productos': productos})
