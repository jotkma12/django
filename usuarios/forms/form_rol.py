from django import forms
from ..models import Rol

class RolForm(forms.Form):
    nombre = forms.CharField(
        max_length=50,
        label="Nombre del rol",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    def save(self, commit=True, instance=None):
        if instance is None:
            instance = Rol()
        instance.nombre = self.cleaned_data['nombre']
        instance.descripcion = self.cleaned_data['descripcion']
        if commit:
            instance.save()
        return instance
