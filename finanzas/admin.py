from django.contrib import admin

from .models import Caja, Gasto, Impuesto, Ingreso, EstadoResultados, Proyeccion, Balance, ReporteFinanciero

admin.site.register(Caja)
admin.site.register(Gasto)
admin.site.register(Impuesto)
admin.site.register(Ingreso)
admin.site.register(EstadoResultados)
admin.site.register(Proyeccion)
admin.site.register(Balance)
admin.site.register(ReporteFinanciero)
