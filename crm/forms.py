from django import forms
from django.contrib.auth.models import Group, User

from .models import Cliente, Interaccion


INPUT = 'w-full px-4 py-2 border border-slate-300 rounded-lg'


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre', 'correo', 'telefono', 'etapa_crm', 'estado')
        widgets = {field: forms.TextInput(attrs={'class': INPUT}) for field in ('nombre', 'telefono')}
        widgets.update({'correo': forms.EmailInput(attrs={'class': INPUT}), 'etapa_crm': forms.Select(attrs={'class': INPUT}), 'estado': forms.Select(attrs={'class': INPUT})})


class InteraccionForm(forms.ModelForm):
    class Meta:
        model = Interaccion
        fields = ('cliente', 'tipo', 'descripcion')
        widgets = {'cliente': forms.Select(attrs={'class': INPUT}), 'tipo': forms.Select(attrs={'class': INPUT}), 'descripcion': forms.Textarea(attrs={'class': INPUT, 'rows': 4})}


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', required=False, widget=forms.PasswordInput(attrs={'class': INPUT}))
    password_confirmacion = forms.CharField(label='Confirmar contraseña', required=False, widget=forms.PasswordInput(attrs={'class': INPUT}))
    rol = forms.ChoiceField(label='Rol', choices=())
    is_active = forms.BooleanField(label='Activo', required=False, initial=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {field: forms.TextInput(attrs={'class': INPUT}) for field in ('first_name', 'last_name')}
        widgets['email'] = forms.EmailInput(attrs={'class': INPUT})

    def __init__(self, *args, allowed_roles=('empleado', 'admin'), include_role=True, include_active=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].choices = [(role, 'Administrador' if role == 'admin' else 'Empleado') for role in allowed_roles]
        if self.instance.pk:
            self.initial['rol'] = 'admin' if self.instance.groups.filter(name='admin').exists() else 'empleado'
        if not include_role:
            self.fields.pop('rol')
        if not include_active:
            self.fields.pop('is_active')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        users = User.objects.filter(email__iexact=email)
        if self.instance.pk:
            users = users.exclude(pk=self.instance.pk)
        if users.exists():
            raise forms.ValidationError('Ya existe un usuario con este correo.')
        return email

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password_confirmacion'):
            self.add_error('password_confirmacion', 'Las contraseñas no coinciden.')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        if 'is_active' in self.fields:
            user.is_active = self.cleaned_data['is_active']
        if commit:
            user.save()
            if 'rol' in self.fields:
                user.groups.remove(*user.groups.filter(name__in=('admin', 'empleado')))
                user.groups.add(Group.objects.get(name=self.cleaned_data['rol']))
        return user
