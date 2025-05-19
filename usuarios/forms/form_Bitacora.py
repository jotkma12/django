from django import forms
from ..models import BitacoraActividad

class BitacoraActividadForm(forms.ModelForm):
    class Meta:
        model = BitacoraActividad
        fields = ['usuario', 'accion', 'ip', 'descripcion']
