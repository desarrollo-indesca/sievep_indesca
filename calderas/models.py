from django.db import models
from django.contrib.auth import get_user_model

from intercambiadores.models import Planta, Fluido, Unidades

# Create your models here.

class Tambor(models.Model):
    presion_operacion = models.FloatField(null=True, blank = True)
    temp_operacion = models.FloatField(null=True, blank = True)
    presion_diseno = models.FloatField(null=True, blank = True)
    temp_diseno = models.FloatField(null=True, blank = True)
    material = models.CharField(max_length=45, null=True, blank = True)

    temperatura_unidad = models.ForeignKey(Unidades, models.PROTECT, default=1, related_name="temperatura_unidad_tambor")
    presion_unidad = models.ForeignKey(Unidades, models.PROTECT, default=33, related_name="presion_unidad_tambor")

class SeccionTambor(models.Model):
    SECCIONES = [
        ('I','Inferior'),
        ('S','Superior')
    ]

    seccion = models.CharField(max_length=1, choices=SECCIONES)
    diametro = models.FloatField(null=True, blank = True)
    longitud = models.FloatField(null=True, blank = True)
    tambor = models.ForeignKey(Tambor, models.PROTECT)

    dimensiones_unidad = models.ForeignKey(Unidades, models.PROTECT, default=4)

class DimsSobrecalentador(models.Model):
    SECCIONES = [
        ('I','Inferior'),
        ('S','Superior')
    ]

    area_total_transferencia = models.FloatField(null=True, blank = True)
    diametro_tubos = models.FloatField(null=True, blank = True)
    num_tubos = models.IntegerField(null=True, blank = True)

    area_unidad = models.ForeignKey(Unidades, models.PROTECT, default=3, related_name="area_unidad_sobrecalentador")
    diametro_unidad = models.ForeignKey(Unidades, models.PROTECT, default=4, related_name="diametro_unidad_sobrecalentador")

class Sobrecalentador(models.Model):
    presion_operacion = models.FloatField()
    temp_operacion = models.FloatField()
    presion_diseno = models.FloatField()
    flujo_max_continuo = models.FloatField()

    dims = models.OneToOneField(DimsSobrecalentador, models.PROTECT)

    temperatura_unidad = models.ForeignKey(Unidades, models.PROTECT, default=1, related_name="temperatura_unidad_sobrecalentador")
    presion_unidad = models.ForeignKey(Unidades, models.PROTECT, default=33, related_name="presion_unidad_sobrecalentador")
    flujo_unidad = models.ForeignKey(Unidades, models.PROTECT, default=26, related_name="flujo_unidad_sobrecalentador")

class DimensionesCaldera(models.Model):
    ancho = models.FloatField()
    largo = models.FloatField()
    alto = models.FloatField()
    dimensiones_unidad = models.ForeignKey(Unidades, models.PROTECT, default=4)

class EspecificacionesCaldera(models.Model):
    material = models.CharField(max_length=45, null=True, blank = True)

    area_transferencia_calor = models.FloatField(null=True, blank = True)
    area_unidad = models.ForeignKey(Unidades, models.PROTECT, default=3, related_name="area_unidad_especificaciones")

    calor_intercambiado = models.FloatField(null=True, blank = True)
    calor_unidad = models.ForeignKey(Unidades, models.PROTECT, default=62, related_name="calor_unidad_especificaciones")

    capacidad = models.FloatField(null=True, blank = True)
    capacidad_unidad = models.ForeignKey(Unidades, models.PROTECT, default=6, related_name="capacidad_unidad_especificaciones")

    temp_diseno = models.FloatField(null=True, blank = True)
    temp_operacion = models.FloatField(null=True, blank = True)
    temperatura_unidad = models.ForeignKey(Unidades, models.PROTECT, default=1, related_name="temperatura_unidad_especificaciones")

    presion_diseno = models.FloatField(null=True, blank = True)
    presion_operacion = models.FloatField(null=True, blank = True)
    presion_unidad = models.ForeignKey(Unidades, models.PROTECT, default=33, related_name="presion_unidad_especificaciones")

    carga = models.FloatField(null=True, blank = True)
    carga_unidad = models.ForeignKey(Unidades, models.PROTECT, default=6, related_name="carga_unidad_especificaciones")

    eficiencia_termica = models.FloatField(null=True, blank = True)

class Combustible(models.Model):
    nombre_gas = models.CharField(max_length=45)
    liquido = models.BooleanField()
    nombre_liquido = models.CharField(max_length=45, null=True, blank = True)

class ComposicionCombustible(models.Model):
    porc_vol = models.FloatField()
    porc_aire = models.FloatField()
    combustible = models.ForeignKey(Combustible, models.PROTECT)
    fluido = models.ForeignKey(Fluido, models.PROTECT)

class Chimenea(models.Model):
    diametro = models.FloatField(null=True, blank = True)
    altura = models.FloatField(null=True, blank = True)
    dimensiones_unidad = models.ForeignKey(Unidades, models.PROTECT, default=4)

