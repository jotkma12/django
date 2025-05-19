from django import forms
from usuarios.models import Direccion, Usuario

class DireccionForm(forms.Form):
    direccion = forms.CharField(max_length=100)
    barrio = forms.CharField(max_length=100)
    ciudad = forms.CharField(max_length=100)
    principal = forms.BooleanField(required=False)

    def update(self, instancia):
        instancia.direccion = self.cleaned_data['direccion']
        instancia.barrio = self.cleaned_data['barrio']
        instancia.ciudad = self.cleaned_data['ciudad']
        instancia.principal = self.cleaned_data['principal']
        instancia.save()
