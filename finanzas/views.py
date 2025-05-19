from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Ingreso,Gasto, Balance,Caja, ReporteFinanciero,Proyeccion,Impuesto,EstadoResultados
from .forms import FormularioIngreso, FormularioGasto
from datetime import datetime
from collections import defaultdict
from .models import Balance
from decimal import Decimal
from collections import namedtuple


# def inicio(request):
#     return HttpResponse('<h1>bienvenido al modulo contabilidad</h1>')

def inicio(request):
    return render(request, 'index.html')

def goIndex(request):
    return render(request, 'index.html')



def finanzas(request):
    return render(request, 'index.html')

def crearIngreso(request):
    if request.method == "POST":
        nuevoIngreso = Ingreso(
        concepto=request.POST['concepto'],
        monto=request.POST['monto'],
        fecha=request.POST['fecha'],
        metodoPago=request.POST['metodoPago'],
        descripcion=request.POST['descripcion']
        )
        nuevoIngreso.save()
        return redirect('crearIngreso')
    else:
        data = Ingreso.objects.all().order_by('-fecha')
        return render(request, 'ingresos.html', {'informacion':data, 'formulario': FormularioIngreso})
    
def mostrarIngreso(request, idIngreso):

    try:
        ingreso = Ingreso.objects.get(id=idIngreso)
    except ObjectDoesNotExist:
        ingreso = None

    if ingreso is not None:
        if request.method == "GET":
            formulario = FormularioIngreso(initial={
                'id': ingreso.id,
                'concepto': ingreso.concepto,
                'monto':ingreso.monto,
                'fecha':ingreso.fecha,
                'metodoPago': ingreso.metodoPago,
                'descripcion': ingreso.descripcion
            })
            data = Ingreso.objects.all().order_by('-fecha')
            mostrarFormulario = True

            return render(request, 'ingresos.html', {'informacion':data,'formulario': formulario, 'mostrarFormulario': mostrarFormulario})
        else:
            concepto=request.POST['concepto']
            monto=request.POST['monto']
            fecha=request.POST['fecha']
            metodoPago=request.POST['metodoPago']
            descripcion=request.POST['descripcion']
     
            if ingreso.concepto != concepto:
                ingreso.concepto = concepto
            if ingreso.monto != monto:
                ingreso.monto = monto
            if ingreso.fecha != fecha:
                ingreso.fecha = fecha
            if ingreso.metodoPago != metodoPago:
                ingreso.metodoPago = metodoPago
            if ingreso.descripcion != descripcion:
                ingreso.descripcion = descripcion

            ingreso.save()

            return redirect('crearIngreso') 

def eliminarIngreso(request, idIngreso):
    try:
        ingreso = Ingreso.objects.get(id=idIngreso)
    except ObjectDoesNotExist:
        ingreso = None

    if ingreso is not None:
        if request.method == "POST":
            ingreso.delete()
    return redirect('crearIngreso') 



def crearGasto(request):
    if request.method == "POST":
        nuevoGasto = Gasto(
        concepto=request.POST['concepto'],
        monto=request.POST['monto'],
        fecha=request.POST['fecha'],
        categoria=request.POST['categoria'],
        descripcion=request.POST['descripcion']
        )
        nuevoGasto.save()
        return redirect('crearIngreso')
    else:
        data = Gasto.objects.all().order_by('-fecha')
        return render(request, 'gastos.html', {'informacion':data, 'formulario': FormularioGasto})
    
def mostrarGasto(request, idGasto):

    try:
        gasto = Gasto.objects.get(id=idGasto)
    except ObjectDoesNotExist:
        gasto = None

    if gasto is not None:
        if request.method == "GET":
            formulario = FormularioGasto(initial={
                'id': gasto.id,
                'concepto': gasto.concepto,
                'monto':gasto.monto,
                'fecha':gasto.fecha,
                'categoria': gasto.categoria,
                'descripcion': gasto.descripcion
            })
            data = Gasto.objects.all().order_by('-fecha')
            mostrarFormulario = True

            return render(request, 'Gastos.html', {'informacion':data,'formulario': formulario, 'mostrarFormulario': mostrarFormulario})
        else:
            concepto=request.POST['concepto']
            monto=request.POST['monto']
            fecha=request.POST['fecha']
            categoria=request.POST['categoria']
            descripcion=request.POST['descripcion']
     
            if gasto.concepto != concepto:
                gasto.concepto = concepto
            if gasto.monto != monto:
                gasto.monto = monto
            if gasto.fecha != fecha:
                gasto.fecha = fecha
            if gasto.categoria != categoria:
                gasto.categoria = categoria
            if gasto.descripcion != descripcion:
                gasto.descripcion = descripcion

            gasto.save()

            return redirect('crearGasto') 

def eliminarGasto(request, idGasto):
    try:
        gasto = Gasto.objects.get(id=idGasto)
    except ObjectDoesNotExist:
        gasto = None

    if gasto is not None:
        if request.method == "POST":
            gasto.delete()
    return redirect('crearGasto') 

# def mostrarBalance(request):
#     if request.method == "GET":
#         data = Balance.objects.all().order_by('-fecha')
#         return render(request, 'balance.html', {'informacion': data})

def mostrarBalance(request):
    balances = Balance.objects.all().order_by('-fecha')

    informacionMes = defaultdict(lambda: {'ingresos': Decimal('0'), 'gastos': Decimal('0')})

    for b in balances:
        mes = b.fecha.strftime('%Y-%m')

        ingresos = b.ingresosTotales.to_decimal() if b.ingresosTotales else Decimal('0')
        gastos = b.gastosTotales.to_decimal() if b.gastosTotales else Decimal('0')

        informacionMes[mes]['ingresos'] += ingresos
        informacionMes[mes]['gastos'] += gastos

    informacionOrdenaMes= dict(sorted(informacionMes.items()))

    labels = [datetime.strptime(k, '%Y-%m').strftime('%b %Y') for k in informacionOrdenaMes.keys()]
    ingresos = [float(v['ingresos']) for v in informacionOrdenaMes.values()]
    gastos = [float(v['gastos']) for v in informacionOrdenaMes.values()]

    balances2 = Balance.objects.all().order_by('-fecha')

    BalanceConMes = namedtuple('BalanceConMes', ['mes', 'balance'])

    balancesMes = [
        BalanceConMes(
            mes=balance.fecha.strftime('%Y-%m'),
            balance=balance
        )
        for balance in balances2
    ]

    return render(request, 'balance.html', {
        'informacion': balances,
        'labels': labels,
        'ingresos': ingresos,
        'gastos': gastos,
        'balances_con_mes': balancesMes
    })
    
    
