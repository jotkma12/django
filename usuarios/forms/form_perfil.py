from django import forms
from ..models import Perfil

class PerfilForm(forms.Form):
    fecha_nacimiento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    foto = forms.ImageField(required=False)

    def save(self, usuario):
        data = self.cleaned_data
        perfil = Perfil.objects.create(
            usuario=usuario,
            fecha_nacimiento=data.get('fecha_nacimiento'),
            foto=data.get('foto')
        )
        return perfil
