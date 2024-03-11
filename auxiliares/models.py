from django.db import models
from django.contrib.auth import get_user_model
from intercambiadores.models import Fluido, Planta, Unidades

# MODELOS DE BOMBAS

MOTOR_POSICIONES = (
    ('H', 'Horizontal'),
    ('V','Vertical')
)

LADOS_BOMBA = (
    ('S', 'Succión'),
    ('D', 'Descarga')
)

AISLAMIENTO = (
    ('F','CLASE F')
)

CORROSIVIDAD = (
    ('C', 'Corrosivo'),
    ('E', 'Erosivo'),
    ('N', 'No Errosivo ni Corrosivo'), 
    ('D', 'Desconocido')
)  

SI_NO_DESC = (
    ('S', 'Sí'),
    ('N', 'No'), 
    ('D', 'Desconocido')
)

CALCULO_PROPIEDADES = (
    ('M', 'Manual'),
    ('A', 'Automático')
)

class Material(models.Model):
    nombre = models.CharField(max_length = 45)
    rugosidad = models.FloatField()

class EspecificacionesInstalacion(models.Model):
    lado = models.CharField()
    elevacion_succion =  models.FloatField()
    elevacion_unidad = models.ForeignKey(Unidades, related_name="elevacion_unidad_especificacionesinstalacion")
    longitud_tuberia = models.FloatField(null = True)
    longitud_tuberia_unidad = models.CharField(max_length = 45)
    numero_codos_90 = models.IntegerField(null = True)
    numero_codos_90_rl = models.IntegerField(null = True, verbose_name="Número de Codos a 90°")
    numero_codos_90_ros = models.IntegerField(null = True)
    numero_codos_45 = models.IntegerField(null = True)
    numero_codos_45_ros = models.IntegerField(null = True)
    numero_codos_180 = models.IntegerField(null = True)
    conexiones_t_directo = models.IntegerField(null = True)
    conexiones_t_ramal = models.IntegerField(null = True)
    numero_valvulas_mariposa_2_8 = models.IntegerField(null = True)
    numero_valvulas_mariposa_10_14 = models.IntegerField(null = True)
    numero_valvulas_mariposa_16_24 = models.IntegerField(null = True)
    numero_contracciones_linea = models.IntegerField(null = True)
    numero_expansiones_linea = models.IntegerField(null = True)

class TipoCarcasaBomba(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

class TipoBombaConstruccion(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

class TipoBomba(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

class DetallesMotorBomba(models.Model):
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
    npshr = models.FloatField()
    npshr_unidad = models.ForeignKey(Unidades, related_name="npshr_unidad_especificacionesbomba")

    cabezal_total = models.FloatField()
    cabezal_unidad = models.ForeignKey(Unidades, related_name="cabezal_unidad_especificacionesbomba")
    numero_etapas = models.SmallIntegerField()
    succion_id = models.FloatField()
    descarga_id = models.FloatField()
    id_unidad = models.ForeignKey(Unidades, related_name="id_unidad_especificacionesbomba")
    material_tuberia = models.ForeignKey(Material)

class CondicionFluidoBomba(models.Model):
    temperatura_operacion = models.FloatField()
    presion_vapor = models.FloatField()
    temperatura_presion_vapor = models.FloatField()
    densidad_relativa = models.FloatField()
    viscosidad = models.FloatField()
    corrosividad = models.CharField(max_length = 1, choices = CORROSIVIDAD)
    peligroso = models.CharField(max_length = 1, choices = SI_NO_DESC)
    inflamable = models.CharField(max_length = 1, choices = SI_NO_DESC)
    concentracion_h2s = models.FloatField()
    concentracion_cloro = models.FloatField() 
    concentracion_unidad = models.ForeignKey(Unidades, related_name = "presion_unidad_condicionesfluido")
    nombre_fluido = models.CharField(max_length = 45, null = True)
    calculo_propiedades = models.CharField(max_length = 1, default = "M", choices=)
    fluido = models.ForeignKey(Fluido)

class CondicionesDisenoBomba(models.Model):
    capacidad = models.FloatField()
    presion_succion = models.FloatField()
    presion_descarga = models.FloatField()
    presion_diferencial_descarga = models.FloatField()
    presion_diferencial_succion = models.FloatField()
    presion_unidad = models.ForeignKey(Unidades, related_name="presion_unidad_condicionesdisenobomba")
    npsha = models.FloatField()
    condiciones_fluido = models.ForeignKey(CondicionFluidoBomba)

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

# MODELOS DE VENTILADORES

# MODELOS DE PRECALENTADOR DE AGUA

# MODELOS DE ECONOMIZADORES

# MODELOS DE PRECALENTADOR DE AIRE