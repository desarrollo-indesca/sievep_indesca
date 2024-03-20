from django.db import models
from django.contrib.auth import get_user_model
from intercambiadores.models import Fluido, Planta, Unidades
from calculos.utils import conseguir_largo
from simulaciones_pequiven.settings import MEDIA_ROOT

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
    ('A', 'Ambos'),
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

    def __str__(self) -> str:
        return self.nombre.upper()

class TipoCarcasaBomba(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

    def __str__(self) -> str:
        return self.nombre.upper()

class TipoBombaConstruccion(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

    def __str__(self) -> str:
        return self.nombre.upper()

class DetallesConstruccionBomba(models.Model):
    conexion_succion = models.PositiveIntegerField(null = True, blank = True, verbose_name = "Conexión de Succión")
    tamano_rating_succion = models.FloatField(null = True, blank = True, verbose_name = "Tamaño Rating (Succión)")
    conexion_descarga = models.PositiveIntegerField(null = True, blank = True, verbose_name = "Conexión de Descarga")
    tamano_rating_descarga = models.FloatField(null = True, blank = True, verbose_name = "Tamaño Rating (Descarga)")
    carcasa_dividida = models.CharField(max_length = 1, null = True, blank = True, choices = CARCASA_DIVIDIDA, verbose_name = "Carcasa Dividida")
    modelo_construccion = models.CharField(max_length = 45, null = True, blank = True, verbose_name = "Modelo de Construcción")
    fabricante_sello = models.CharField(max_length = 45, null = True, blank = True, verbose_name = "Fabricante de Sello")
    tipo = models.ForeignKey(TipoBombaConstruccion, on_delete=models.CASCADE, null = True, blank = True, verbose_name = "Tipo por Construcción")
    tipo_carcasa1 = models.ForeignKey(TipoCarcasaBomba, verbose_name = "Tipo de Carcasa (1)", on_delete=models.CASCADE, null = True, blank = True, related_name="tipo_carcasa_construccion1")
    tipo_carcasa2 = models.ForeignKey(TipoCarcasaBomba, verbose_name = "Tipo de Carcasa (2)", on_delete=models.CASCADE, null = True, blank = True, related_name="tipo_carcasa_construccion2")

    def carcasa_dividida_largo(self):
        return conseguir_largo(CARCASA_DIVIDIDA, self.carcasa_dividida)

class TipoBomba(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)

    def __str__(self) -> str:
        return self.nombre.upper()

class DetallesMotorBomba(models.Model):
    potencia_motor = models.FloatField(null = True, blank = True, verbose_name = "Potencia del Motor")
    potencia_motor_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="potencia_unidad_detallesmotor")
    velocidad_motor = models.FloatField(verbose_name="Velocidad del Motor") # RPM
    velocidad_motor_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="velocidad_unidad_detallesmotor")
    factor_de_servicio = models.FloatField(null = True, blank = True, verbose_name = "Factor de Servicio")
    posicion = models.CharField(null = True, blank = True, max_length = 1, choices = MOTOR_POSICIONES, verbose_name="Posición del Motor")
    voltaje = models.FloatField(null=True, verbose_name = "Voltaje del Motor")
    voltaje_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="voltaje_unidad_detallesmotor")
    fases = models.PositiveSmallIntegerField(null = True)
    frecuencia = models.FloatField(null = True)
    frecuencia_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="frecuencia_unidad_detallesmotor")
    aislamiento = models.CharField(null = True, blank = True, max_length = 1, choices = AISLAMIENTO)
    arranque = models.CharField(null = True, blank = True, max_length = 45)

    def posicion_largo(self):
        return conseguir_largo(MOTOR_POSICIONES, self.posicion)
    
    def aislamiento_largo(self):
        return conseguir_largo(AISLAMIENTO, self.aislamiento)

class EspecificacionesBomba(models.Model):
    numero_curva = models.CharField(max_length = 10, null = True, blank = True, verbose_name = "Número de Curva")
    velocidad = models.FloatField(null = True)
    velocidad_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="velocidad_unidad_especificacionesbomba")
    potencia_maxima = models.FloatField(verbose_name = "Potencia Máxima")
    potencia_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="potencia_unidad_especificacionesbomba")
    eficiencia = models.FloatField()
    npshr = models.FloatField(null = True, blank = True, verbose_name = "NPSHr")
    npshr_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="npshr_unidad_especificacionesbomba")

    cabezal_total = models.FloatField()
    cabezal_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="cabezal_unidad_especificacionesbomba")
    numero_etapas = models.SmallIntegerField(verbose_name = "Número de Etapas")
    
    succion_id = models.FloatField(verbose_name = "Diámetro Interno Succión")
    descarga_id = models.FloatField(verbose_name = "Diámetro Interno Descarga")
    id_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="id_unidad_especificacionesbomba")

