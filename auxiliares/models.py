from django.db import models
from django.contrib.auth import get_user_model
from intercambiadores.models import Fluido, Planta, Unidades


# CONSTANTES DE SELECCIÓN

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

CARCASA_DIVIDIDA = (
    ('A', 'Axial'),
    ('R', 'Radial')
)

# MODELOS DE BOMBAS

class Material(models.Model):
    nombre = models.CharField(max_length = 45)
    rugosidad = models.FloatField()

class EspecificacionesInstalacion(models.Model):
    lado = models.CharField()
    elevacion_succion =  models.FloatField()
    elevacion_unidad = models.ForeignKey(Unidades, related_name="elevacion_unidad_especificacionesinstalacion")
    longitud_tuberia = models.FloatField(null = True)
    longitud_tuberia_unidad = models.CharField(max_length = 45)

    numero_codos_90 = models.PositiveIntegerField(null = True)
    numero_codos_90_rl = models.PositiveIntegerField(null = True, verbose_name="Número de Codos a 90°")
    numero_codos_90_ros = models.PositiveIntegerField(null = True)
    numero_codos_45 = models.PositiveIntegerField(null = True)
    numero_codos_45_ros = models.PositiveIntegerField(null = True)
    numero_codos_180 = models.PositiveIntegerField(null = True)
    conexiones_t_directo = models.PositiveIntegerField(null = True)
    conexiones_t_ramal = models.PositiveIntegerField(null = True)

    # VÁLVULAS COMPUERTA
    numero_valvulas_compuerta = models.PositiveIntegerField(null = True)
    numero_valvulas_compuerta_abierta_3_4 = models.PositiveIntegerField(null = True)
    numero_valvulas_compuerta_abierta_1_2 = models.PositiveIntegerField(null = True)
    numero_valvulas_compuerta_abierta_1_4 = models.PositiveIntegerField(null = True)

    # VÁLVULAS MARIPOSA
    numero_valvulas_mariposa_2_8 = models.PositiveIntegerField(null = True)
    numero_valvulas_mariposa_2_8_abiertas = models.PositiveIntegerField(null = True)
    numero_valvulas_mariposa_10_14 = models.PositiveIntegerField(null = True)
    numero_valvulas_mariposa_10_14_abiertas = models.PositiveIntegerField(null = True)
    numero_valvulas_mariposa_16_24 = models.PositiveIntegerField(null = True)
    numero_valvulas_mariposa_16_24_abiertas = models.PositiveIntegerField(null = True)

    # VÁLVULAS CHECK
    numero_valvula_giratoria = models.PositiveIntegerField(null = True)
    numero_valvula_bola = models.PositiveIntegerField(null = True)
    numero_valvula_vastago = models.PositiveIntegerField(null = True)
    numero_valvula_bisagra = models.PositiveIntegerField(null = True)

    # ACCESORIOS
    numero_valvula_globo = models.PositiveIntegerField(null = True)
    numero_valvula_globo_abiertas = models.PositiveIntegerField(null = True)
    numero_valvula_angulo = models.PositiveIntegerField(null = True)
    numero_valvula_angulo_abiertas = models.PositiveIntegerField(null = True)
    
    numero_contracciones_linea = models.PositiveIntegerField(null = True)
    numero_expansiones_linea = models.PositiveIntegerField(null = True)

class TipoCarcasaBomba(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

class TipoBombaConstruccion(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

class DetallesConstruccionBomba(models.Model):
    conexion_succion = models.PositiveIntegerField(null = True)
    tamano_rating_succion = models.FloatField(null = True)
    conexion_descarga = models.PositiveIntegerField(null = True)
    tamano_rating_descarga = models.FloatField(null = True)
    carcasa_dividida = models.CharField(max_length = 1, null = True, choices = CALCULO_PROPIEDADES)
    modelo = models.CharField(max_length = 45, null = True)
    fabricante_sello = models.CharField(max_length = 45, null = True)
    tipo = models.ForeignKey(TipoBombaConstruccion)
    tipo_carcasa1 = models.ForeignKey(TipoCarcasaBomba, related_name="tipo_carcasa_construccion1")
    tipo_carcasa2 = models.ForeignKey(TipoCarcasaBomba, related_name="tipo_carcasa_construccion2")

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
    fases = models.PositiveSmallIntegerField(null = True)
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

    entrada_proyectada_dentro_succion = models.PositiveIntegerField(null = True)
    entrada_bordes_afilados_succion = models.PositiveIntegerField(null = True)
    entrada_achaflamada_succion = models.PositiveIntegerField(null = True)
    salida = models.PositiveIntegerField(null = True)

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
    calculo_propiedades = models.CharField(max_length = 1, default = "M", choices=CALCULO_PROPIEDADES)
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
    planta = models.ForeignKey(Planta)
    tipo_bomba = models.ForeignKey(TipoBomba)
    detalles_motor = models.OneToOneField(DetallesMotorBomba)
    especificaciones_bomba = models.OneToOneField(EspecificacionesBomba)
    especificaciones_instalacion = models.OneToOneField(EspecificacionesInstalacion)
    detalles_construccion = models.OneToOneField(DetallesConstruccionBomba)
    condiciones_diseno = models.OneToOneField(CondicionesDisenoBomba)
    grafica = models.FileField(null = False)

# Evaluación de Bombas

# MODELOS DE VENTILADORES

# MODELOS DE PRECALENTADOR DE AGUA

# MODELOS DE ECONOMIZADORES

# MODELOS DE PRECALENTADOR DE AIRE