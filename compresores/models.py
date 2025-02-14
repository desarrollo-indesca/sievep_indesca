from django.db import models
from django.contrib.auth import get_user_model
from intercambiadores.models import Planta, Fluido, Unidades
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator

LADOS_COMPRESOR= (
    ('I', 'Entrada'), 
    ('E', 'Salida')
)

# Create your models here.

class TipoCompresor(models.Model):
    nombre = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.nombre

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
    tag = models.CharField(max_length=20, unique=True, verbose_name="Tag")
    descripcion = models.CharField(max_length=100, verbose_name="Descripción del Compresor")
    fabricante = models.CharField(max_length=45, null=True, blank=True, verbose_name="Fabricante")
    modelo = models.CharField(max_length=45, null=True, blank=True, verbose_name="Modelo del Compresor")
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, verbose_name="Planta")
    tipo = models.ForeignKey(TipoCompresor, on_delete=models.PROTECT, verbose_name="Tipo de Compresor")
    creado_al = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    editado_al = models.DateTimeField(null=True, verbose_name="Fecha de Última Edición")
    creado_por = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name="compresor_creado_por", verbose_name="Creado por")
    editado_por = models.ForeignKey('auth.User', on_delete=models.PROTECT, null=True, related_name="compresor_editado_por", verbose_name="Editado por")
    copia = models.BooleanField(default=False, blank=True, verbose_name="Es Copia")

    curva_caracteristica = models.FileField(null=True, blank=True, upload_to="compresores/curvas-compresores/", verbose_name="Curva de Característica", validators=[FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'pdf']
    )])

    class Meta:
        ordering = ('tag',)

class TipoLubricacion(models.Model):
    nombre = models.CharField(max_length=45, unique=True)

class PropiedadesCompresor(models.Model):
    numero_impulsores = models.IntegerField(null=True, blank=True, verbose_name="Número de Impulsores")
    material_carcasa = models.CharField(max_length=45, null=True, blank=True, verbose_name="Material de la Carcasa")
    tipo_sello = models.CharField(max_length=45, null=True, blank=True, verbose_name="Tipo de Sello")
    velocidad_max_continua = models.FloatField(null=True, blank=True, verbose_name="Velocidad Máxima Continua")
    velocidad_rotacion = models.FloatField(null=True, blank=True, verbose_name="Velocidad de Rotación")
    unidad_velocidad = models.ForeignKey(Unidades, default=52, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_velocidad_compresor", verbose_name="Unidad de la Velocidad")
    potencia_requerida = models.FloatField(null=True, blank=True, verbose_name="Potencia Requerida")
    unidad_potencia = models.ForeignKey(Unidades, default=53, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_potencia_compresor", verbose_name="Unidad de la Potencia")
    compresor = models.ForeignKey(Compresor, on_delete=models.PROTECT, related_name="casos", verbose_name="Compresor") # IMPORTANTE: Varias Propiedades
    tipo_lubricacion = models.ForeignKey(TipoLubricacion, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de Lubricación")

class EtapaCompresor(models.Model):
    compresor = models.ForeignKey(PropiedadesCompresor, on_delete=models.PROTECT, related_name='etapas', verbose_name="Compresor")
    numero = models.IntegerField(verbose_name="Número")
    nombre_fluido = models.CharField(max_length=45, null=True, blank=True, verbose_name="Nombre del Gas")
    flujo_masico = models.FloatField(null=True, blank=True, verbose_name="Flujo Másico")
    flujo_masico_unidad = models.ForeignKey(Unidades, default=54, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_flujo_masico_compresor", verbose_name="Unidad")
    flujo_molar = models.FloatField(null=True, blank=True, verbose_name="Flujo Molar")
    flujo_molar_unidad = models.ForeignKey(Unidades, default=94, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_flujo_molar_compresor", verbose_name="Unidad")
    densidad = models.FloatField(null=True, blank=True, verbose_name="Densidad")
    densidad_unidad = models.ForeignKey(Unidades, on_delete=models.PROTECT, default=43, null=True, blank=True, related_name="unidad_densidad_compresor", verbose_name="Unidad")
    aumento_estimado = models.FloatField(null=True, blank=True, verbose_name="Aumento Estimado")
    rel_compresion = models.FloatField(null=True, blank=True, verbose_name="Relación de Compresión")
    potencia_nominal = models.FloatField(null=True, blank=True, verbose_name="Potencia Nominal")
    potencia_req = models.FloatField(null=True, blank=True, verbose_name="Potencia Requerida")
    potencia_unidad = models.ForeignKey(Unidades, default=53, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_potencia_etapa_compresor", verbose_name="Unidad")
    eficiencia_isentropica = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], verbose_name="Eficiencia Isentrópica")
    eficiencia_politropica = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], verbose_name="Eficiencia Politrópica")
    cabezal_politropico = models.FloatField(null=True, blank=True, verbose_name="Cabezal Politrópico")
    cabezal_unidad = models.ForeignKey(Unidades, default=4, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_cabezal_compresor", verbose_name="Unidad")
    humedad_relativa = models.FloatField(null=True, blank=True, verbose_name="Humedad Relativa (%)", validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    volumen_diseno = models.FloatField(null=True, blank=True, verbose_name="Volumen de Diseño")
    volumen_normal = models.FloatField(null=True, blank=True, verbose_name="Volumen Normal")
    volumen_unidad = models.ForeignKey(Unidades, default=34, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_volumen_etapa_compresor", verbose_name="Unidad")
    
    curva_caracteristica = models.FileField("Curva Característica", null=True, blank=True, upload_to='compresores/curvas-etapas/', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'pdf'])
    ])

    class Meta:
        ordering = ('numero', )

class ComposicionGases(models.Model):
    etapa = models.ForeignKey(
        EtapaCompresor, 
        on_delete=models.PROTECT, 
        related_name='composiciones', 
        verbose_name="Etapa del Compresor"
    )
    porc_molar = models.FloatField(
        null=True, 
        blank=True, 
        verbose_name="Porcentaje Molar"
    )
    compuesto = models.ForeignKey(
        Fluido, 
        on_delete=models.CASCADE, 
        verbose_name="Compuesto"
    )

class LadoEtapaCompresor(models.Model):
    etapa = models.ForeignKey(EtapaCompresor, on_delete=models.PROTECT, related_name='lados', verbose_name="Etapa del Compresor")
    lado = models.CharField(max_length=1, choices=LADOS_COMPRESOR, verbose_name="Lado del Compresor")
    temp = models.FloatField(null=True, blank=True, verbose_name="Temperatura")
    temp_unidad = models.ForeignKey(Unidades, default=1, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_temp_etapa_compresor", verbose_name="Unidad de Temperatura")
    presion = models.FloatField(null=True, blank=True, verbose_name="Presión")
    presion_unidad = models.ForeignKey(Unidades, default=7, on_delete=models.PROTECT, null=True, blank=True, related_name="unidad_presion_etapa_compresor", verbose_name="Unidad de Presión")
    compresibilidad = models.FloatField(null=True, blank=True, verbose_name="Compresibilidad")
    cp_cv = models.FloatField(null=True, blank=True, verbose_name="Relación Cp/Cv")

# MODELOS DE EVALUACIÓN

# TODO