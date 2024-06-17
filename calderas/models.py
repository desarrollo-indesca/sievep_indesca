from django.db import models
from django.contrib.auth import get_user_model

from intercambiadores.models import Planta, Fluido

# Create your models here.

class Tambor(models.Model):
    presion_operacion = models.FloatField()
    temp_operacion = models.FloatField()
    presion_diseno = models.FloatField()
    temp_diseno = models.FloatField()
    material = models.CharField(max_length=45)

class SeccionTambor(models.Model):
    SECCIONES = [
        ('I','Inferior'),
        ('S','Superior')
    ]

    seccion = models.CharField(max_length=1, choices=SECCIONES)
    diametro = models.FloatField(null=True)
    longitud = models.FloatField(null=True)
    tambor = models.ForeignKey(Tambor, models.PROTECT)

class DimsSobrecalentador(models.Model):
    SECCIONES = [
        ('I','Inferior'),
        ('S','Superior')
    ]

    area_total_transferencia = models.FloatField(null=True)
    diametro_tubos = models.FloatField(null=True)
    num_tubos = models.IntegerField(null=True)

class Sobrecalentador(models.Model):
    presion_operacion = models.FloatField()
    temp_operacion = models.FloatField()
    presion_diseno = models.FloatField()
    flujo_max_continuo = models.FloatField()

    dims = models.OneToOneField(DimsSobrecalentador, models.PROTECT)

class DimensionesCaldera(models.Model):
    ancho = models.FloatField()
    largo = models.FloatField()
    alto = models.FloatField()

class ParametrosCaldera(models.Model):
    material = models.CharField(max_length=45)
    area_transferencia_calor = models.FloatField()
    calor_intercambiado = models.FloatField()
    eficiencia_termina = models.FloatField()
    capacidad = models.FloatField()
    temp_diseno = models.FloatField()
    presion_diseno = models.FloatField()
    temp_operacion = models.FloatField()
    presion_operacion = models.FloatField()
    carga = models.FloatField()

class Combustible(models.Model):
    nombre_gas = models.CharField(max_length=45)
    liquido = models.BooleanField()
    nombre_liquido = models.CharField(max_length=45, null=True)

class ComposicionCombustible(models.Model):
    porc_vol = models.FloatField()
    porc_aire = models.FloatField()
    combustible = models.ForeignKey(Combustible, models.PROTECT)
    fluido = models.ForeignKey(Fluido, models.PROTECT)

class Chimenea(models.Model):
    diametro = models.FloatField(null=True)
    altura = models.FloatField(null=True)

class Economizador(models.Model):
    area_total_transferencia = models.FloatField(null=True)
    diametro_tubos = models.FloatField(null=True)
    numero_tubos = models.IntegerField(name=True)

class Caldera(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, related_name="planta_caldera")
    tag = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")
    fabricante = models.CharField(max_length=45, null = True, blank = True)
    modelo = models.CharField(max_length=45, null = True, blank = True)
    tipo_caldera = models.CharField(max_length=45, null = True, blank = True)
    accesorios = models.CharField(max_length=45, null = True, blank = True)

    sobrecalentador = models.OneToOneField(Sobrecalentador, models.CASCADE)
    tambor = models.OneToOneField(Tambor, models.PROTECT)
    dimensiones = models.OneToOneField(DimsSobrecalentador, models.PROTECT)
    parametros = models.OneToOneField(ParametrosCaldera, models.PROTECT)
    combustible = models.OneToOneField(Combustible, models.PROTECT)
    chimenea = models.OneToOneField(Chimenea, models.PROTECT)
    economizador = models.OneToOneField(Economizador, models.PROTECT)

    creado_al = models.DateTimeField(auto_now_add=True)
    editado_al = models.DateTimeField(null = True)
    creado_por = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="caldera_creada_por")
    editado_por = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null = True, related_name="caldera_editada_por")

class Caracteristica(models.Model):
    clase = models.CharField(max_length=1)
    nombre = models.CharField(max_length=45)
    tipo_unidad = models.CharField(max_length=1)
    caldera = models.ForeignKey(Caldera, on_delete=models.PROTECT)

class ValorPorCarga(models.Model):
    tipo = models.CharField(max_length=1)
    carga = models.FloatField()
    valor_num = models.FloatField()
    caracteristica = models.ForeignKey(Caracteristica, models.PROTECT)

class Corriente(models.Model):
    TIPOS_CORRIENTES = [
        ('V', "Vapor de Alta Presión"),
        ('A', "Agua"),
        ('P', "Purga"),
        ('V', "Vapor de Baja Presión"),
    ]

    numero = models.CharField(max_length=45, unique=True)
    tipo = models.CharField(choices=TIPOS_CORRIENTES)
    flujo_masico = models.FloatField()
    densidad = models.FloatField()
    estado = models.CharField(max_length=[('L','Líquido'), ('V', 'Vapor')])
    temp_operacion = models.FloatField()
    presion = models.FloatField()
    caldera = models.ForeignKey(Caldera, on_delete=models.PROTECT)

## EVALUACIONES