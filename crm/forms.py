from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'empresa',
            'correo',
            'telefono',
            'etapa',
            'estado',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
                'placeholder': 'Nombre completo',
            }),

            'empresa': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
                'placeholder': 'Empresa o negocio',
            }),

            'correo': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
                'placeholder': 'correo@ejemplo.com',
            }),

            'telefono': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
                'placeholder': '449-123-4567',
            }),

            'etapa': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
            }),

            'estado': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
            }),
        }