class Economizador(models.Model):
    area_total_transferencia = models.FloatField(null=True, blank = True)
    diametro_tubos = models.FloatField(null=True, blank = True)
    numero_tubos = models.IntegerField(null=True)

    area_unidad = models.ForeignKey(Unidades, models.PROTECT, default=3, related_name="area_unidad_economizador")
    diametro_unidad = models.ForeignKey(Unidades, models.PROTECT, default=4, related_name="diametro_unidad_economizador")

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
    especificaciones = models.OneToOneField(EspecificacionesCaldera, models.PROTECT)
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
    unidad = models.ForeignKey(Unidades, models.PROTECT)

class Corriente(models.Model):
    TIPOS_CORRIENTES = [
        ('V', "Vapor de Alta Presión"),
        ('A', "Agua"),
        ('P', "Purga"),
        ('V', "Vapor de Baja Presión"),
    ]

    numero = models.CharField(max_length=45, unique=True)
    tipo = models.CharField(max_length=1, choices=TIPOS_CORRIENTES)

    flujo_masico = models.FloatField()
    flujo_masico_unidad = models.ForeignKey(Unidades, models.PROTECT, default=26, related_name="flujomasico_unidad_corriente_calderas")
    densidad = models.FloatField()
    densidad_unidad = models.ForeignKey(Unidades, models.PROTECT, default=43, related_name="densidad_unidad_corriente_corriente_calderas")
    estado = models.CharField(max_length=1, choices=[('L','Líquido'), ('V', 'Vapor')])
    temp_operacion = models.FloatField()
    temp_operacion_unidad = models.ForeignKey(Unidades, models.PROTECT, default=1, related_name="temp_operacion_unidad_corriente_calderas")
    presion = models.FloatField()
    presion_unidad = models.ForeignKey(Unidades, models.PROTECT, default=1, related_name="presion_unidad_corriente_calderas")
    caldera = models.ForeignKey(Caldera, on_delete=models.PROTECT)

## EVALUACIONES
class SalidaBalanceEnergia(models.Model):
    energia_entrada_gas = models.FloatField()
    energia_entrada_aire = models.FloatField()
    energia_total_entrada = models.FloatField()
    energia_total_reaccion = models.FloatField()
    energia_horno = models.FloatField()

    energia_unidad = models.ForeignKey(Unidades, models.PROTECT, default=4, related_name="energia_salida_agua_evaluacion")

class SalidaLadoAgua(models.Model):
    flujo_purga = models.FloatField()
    energia_vapor = models.FloatField()
    eficiencia = models.FloatField()

    flujo_unidad = models.ForeignKey(Unidades, models.PROTECT, default=3, related_name="flujo_salida_agua_evaluacion")

class SalidaFracciones(models.Model):
    h2o = models.FloatField()
    co2 = models.FloatField()
    n2 = models.FloatField()
    so2 = models.FloatField()
    o2 = models.FloatField()

class SalidaBalanceMolar(models.Model):
    # Se asumen todas las unidades como kmol/h
    n_gas_entrada = models.FloatField()
    n_aire_gas_entrada = models.FloatField()
    n_total = models.FloatField()

class SalidaFlujosEntrada(models.Model):
    flujo_gas_entrada = models.FloatField()
    flujo_aire_entrada = models.FloatField()
    flujo_combustion = models.FloatField()
    flujo_combustion_vol = models.FloatField()
    porc_o2_exceso = models.FloatField()

    flujo_masico_unidad = models.ForeignKey(Unidades, models.PROTECT, related_name="flujo_masico_unidad_salida_flujos_evaluacion")    
    flujo_vol_unidad = models.ForeignKey(Unidades, models.PROTECT, related_name="flujo_volumetrico_unidad_salida_flujos_evaluacion")

class Evaluacion(models.Model):
    nombre = models.CharField(max_length=45)
    fecha = models.DateTimeField(auto_created=True)

    salida_flujos = models.ForeignKey(SalidaFlujosEntrada, models.PROTECT)
    salida_balance_molar = models.ForeignKey(SalidaBalanceMolar, models.PROTECT)
    salida_fracciones = models.ForeignKey(SalidaFracciones, models.PROTECT)
    salida_balance_energia = models.ForeignKey(SalidaBalanceEnergia, models.PROTECT)
    salida_lado_agua = models.ForeignKey(SalidaLadoAgua, models.PROTECT)
    caldera = models.ForeignKey(Caldera, models.PROTECT)

class EntradasFluidos(models.Model):
    TIPOS_FLUIDOS = [
        ("G","Gas"),
        ("A","Aire"),
        ("H","Horno"),
        ("L","Líquido"),
        ("W","Agua de Entrada a la Caldera"),
        ("V","Vapor Producido")
    ]

    nombre_fluido = models.CharField("Nombre del Fluido", max_length=45)
    flujo = models.FloatField("Flujo Másico")
    temperatura = models.FloatField("Temperatura de Operación")
    presion = models.FloatField("Presión de Operación")
    tipo_fluido = models.CharField(max_length=1, choices=TIPOS_FLUIDOS)
    humedad_relativa = models.FloatField(null=True, blank=True)
    evaluacion = models.ForeignKey(Evaluacion, models.PROTECT)