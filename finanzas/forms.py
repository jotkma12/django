from django import forms

class FormularioIngreso(forms.Form):
    concepto = forms.CharField(max_length=255)
    monto = forms.DecimalField(max_digits=10, decimal_places=2)
    fecha = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local'
            }
        ),
        input_formats=['%Y-%m-%dT%H:%M:%S'],
    )
    metodoPago = forms.ChoiceField(choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia'),('nequi', 'Nequi'), ('daviplata','Daviplata')])
    descripcion = forms.CharField(widget=forms.Textarea)


class FormularioGasto(forms.Form):
    opcionesCategoria = [
        ('materia_prima', 'Materia Prima'),
        ('sueldos', 'Sueldos y Salarios'),
        ('alquiler', 'Alquiler'),
        ('servicios', 'Servicios Públicos'),
        ('equipos', 'Equipos y Herramientas'),
        ('publicidad', 'Publicidad y Marketing'),
        ('transporte', 'Transporte'),
        ('mantenimiento', 'Gastos de Mantenimiento'),
        ('seguros', 'Seguros'),
        ('costos_financieros', 'Costos Financieros'),
        ('impuestos', 'Impuestos'),
        ('material_empaque', 'Material de Empaque'),
        ('administrativos', 'Gastos Administrativos'),
        ('otros', 'Otros'),
    ]
    concepto = forms.CharField(max_length=255)
    monto = forms.DecimalField(max_digits=10, decimal_places=2)
    fecha = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local'
            }
        ),
        input_formats=['%Y-%m-%dT%H:%M:%S'],
    )
    categoria = forms.ChoiceField(choices=opcionesCategoria)
    descripcion = forms.CharField(widget=forms.Textarea)