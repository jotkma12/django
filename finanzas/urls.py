from django.urls import path
from .views import inicio, goIndex, finanzas, crearIngreso, mostrarIngreso, eliminarIngreso, crearGasto, mostrarGasto, eliminarGasto, mostrarBalance

urlpatterns = [
    path('finanzas/', inicio, name='inicio'),
    path('index/', goIndex, name='index'),
    path('finanzas/', finanzas, name="finanzas"),
    path('finanzas/ingresos', crearIngreso, name="crearIngreso"),
    path('finanzas/ingresos/<int:idIngreso>', mostrarIngreso, name="mostrarIngreso"),
    path('finanzas/ingresos/del/<int:idIngreso>', eliminarIngreso, name="eliminarIngreso"),
    path('finanzas/gastos', crearGasto, name="crearGasto"),
    path('finanzas/gastos/<int:idGasto>', mostrarGasto, name="mostrarGasto"),
    path('finanzas/gastos/del/<int:idGasto>', eliminarGasto, name="eliminarGasto"),
    path('finanzas/balance/', mostrarBalance, name="mostrarBalance")

]