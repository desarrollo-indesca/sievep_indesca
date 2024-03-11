from django.db import models
from django.contrib.auth import get_user_model
from intercambiadores.models import Fluido, Planta, Unidades

# MODELOS DE BOMBAS

MOTOR_POSICIONES = (
    ('H', 'Horizontal'),
    ('V','Vertical')
)

AISLAMIENTO = (
    ('F','CLASE F')
)

class TipoBomba(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

class DetallesMotor(models.Model):
    potencia = models.FloatField(null = True, verbose_name = "Potencia de la Bomba")
    potencia_unidad = models.ForeignKey(Unidades, related_name="potencia_unidad_detallesmotor")
    velocidad = models.FloatField(verbose_name="Velocidad del Motor (RPM)") # RPM
    factor_de_servicio = models.FloatField(null = True)
    posicion = models.CharField(null = True, max_length = 1, choices = MOTOR_POSICIONES, verbose_name="Posición del Motor")
    voltaje = models.FloatField(null=True)
    voltaje_unidad = models.ForeignKey(Unidades, related_name="voltaje_unidad_detallesmotor")
    fases = models.SmallIntegerField(null = True)
    frecuencia = models.FloatField(null = True)
    frecuencia_unidad = models.ForeignKey(Unidades, related_name="frecuencia_unidad_detallesmotor")
    aislamiento = models.CharField(null = True, max_length = 1, choices = AISLAMIENTO)
    arranque = models.CharField(null = True, max_length = 45)

class EspecificacionesBomba(models.Model):
    numero_curva = models.CharField(max_length = 10, null = True)
    velocidad = models.FloatField(null = True)
    velocidad_unidad = models.ForeignKey(Unidades, related_name="velocidad_unidad_especificacionesbomba")
    potencia_maxima = models.FloatField()
    potencia_unidad = models.ForeignKey(Unidades, related_name="potencia_unidad_especificacionesbomba")
    eficiencia = models.FloatField()

    cabezal_total = models.FloatField()
    cabezal_unidad = models.ForeignKey(Unidades, related_name="cabezal_unidad_especificacionesbomba")
    numero_etapas = models.SmallIntegerField()
    succion_id = models.FloatField()
    descarga_id = models.FloatField()
    id_unidad = models.ForeignKey(Unidades, related_name="id_unidad_especificacionesbomba")

class Bombas(models.Model):
    tag = models.CharField(max_length = 45, unique = True)
    descripcion = models.CharField(max_length = 80)
    fabricante = models.CharField(max_length = 45)
    modelo = models.CharField(max_length = 45, null = True)
    creado_al = models.DateTimeField()
    editado_al = models.DateTimeField(null = True)
    creado_por = models.ForeignKey(get_user_model())
    editado_por = models.ForeignKey(get_user_model(), null = True)
    tipo_bomba = models.ForeignKey(TipoBomba)
    detalle_motor = models.ForeignKey(DetallesMotor)
    especificaciones_bombre = models.ForeignKey(EspecificacionesBomba)

class DetallesConstruccion(models.Model):
    pass

class TipoCarcasaBomba(models.Model):
    pass

class TipoBombaConstruccion(models.Model):
    pass

# MODELOS DE VENTILADORES

# MODELOS DE PRECALENTADOR DE AGUA

# MODELOS DE ECONOMIZADORES

# MODELOS DE PRECALENTADOR DE AIRE