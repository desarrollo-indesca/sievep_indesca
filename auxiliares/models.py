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
    ('F','CLASE F'),
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

class MaterialTuberia(models.Model):
    nombre = models.CharField(max_length = 45)
    rugosidad = models.FloatField()

class TipoCarcasaBomba(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

class TipoBombaConstruccion(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

class DetallesConstruccionBomba(models.Model):
    conexion_succion = models.PositiveIntegerField(null = True)
    tamano_rating_succion = models.FloatField(null = True)
    conexion_descarga = models.PositiveIntegerField(null = True)
    tamano_rating_descarga = models.FloatField(null = True)
    carcasa_dividida = models.CharField(max_length = 1, null = True, choices = CARCASA_DIVIDIDA)
    modelo = models.CharField(max_length = 45, null = True)
    fabricante_sello = models.CharField(max_length = 45, null = True)
    tipo = models.ForeignKey(TipoBombaConstruccion, on_delete=models.CASCADE, null = True)
    tipo_carcasa1 = models.ForeignKey(TipoCarcasaBomba, on_delete=models.CASCADE, null = True, related_name="tipo_carcasa_construccion1")
    tipo_carcasa2 = models.ForeignKey(TipoCarcasaBomba, on_delete=models.CASCADE, null = True, related_name="tipo_carcasa_construccion2")

class TipoBomba(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

class DetallesMotorBomba(models.Model):
    potencia = models.FloatField(null = True, verbose_name = "Potencia de la Bomba")
    potencia_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="potencia_unidad_detallesmotor")
    velocidad = models.FloatField(verbose_name="Velocidad del Motor (RPM)") # RPM
    velocidad_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="velocidad_unidad_detallesmotor")
    factor_de_servicio = models.FloatField(null = True)
    posicion = models.CharField(null = True, max_length = 1, choices = MOTOR_POSICIONES, verbose_name="Posición del Motor")
    voltaje = models.FloatField(null=True)
    voltaje_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="voltaje_unidad_detallesmotor")
    fases = models.PositiveSmallIntegerField(null = True)
    frecuencia = models.FloatField(null = True)
    frecuencia_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="frecuencia_unidad_detallesmotor")
    aislamiento = models.CharField(null = True, max_length = 1, choices = AISLAMIENTO)
    arranque = models.CharField(null = True, max_length = 45)

class EspecificacionesBomba(models.Model):
    numero_curva = models.CharField(max_length = 10, null = True)
    velocidad = models.FloatField(null = True)
    velocidad_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="velocidad_unidad_especificacionesbomba")
    potencia_maxima = models.FloatField()
    potencia_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="potencia_unidad_especificacionesbomba")
    eficiencia = models.FloatField()
    npshr = models.FloatField(null = True)
    npshr_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="npshr_unidad_especificacionesbomba")

    cabezal_total = models.FloatField()
    cabezal_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="cabezal_unidad_especificacionesbomba")
    numero_etapas = models.SmallIntegerField()
    
    succion_id = models.FloatField()
    descarga_id = models.FloatField()
    id_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="id_unidad_especificacionesbomba")

    material_tuberia = models.ForeignKey(MaterialTuberia, on_delete=models.CASCADE, null = True)

    entrada_proyectada_dentro_succion = models.PositiveIntegerField(null = True)
    entrada_bordes_afilados_succion = models.PositiveIntegerField(null = True)
    entrada_achaflamada_succion = models.PositiveIntegerField(null = True)
    salida = models.PositiveIntegerField(null = True)

class CondicionFluidoBomba(models.Model):
    temperatura_operacion = models.FloatField()
    presion_vapor = models.FloatField(null = True)
    temperatura_presion_vapor = models.FloatField(null = True)
    densidad_relativa = models.FloatField(null = True)
    temperatura_unidad = models.ForeignKey(Unidades, on_delete = models.CASCADE, related_name="temperatura_unidad_condicionesdisenobomba")
    viscosidad = models.FloatField(null = True)
    viscosidad_unidad = models.ForeignKey(Unidades, on_delete = models.CASCADE, related_name="viscosidad_unidad_condicionesdisenobomba")
    corrosividad = models.CharField(max_length = 1, choices = CORROSIVIDAD)
    peligroso = models.CharField(max_length = 1, choices = SI_NO_DESC)
    inflamable = models.CharField(max_length = 1, choices = SI_NO_DESC)
    concentracion_h2s = models.FloatField(null = True)
    concentracion_cloro = models.FloatField(null = True)
    concentracion_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name = "concentracion_unidad_condicionesfluido")
    nombre_fluido = models.CharField(max_length = 45, null = True)
    calculo_propiedades = models.CharField(max_length = 1, default = "M", choices=CALCULO_PROPIEDADES)
    presion_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="presion_unidad_condicionesfluido")
    fluido = models.ForeignKey(Fluido, on_delete=models.CASCADE)

class CondicionesDisenoBomba(models.Model):
    capacidad = models.FloatField()
    capacidad_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="capacidad_unidad_condicionesdisenobomba")
    presion_succion = models.FloatField()
    presion_descarga = models.FloatField()
    presion_diferencial = models.FloatField(null = True)
    presion_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="presion_unidad_condicionesdisenobomba")
    npsha = models.FloatField(null = True)
    npsha_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="npsha_unidad_condicionesdisenobomba")
    condiciones_fluido = models.OneToOneField(CondicionFluidoBomba, on_delete=models.CASCADE)

class Bombas(models.Model):
    tag = models.CharField(max_length = 45, unique = True)
    descripcion = models.CharField(max_length = 80)
    fabricante = models.CharField(max_length = 45)
    modelo = models.CharField(max_length = 45, null = True)
    creado_al = models.DateTimeField(auto_now = True)
    editado_al = models.DateTimeField(null = True)
    creado_por = models.ForeignKey(get_user_model(), on_delete = models.CASCADE, related_name="bomba_creada_por")
    editado_por = models.ForeignKey(get_user_model(), on_delete = models.CASCADE, related_name="bomba_editada_por", null = True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    tipo_bomba = models.ForeignKey(TipoBomba, on_delete=models.CASCADE)
    detalles_motor = models.OneToOneField(DetallesMotorBomba, on_delete=models.CASCADE)
    especificaciones_bomba = models.OneToOneField(EspecificacionesBomba, on_delete=models.CASCADE)
    detalles_construccion = models.OneToOneField(DetallesConstruccionBomba, on_delete=models.CASCADE)
    condiciones_diseno = models.OneToOneField(CondicionesDisenoBomba, on_delete=models.CASCADE)
    grafica = models.FileField(null = True)

class EspecificacionesInstalacion(models.Model):
    lado = models.CharField(max_length = 1, choices = LADOS_BOMBA)
    elevacion =  models.FloatField(null = True)
    elevacion_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="elevacion_unidad_especificacionesinstalacion")
    longitud_tuberia = models.FloatField(null = True)
    longitud_tuberia_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="longitud_tuberia_unidad_especificacionesinstalacion")

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

    bomba = models.ForeignKey(Bombas, on_delete=models.CASCADE)

# Evaluación de Bombas

# MODELOS DE VENTILADORES

# MODELOS DE PRECALENTADOR DE AGUA

# MODELOS DE ECONOMIZADORES

# MODELOS DE PRECALENTADOR DE AIRE