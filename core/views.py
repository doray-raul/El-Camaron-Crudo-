from django.shortcuts import render

def home(request):
    # Las imágenes del carrusel pueden ser estáticas o dinámicas
    # Aquí pasamos una lista de diccionarios con info de las imágenes
    carousel_items = [
        {'title': 'Tostadas y Tostitos', 'desc': 'Crujientes y llenos de sabor', 'image': 'core/images/carousel1.jpg'},
        {'title': 'Estilo Jerez', 'desc': 'El auténtico sabor de la región', 'image': 'core/images/carousel2.jpg'},
        {'title': '¡Enchila pero no envenena!', 'desc': 'Nuestro toque especial', 'image': 'core/images/carousel3.jpg'},
    ]
    context = {
        'carousel_items': carousel_items,
    }
    return render(request, 'core/home.html', context)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})