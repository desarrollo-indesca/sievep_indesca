from django.db import models
from django.contrib.auth import get_user_model
from intercambiadores.models import Planta, Complejo, Unidades
from django.core.validators import MinValueValidator, MaxValueValidator

LADOS_COMPRESOR= (
    ('I', 'Entrada'), 
    ('E', 'Salida')
)

# Create your models here.

class TipoCompresor(models.Model):
    nombre = models.CharField(max_length=45, unique=True)

class Compresor(models.Model):
    tag = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")
    fabricante = models.CharField(max_length=45, null=True, blank=True)
    modelo = models.CharField(max_length=45, null=True, blank=True)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT)
    tipo = models.ForeignKey(TipoCompresor, on_delete=models.PROTECT)
    creado_al = models.DateTimeField(auto_now_add=True)
    editado_al = models.DateTimeField(null=True)
    creado_por = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name="compresor_creado_por")
    editado_por = models.ForeignKey('auth.User', on_delete=models.PROTECT, null=True, related_name="compresor_editado_por")

class TipoLubricacion(models.Model):
    nombre = models.CharField(max_length=45, unique=True)

class PropiedadesCompresor(models.Model):
    numero_impulsores = models.IntegerField(null=True, blank=True)
    material_carcasa = models.CharField(max_length=45, null=True, blank=True)
    tipo_lubricante = models.CharField("Tipo de lubricante(ROT)", max_length=45, null=True, blank=True)
    tipo_sello = models.CharField(max_length=45, null=True, blank=True)
    velocidad_max_continua = models.FloatField(null=True, blank=True)
    velocidad_rotacion = models.FloatField(null=True, blank=True)
    unidad_velocidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_velocidad_compresor")
    potencia_requerida = models.FloatField(null=True, blank=True)
    unidad_potencia = models.ForeignKey(Unidades, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_potencia_compresor")
    compresor = models.ForeignKey(Compresor, on_delete=models.PROTECT)
    tipo_lubricacion = models.ForeignKey(TipoLubricacion, on_delete=models.PROTECT, null=True, blank=True)

class EtapaCompresor(models.Model):
    compresor = models.ForeignKey(Compresor, on_delete=models.PROTECT)
    numero = models.IntegerField()
    nombre_fluido = models.CharField(max_length=45, null=True, blank=True)
    flujo_masico = models.FloatField(null=True, blank=True)
    flujo_molar = models.FloatField(null=True, blank=True)
    densidad = models.FloatField(null=True, blank=True)
    aumento_estimado = models.FloatField(null=True, blank=True)
    velocidad_diseno = models.FloatField(null=True, blank=True)
    velocidad_normal = models.FloatField(null=True, blank=True)
    rel_compresion = models.FloatField(null=True, blank=True)
    potencial_nominal = models.FloatField(null=True, blank=True)
    potencia_req = models.FloatField("Potencia Requerida", null=True, blank=True)
    eficiencia_isentropica = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    eficiencia_politropica = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    cabezal_politropico = models.FloatField(null=True, blank=True)
    humedad_relativa = models.FloatField(null=True, blank=True)
    volumen_diseno = models.FloatField(null=True, blank=True)
    volumen_normal = models.FloatField(null=True, blank=True)

class ComposicionGases(models.Model):
    porc_molar = models.FloatField(null=True, blank=True)

class LadoEtapaCompresor(models.Model):
    etapa = models.ForeignKey(EtapaCompresor, on_delete=models.PROTECT)
    lado = models.CharField(max_length=1, choices=LADOS_COMPRESOR)
    temp = models.FloatField(null=True, blank=True)
    presion = models.FloatField(null=True, blank=True)
    compresibilidad = models.FloatField(null=True, blank=True)
    cp_cv = models.FloatField(null=True, blank=True)
    n = models.FloatField(null=True, blank=True)