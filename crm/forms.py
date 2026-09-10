from django import forms
from django.contrib.auth.models import User
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'correo',
            'telefono',
            'etapa_crm',
            'estado',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
                'placeholder': 'Nombre completo',
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
                'placeholder': 'correo@ejemplo.com',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
                'placeholder': '449-123-4567',
            }),
            'etapa_crm': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-coral/20 focus:border-brand-coral',
            }),
        }


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg',
            'placeholder': 'Nueva contraseña',
        }),
        required=False
    )

    password_confirmacion = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg',
            'placeholder': 'Confirmar nueva contraseña',
        }),
        required=False
    )

    es_administrador = forms.BooleanField(
        label='Administrador',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4',
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg',
                'placeholder': 'Nombre',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg',
                'placeholder': 'Apellidos',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg',
                'placeholder': 'correo@ejemplo.com',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirmacion = cleaned_data.get('password_confirmacion')

        if password or confirmacion:
            if password != confirmacion:
                raise forms.ValidationError(
                    'Las contraseñas no coinciden.'
                )

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)

        usuario.username = usuario.email

        password = self.cleaned_data.get('password')

        if password:
            usuario.set_password(password)

        usuario.is_staff = self.cleaned_data.get(
            'es_administrador',
            False
        )

        if commit:
            usuario.save()

        return usuario