class CondicionFluidoBomba(models.Model):
    temperatura_operacion = models.FloatField(verbose_name = "Temperatura de Operación*")
    presion_vapor = models.FloatField(null = True, blank = True, verbose_name = "Presión de Vapor")
    temperatura_presion_vapor = models.FloatField(null = True, blank = True, verbose_name = "Temperatura a la Presión de Vapor")
    densidad = models.FloatField(null = True)
    densidad_unidad = models.ForeignKey(Unidades, blank = True, on_delete = models.CASCADE, related_name="densidad_unidad_condicionesdisenobomba", null = True)
    temperatura_unidad = models.ForeignKey(Unidades, on_delete = models.CASCADE, related_name="temperatura_unidad_condicionesdisenobomba")
    viscosidad = models.FloatField(null = True)
    viscosidad_unidad = models.ForeignKey(Unidades, on_delete = models.CASCADE, related_name="viscosidad_unidad_condicionesdisenobomba")
    corrosividad = models.CharField(max_length = 1, choices = CORROSIVIDAD, verbose_name = "Corrosivo/Erosivo*")
    peligroso = models.CharField(max_length = 1, choices = SI_NO_DESC, verbose_name = "Peligroso*")
    inflamable = models.CharField(max_length = 1, choices = SI_NO_DESC, verbose_name = "Inflamable*")
    concentracion_h2s = models.FloatField(null = True, blank = True, verbose_name = "Concentración de H₂S")
    concentracion_cloro = models.FloatField(null = True, blank = True, verbose_name = "Concentración de Cloro")
    concentracion_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name = "concentracion_unidad_condicionesfluido")
    nombre_fluido = models.CharField(max_length = 45, null = True, blank = True)
    calculo_propiedades = models.CharField(max_length = 1, default = "M", choices=CALCULO_PROPIEDADES, verbose_name = "Cálculo de Propiedades")
    presion_vapor_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="presion_unidad_condicionesfluido")
    fluido = models.ForeignKey(Fluido, on_delete=models.CASCADE, verbose_name = "Fluido*")

    def corrosividad_largo(self):
        return conseguir_largo(CORROSIVIDAD, self.corrosividad)
    
    def peligroso_largo(self):
        return conseguir_largo(SI_NO_DESC, self.peligroso)
    
    def inflamable_largo(self):
        return conseguir_largo(SI_NO_DESC, self.inflamable)

class CondicionesDisenoBomba(models.Model):
    capacidad = models.FloatField(verbose_name = "Capacidad*")
    capacidad_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="capacidad_unidad_condicionesdisenobomba")
    presion_succion = models.FloatField(verbose_name = "Presión de Succión*")
    presion_descarga = models.FloatField(verbose_name = "Presión de Descarga*")
    presion_diferencial = models.FloatField(null = True, blank = True, verbose_name = "Presión Diferencial")
    presion_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="presion_unidad_condicionesdisenobomba")
    npsha = models.FloatField(null = True, blank = True, verbose_name = "NPSHa")
    npsha_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="npsha_unidad_condicionesdisenobomba")
    condiciones_fluido = models.OneToOneField(CondicionFluidoBomba, on_delete=models.CASCADE)

