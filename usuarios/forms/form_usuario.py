from django import forms
from usuarios.models import Usuario, Rol, Estado
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError


class UsuarioForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    numero_documento = forms.CharField(max_length=30)
    correo = forms.EmailField()
    telefono = forms.CharField(max_length=20)
    contrasena = forms.CharField(widget=forms.PasswordInput)
    rol = forms.ModelChoiceField(queryset=Rol.objects.all())
    estado = forms.ModelChoiceField(queryset=Estado.objects.all())

    def clean_contrasena(self):
        return make_password(self.cleaned_data['contrasena'])
    
    """def clean_numero_documento(self):
        numero = self.cleaned_data['numero_documento']
        if Usuario.objects.filter(numero_documento=numero).exists():
            raise ValidationError("El número de documento ya está registrado.")
        return numero

    def clean_correo(self):
        email = self.cleaned_data['correo']
        if Usuario.objects.filter(correo=email).exists():
            raise ValidationError("El correo ya está registrado.")
        return email"""

    def save(self):
        data = self.cleaned_data
        usuario = Usuario.objects.create(
            nombre=data['nombre'],
            apellido=data['apellido'],
            numero_documento=data['numero_documento'],
            correo=data['correo'],
            telefono=data['telefono'],
            contrasena=data['contrasena'],
            rol=data['rol'],
            estado=data['estado']
        )
        return usuario
