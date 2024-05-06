from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from intercambiadores.models import Unidades, Planta, Complejo

# Create your models here.

FASES_CORRIENTES = (
    ('S','Saturado'),
    ('L','Líquido'),
    ('V','Vapor'),
    ('O', 'Sólido')
)

class DatosCorrientes(models.Model):
    flujo_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="flujo_unidad_corriente")
    entalpia_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="entalpia_unidad_corriente")
    presion_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="presion_unidad_corriente")
    temperatura_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="temperatura_unidad_corriente")

class Corriente(models.Model):
    numero_corriente = models.CharField('Número Corriente', max_length=10)
    descripcion_corriente = models.CharField('Descripción de la Corriente', max_length=50)

    flujo = models.FloatField(validators=[MinValueValidator(0.00001)])
    entalpia = models.FloatField(validators=[MinValueValidator(0.00001)])
    presion = models.FloatField(validators=[MinValueValidator(0.00001)])
    temperatura = models.FloatField(validators=[MinValueValidator(-273.15)])

    fase = models.CharField(max_length=1, choices=FASES_CORRIENTES)
    entrada = models.BooleanField()
    datos_corriente = models.ForeignKey(DatosCorrientes, on_delete=models.PROTECT)

class GeneradorElectrico(models.Model):
    polos = models.PositiveSmallIntegerField()
    fases = models.PositiveSmallIntegerField()
    
    ciclos = models.FloatField(validators=[MinValueValidator(0.0)])
    ciclos_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="ciclos_unidad_generador")

    potencia_real = models.FloatField(validators=[MinValueValidator(0.000001)])
    potencia_real_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="potencia_real_unidad_generador")

    potencia_aparente = models.FloatField(validators=[MinValueValidator(0.000001)])
    potencia_aparente_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="potencia_aparente_unidad_generador")

    velocidad = models.FloatField(validators=[MinValueValidator(0.000001)])
    velocidad_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="velocidad_unidad_generador")
    
    corriente_electrica = models.FloatField('Corriente Eléctrica', validators=[MinValueValidator(0.000001)])
    corriente_electrica = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="corriente_electrica_generador")

    voltaje = models.FloatField(validators=[MinValueValidator(0.000001)])
    voltaje_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="voltaje_unidad_generador")   

class EspecificacionesTurbinaVapor(models.Model):
    potencia = models.FloatField(validators=[MinValueValidator(0.000001)])
    potencia_max = models.FloatField(validators=[MinValueValidator(0.000001)])
    potencia_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="potencia_unidad_turbinavapor")

    velocidad = models.FloatField(validators=[MinValueValidator(0.000001)])
    velocidad_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="velocidad_unidad_turbinavapor")

    presion_entrada = models.FloatField(validators=[MinValueValidator(0.000001)]) # MANOMÉTRICA
    presion_entrada = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="presion_entrada_turbinavapor")

    temperatura_entrada = models.FloatField(validators=[MinValueValidator(0.000001)])
    temperatura_entrada = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="temperatura_entrada_turbinavapor")

    contra_presion = models.FloatField(validators=[MinValueValidator(0.000001)]) # ABSOLUTA
    contra_presion_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="contra_presion_unidad_turbinavapor")

    eficiencia = models.FloatField(null = True)

class TurbinaVapor(models.Model):
    # Identificación de la turbina
    tag = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField('Descripción', max_length=100)
    fabricante = models.CharField(max_length=45)
    modelo = models.CharField(max_length=45, null = True)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT)

    # Atributos de la Turbina de Vapor
    generador_electrico = models.OneToOneField(GeneradorElectrico, on_delete=models.PROTECT)
    especificaciones = models.OneToOneField(EspecificacionesTurbinaVapor, on_delete=models.PROTECT)
    datos_corrientes = models.OneToOneField(DatosCorrientes, on_delete=models.PROTECT)

    # Datos de trazabilidad
    creado_por = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="turbina_creada_por")
    editado_por = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null = True, related_name="turbina_editada_por")
    creado_al = models.DateTimeField(auto_now_add=True)
    editado_al = models.DateTimeField(null = True)

    class Meta:
        ordering = ('tag',)

## Modelos de Evaluación

class EntradaEvaluacion(models.Model):
    flujo_entrada = models.FloatField(validators=[MinValueValidator(0.00001)])
    flujo_entrada_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="flujo_entrada_unidad_entradaevaluacion")
    potencia_real = models.FloatField(validators=[MinValueValidator(0.00001)])
    potencia_real_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT)

    # Para las entradas de corrientes:
    presion_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="presion_unidad_entrada_evaluacion_turbina")
    temperatura_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, related_name="temperatura_unidad_entrada_evaluacion")

class EntradaCorriente(models.Model):
    presion = models.FloatField()
    temperatura = models.FloatField(validators=[MinValueValidator(-273.15)])
    corriente = models.ForeignKey(Corriente, on_delete=models.PROTECT)
    entrada = models.ForeignKey(EntradaEvaluacion, on_delete=models.PROTECT)

class SalidaEvaluacion(models.Model):
    eficiencia = models.FloatField()
    potencia_calculada = models.FloatField()

    entalpia_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT)

class SalidaCorriente(models.Model):
    flujo = models.FloatField()
    entalpia = models.FloatField()
    fase = models.CharField(max_length=1, choices=FASES_CORRIENTES)
    corriente = models.ForeignKey(Corriente, on_delete=models.PROTECT)
    salida = models.ForeignKey(SalidaEvaluacion, on_delete=models.PROTECT)

class Evaluacion(models.Model):
    equipo = models.ForeignKey(TurbinaVapor, on_delete=models.PROTECT)
    creado_por = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    nombre = models.CharField(max_length=45)
    fecha = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    entrada = models.OneToOneField(EntradaEvaluacion, on_delete=models.PROTECT)
    salida = models.OneToOneField(SalidaEvaluacion, on_delete=models.PROTECT)

    class Meta:
        ordering = ('-fecha',)
