from faker import Faker
import random
from ..models import *
from finanzas.utils import generarBalances


fake = Faker('es_ES')


metodos_pago = ['Efectivo', 'Tarjeta de crédito', 'Transferencia', 'Nequi', 'Daviplata']
categorias_gasto = ['Harina', 'Servicios públicos', 'Mantenimiento', 'Personal', 'Publicidad']
estados_pago = ['Pendiente', 'Pagado']
tipos_impuesto = ['IVA', 'Renta', 'Retefuente']



def crearIngresos(n=10):
    for _ in range(n):
        Ingreso.objects.create(
            concepto=random.choice(['Venta de pan francés', 'Venta de tortas', 'Venta de galletas', 'Pedido a domicilio']),
            monto=round(random.uniform(5000, 50000), 2),
            fecha=fake.date_time_between(start_date='-1y', end_date='now'),
            metodoPago=random.choice(metodos_pago),
            descripcion=fake.sentence(nb_words=8)
        )

def crearGastos(n=10):
    for _ in range(n):
        Gasto.objects.create(
            concepto=random.choice(['Compra de harina', 'Pago de servicios', 'Reparación de horno', 'Salario del panadero', 'Campaña en redes']),
            monto=round(random.uniform(10000, 80000), 2),
            fecha=fake.date_time_between(start_date='-1y', end_date='now'),
            categoria=random.choice(categorias_gasto),
            descripcion=fake.sentence(nb_words=10)
        )


def crearDatos():
    crearGastos()
    crearIngresos()
    generarBalances()