class EspecificacionesInstalacion(models.Model):
    elevacion =  models.FloatField(null = True)
    elevacion_unidad = models.ForeignKey(Unidades, default = 4, on_delete=models.CASCADE, related_name="elevacion_unidad_especificacionesinstalacion")
    longitud_tuberia = models.FloatField(null = True)
    longitud_tuberia_unidad = models.ForeignKey(Unidades, default = 4, on_delete=models.CASCADE, related_name="longitud_tuberia_unidad_especificacionesinstalacion")
    diametro_tuberia = models.FloatField(null = True)
    diametro_tuberia_unidad = models.ForeignKey(Unidades, default = 4, on_delete=models.CASCADE, related_name="diametro_tuberia_unidad_especificacionesinstalacion")

    numero_codos_90 = models.PositiveIntegerField(null = True)
    numero_codos_90_rl = models.PositiveIntegerField(null = True, blank = True, verbose_name="Número de Codos a 90°")
    numero_codos_90_ros = models.PositiveIntegerField(null = True)
    numero_codos_45 = models.PositiveIntegerField(null = True)
    numero_codos_45_ros = models.PositiveIntegerField(null = True)
    numero_codos_180 = models.PositiveIntegerField(null = True)
    conexiones_t_directo = models.PositiveIntegerField(null = True)
    conexiones_t_ramal = models.PositiveIntegerField(null = True)
    material_tuberia = models.ForeignKey(MaterialTuberia, on_delete=models.CASCADE, null = True)

    # VÁLVULAS COMPUERTA
    numero_valvulas_compuerta = models.PositiveIntegerField(null = True)
    numero_valvulas_compuerta_abierta_3_4 = models.PositiveIntegerField(null = True)
    numero_valvulas_compuerta_abierta_1_2 = models.PositiveIntegerField(null = True)
    numero_valvulas_compuerta_abierta_1_4 = models.PositiveIntegerField(null = True)

    # VÁLVULAS MARIPOSA
    numero_valvulas_mariposa_2_8 = models.PositiveIntegerField(null = True)
    numero_valvulas_mariposa_10_14 = models.PositiveIntegerField(null = True)
    numero_valvulas_mariposa_16_24 = models.PositiveIntegerField(null = True)

    # VÁLVULAS CHECK
    numero_valvula_giratoria = models.PositiveIntegerField(null = True)
    numero_valvula_bola = models.PositiveIntegerField(null = True)
    numero_valvula_vastago = models.PositiveIntegerField(null = True)
    numero_valvula_bisagra = models.PositiveIntegerField(null = True)

    # ACCESORIOS
    numero_valvula_globo = models.PositiveIntegerField(null = True)
    numero_valvula_angulo = models.PositiveIntegerField(null = True)
    
    numero_contracciones_linea = models.PositiveIntegerField(null = True)
    numero_expansiones_linea = models.PositiveIntegerField(null = True)

class Bombas(models.Model):
    tag = models.CharField(max_length = 45, unique = True, verbose_name = "Tag del Equipo*")
    descripcion = models.CharField(max_length = 80, verbose_name = "Descripción del Equipo*")
    fabricante = models.CharField(max_length = 45, verbose_name = "Fabricante*")
    modelo = models.CharField(max_length = 45, null = True, blank = True, verbose_name = "Modelo del Equipo")
    creado_al = models.DateTimeField(auto_now = True)
    editado_al = models.DateTimeField(null = True)
    creado_por = models.ForeignKey(get_user_model(), on_delete = models.CASCADE, related_name="bomba_creada_por")
    editado_por = models.ForeignKey(get_user_model(), on_delete = models.CASCADE, related_name="bomba_editada_por", null = True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    tipo_bomba = models.ForeignKey(TipoBomba, on_delete=models.CASCADE, default = 1, verbose_name = "Tipo de Bomba")
    detalles_motor = models.OneToOneField(DetallesMotorBomba, on_delete=models.CASCADE)
    especificaciones_bomba = models.OneToOneField(EspecificacionesBomba, on_delete=models.CASCADE)
    detalles_construccion = models.OneToOneField(DetallesConstruccionBomba, on_delete=models.CASCADE)
    condiciones_diseno = models.OneToOneField(CondicionesDisenoBomba, on_delete=models.CASCADE)
    grafica = models.ImageField(null = True, blank = True, upload_to=MEDIA_ROOT + 'auxiliares/bombas/', verbose_name = "Gráfica del Equipo")

    instalacion_succion = models.ForeignKey(EspecificacionesInstalacion, on_delete=models.CASCADE, related_name="instalacion_succion")
    instalacion_descarga = models.ForeignKey(EspecificacionesInstalacion, on_delete=models.CASCADE, related_name="instalacion_descarga")

    def __str__(self) -> str:
        return self.tag.upper()
    
    class Meta:
        ordering = ('tag',)

# Evaluación de Bombas

# MODELOS DE VENTILADORES

# MODELOS DE PRECALENTADOR DE AGUA

# MODELOS DE ECONOMIZADORES

# MODELOS DE PRECALENTADOR DE AIRE