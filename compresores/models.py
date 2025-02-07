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
    """
    Resumen:
        Modelo que representa un compresor de gas. Contiene los datos generales del compresor,
        como su tag, descripción, fabricante y modelo, además de la planta y el tipo de compresor.

    Atributos:
        tag: CharField -> Tag único del compresor.
        descripcion: CharField -> Descripción del compresor.
        fabricante: CharField -> Fabricante del compresor.
        modelo: CharField -> Modelo del compresor.
        planta: ForeignKey -> Planta donde se encuentra el compresor.
        tipo: ForeignKey -> Tipo de compresor.
        creado_al: DateTimeField -> Fecha de creación del compresor.
        editado_al: DateTimeField -> Fecha de última edición del compresor.
        creado_por: ForeignKey -> Usuario que creó el compresor.
        editado_por: ForeignKey -> Usuario que editó por última vez el compresor.
    """
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
    compresor = models.ForeignKey(Compresor, on_delete=models.PROTECT) # IMPORTANTE: Varias Propiedades
    tipo_lubricacion = models.ForeignKey(TipoLubricacion, on_delete=models.PROTECT, null=True, blank=True)

class EtapaCompresor(models.Model):
    compresor = models.ForeignKey(Compresor, on_delete=models.PROTECT)
    numero = models.IntegerField()
    nombre_fluido = models.CharField(max_length=45, null=True, blank=True)
    flujo_masico = models.FloatField(null=True, blank=True)
    flujo_masico_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_flujo_masico_compresor")
    flujo_molar = models.FloatField(null=True, blank=True)
    flujo_molar_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_flujo_molar_compresor")
    densidad = models.FloatField(null=True, blank=True)
    densidad_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_densidad_compresor")
    aumento_estimado = models.FloatField(null=True, blank=True)
    rel_compresion = models.FloatField(null=True, blank=True)
    potencial_nominal = models.FloatField(null=True, blank=True)
    potencia_req = models.FloatField("Potencia Requerida", null=True, blank=True)
    potencia_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_potencia_etapa_compresor")
    eficiencia_isentropica = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    eficiencia_politropica = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    cabezal_politropico = models.FloatField(null=True, blank=True)
    cabezal_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_cabezal_compresor")
    humedad_relativa = models.FloatField(null=True, blank=True)
    volumen_diseno = models.FloatField(null=True, blank=True)
    volumen_normal = models.FloatField(null=True, blank=True)
    volumen_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_volumen_etapa_compresor")

    curva_caracteristica = models.FileField(null=True, blank=True)

class ComposicionGases(models.Model):
    porc_molar = models.FloatField(null=True, blank=True)

class LadoEtapaCompresor(models.Model):
    etapa = models.ForeignKey(EtapaCompresor, on_delete=models.PROTECT)
    lado = models.CharField(max_length=1, choices=LADOS_COMPRESOR)
    temp = models.FloatField(null=True, blank=True)
    temp_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_temp_etapa_compresor")
    presion = models.FloatField(null=True, blank=True)
    presion_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_presion_etapa_compresor")
    compresibilidad = models.FloatField(null=True, blank=True)
    cp_cv = models.FloatField(null=True, blank=True)
    n = models.FloatField(null=True, blank=True)