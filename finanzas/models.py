from djongo import models


class Ingreso(models.Model):
    concepto = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField()
    metodoPago = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return f"Ingreso de {self.monto} por {self.concepto}"


class Gasto(models.Model):
    concepto = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField()
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return f"Gasto de {self.monto} por {self.concepto}"


class Balance(models.Model):
    fecha = models.DateTimeField()
    ingresosTotales = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    gastosTotales = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    ingresosAcumulados = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    gastosAcumulados = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    saldoAcumulado = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f"Balance del mes {self.fecha} - Saldo: {self.saldo}"


class ReporteFinanciero(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ingresos_totales = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    gastos_totales = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    saldo_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Reporte financiero del {self.fecha_inicio} al {self.fecha_fin}"


class Proyeccion(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ingresos_proyectados = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    gastos_proyectados = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    saldo_proyectado = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    descripcion = models.TextField()

    def __str__(self):
        return f"Proyección del {self.fecha_inicio.strftime('%Y-%m-%d')} al {self.fecha_fin.strftime('%Y-%m-%d')}"


class Impuesto(models.Model):
    tipo_impuesto = models.CharField(max_length=100)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    base_imponible = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    monto_impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    fecha_vencimiento = models.DateTimeField()
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Pagado', 'Pagado')])


    def __str__(self):
        return f"Impuesto {self.tipo_impuesto} - {self.monto_impuesto}"


class Caja(models.Model):
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    ingresos = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    egresos = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    saldo_final = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    fecha = models.DateTimeField()


    def __str__(self):
        return f"Caja del {self.fecha} - Saldo final: {self.saldo_final}"


class EstadoResultados(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ingresos_totales = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    costos_ventas = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    utilidad_bruta = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    gastos_operativos = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    utilidad_operativa = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    utilidad_neta = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)


    def __str__(self):
        return f"Estado de Resultados {self.fecha_inicio} - {self.fecha_fin}"



