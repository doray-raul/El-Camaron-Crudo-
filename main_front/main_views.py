from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

def index(request):
    # Datos para el carrusel (pueden ser imágenes de productos)
    carrusel_items = [
        {'imagen': 'img/producto1.jpg', 'titulo': 'Tostadas y Tostitos', 'descripcion': 'Estilo Jerez'},
        {'imagen': 'img/producto2.jpg', 'titulo': 'Aguachile', 'descripcion': 'El mejor sabor'},
        {'imagen': 'img/producto3.jpg', 'titulo': 'Ceviche', 'descripcion': 'Fresco y delicioso'},
        # Puedes agregar más
    ]
    context = {'carrusel_items': carrusel_items}
    return render(request, 'main/index.html', context)

# Login y Logout los podemos usar directamente desde django.contrib.auth.urls
# Pero creamos vistas para registro
class RegistroView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registro.html'