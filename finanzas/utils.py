from pymongo import MongoClient
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from decimal import Decimal
from .models import Balance

client = MongoClient("mongodb://localhost:27017/")
db = client["base_panaderia"]
ingresosCollection = db["finanzas_ingreso"]
gastosCollection = db["finanzas_gasto"]
def generarBalances():
    
    ingresosAcumulados = Decimal('0.00')
    gastosAcumulados = Decimal('0.00')
    saldo = Decimal('0.00')
    saldoAcumulado = Decimal('0.00')
    ingresosTotales = Decimal('0.00')
    gastosTotales = Decimal('0.00')
    
    pipeline = [
        {
            '$project': {
                'day': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$fecha'}},
                'monto': 1
            }
        },
        {
            '$group': {
                '_id': '$day',
                'total': {'$sum': '$monto'}
            }
        }
    ]

    ingresos = list(ingresosCollection.aggregate(pipeline))
    gastos = list(gastosCollection.aggregate(pipeline))

    ingresosDiccionario = {item['_id']: Decimal(str(item['total'])) for item in ingresos}
    gastosDiccionario = {item['_id']: Decimal(str(item['total'])) for item in gastos}

    fechas = set(ingresosDiccionario.keys()) | set(gastosDiccionario.keys())

    

    for dia in fechas:
        fecha = make_aware(parse_datetime(dia + "T00:00:00"))

        ingresosTotales = ingresosDiccionario.get(dia, Decimal('0.00'))
        gastosTotales = gastosDiccionario.get(dia, Decimal('0.00'))

        ingresosAcumulados += ingresosTotales
        gastosAcumulados += gastosTotales

        saldo = ingresosTotales - gastosTotales
        saldoAcumulado = ingresosAcumulados - gastosAcumulados
        

        Balance.objects.update_or_create(
            fecha=fecha,
            defaults={
                'ingresosTotales': ingresosTotales,
                'gastosTotales': gastosTotales,
                'saldo': saldo,
                'ingresosAcumulados': ingresosAcumulados,
                'gastosAcumulados': gastosAcumulados,
                'saldoAcumulado': saldoAcumulado
            }
        )