from django.db import models

# Create your models here.
class CatalogoCuenta(models.Model):
    idCuenta = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=5)
    tipoDeCuenta = models.CharField(max_length=50)
    nombreDeCuenta = models.CharField(max_length=100)

class LibroMayor(models.Model):    
    idLibro = models.AutoField(primary_key=True)
    nombreLibro = models.CharField(max_length=50)
    fechaDeApertura = models.DateField()
    fechaDeCierre = models.DateField()
    saldoAcreedor = models.FloatField(null=True, blank=True)
    saldoDeudor = models.FloatField(null=True, blank=True)

    
class RegistroTransaccion(models.Model):
    idRegistro = models.AutoField(primary_key=True)
    fechaDeRegistro = models.DateField()
    #esto se refiere al debe y haber
    tipoDeMonto = models.CharField(max_length=50)
    montoTransaccion = models.FloatField()
    descripcion = models.TextField(null=True, blank=True)

    #asociacion con libro mayor de muchos a uno
    registroLibro = models.ForeignKey(LibroMayor, null=True, blank=True, on_delete=models.CASCADE)
    registroCatalogo = models.ForeignKey(CatalogoCuenta, null=True, blank=True, on_delete=models.CASCADE)

class CierreContable(models.Model):
    idCierre = models.AutoField(primary_key=True)
    cierreLibro = models.ForeignKey(LibroMayor, null=True, blank=True, on_delete=models.CASCADE)
    ventasNetas = models.FloatField(null=True, blank=True)
    comprasNetas = models.FloatField(null=True, blank=True)
    comprasTotales = models.FloatField(null=True, blank=True)
    mercanciasDisponibles = models.FloatField(null=True, blank=True)
    costoDeVentas = models.FloatField(null=True, blank=True)
    
class Inventario(models.Model):
    idInventario = models.AutoField(primary_key=True)
    fechaDeMovimiento = models.DateField()
    tipoDeMovimiento = models.CharField(max_length=50)
    cantidadProducto = models.IntegerField(null=True, blank=True)
    costoUnitario = models.FloatField(null=True, blank=True)
    descripcionInventario = models.TextField(null=True, blank=True)
    residuo = models.FloatField(null=True, blank=True)
    montoValor = models.FloatField(null=True, blank=True)
    saldoValor = models.FloatField(null=True, blank=True)

class ManoObra(models.Model):
    idManoObra = models.AutoField(primary_key=True)
    salarioNominal = models.FloatField(null=True, blank=True)
    horasTrabajo = models.FloatField(null=True, blank=True)
    diasTrabajo = models.FloatField(null=True, blank=True)
    diasVacaciones = models.IntegerField(null=True, blank=True)
    recargoVacaciones = models.FloatField(null=True, blank=True)
    diasAguinaldo = models.IntegerField(null=True, blank=True)
    porcentajeISSS = models.FloatField(null=True, blank=True)
    porcentajeAFP = models.FloatField(null=True, blank=True)
    porcentajeEficiencia = models.FloatField(null=True, blank=True)