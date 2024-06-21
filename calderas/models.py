from django.db import models
from django.contrib.auth import get_user_model

from intercambiadores.models import Planta, Fluido, Unidades

# Create your models here.

class Tambor(models.Model):
    """
    Resumen:
        Modelo que tiene la información general del tambor de la caldera

    Atributos:
        presion_operacion: models.FloatField -> Presión de operación
        temp_operacion: models.FloatField -> Temp. de Operación
        presion_diseno: models.FloatField -> Presión de diseño
        temp_diseno: models.FloatField -> Temp. de diseño
        material: models.CharField -> Material del tambor
        temperatura_unidad: Unidades -> Unidades de las magnitudes asociadas
        presion_unidad: Unidades -> Unidades de las magnitudes asociadas
    """

    presion_operacion = models.FloatField(null=True, blank = True)
    temp_operacion = models.FloatField(null=True, blank = True)
    presion_diseno = models.FloatField(null=True, blank = True)
    temp_diseno = models.FloatField(null=True, blank = True)
    material = models.CharField(max_length=45, null=True, blank = True)

    temperatura_unidad = models.ForeignKey(Unidades, models.PROTECT, default=1, related_name="temperatura_unidad_tambor")
    presion_unidad = models.ForeignKey(Unidades, models.PROTECT, default=33, related_name="presion_unidad_tambor")

class SeccionTambor(models.Model):
    """
    Resumen:
        Modelo que tiene la información de las dimensiones de una sección del tambor (superior o inferior)

    Atributos:
        seccion: models.CharField -> 'I' para inferior, 'S' para superior. Constante SECCIÓN
        diametro: models.FloatField -> Diámetro de la sección del tambor
        longitud: models.FloatField -> Longitud de la sección del tambor
        tambor: Tambor -> Tambor al que está asociado el lado
        dimensiones_unidad: Unidades -> Unidades de las dimensiones
    """

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
    """
    Resumen:
        Modelo que tiene la información de las dimensiones del sobrecalentador.

    Atributos:
        area_total_transferencia: models.FloatField -> Área total de transferencia
        diametro_tubos: models.FloatField -> Diámetro de los tubos
        num_tubos: models.FloatField -> Número de tubos en el sobrecalentador
        area_unidad: models.FloatField -> Unidades de la propiedad correspondiente
        diametro_unidad: models.FloatField -> Unidades de la propiedad correspondiente
    """

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
    """
    Resumen:
        Modelo que tiene la información general del sobrecalentador de la caldera.

    Atributos:
        presion_operacion: models.FloatField -> Presión de operación
        temp_operacion: models.FloatField -> Temperatura de operación
        presion_diseno: models.FloatField -> Presión de diseño
        flujo_max_continuo: models.FloatField -> Flujo máximo continuo (válido para el sobrecalentador)
        dims: DimsSobrecalentador -> Dimensiones del sobrecalentador
        temperatura_unidad: Unidades -> Unidad de la magnitud correspondiente
        presion_unidad: Unidades -> Unidad de la magnitud correspondiente
        flujo_unidad: Unidades -> Unidad de la magnitud correspondiente  
    """
    presion_operacion = models.FloatField(null=True, blank=True)
    temp_operacion = models.FloatField(null=True, blank=True)
    presion_diseno = models.FloatField(null=True, blank=True)
    flujo_max_continuo = models.FloatField(null=True, blank=True)

    dims = models.OneToOneField(DimsSobrecalentador, models.PROTECT)

    temperatura_unidad = models.ForeignKey(Unidades, models.PROTECT, default=1, related_name="temperatura_unidad_sobrecalentador")
    presion_unidad = models.ForeignKey(Unidades, models.PROTECT, default=33, related_name="presion_unidad_sobrecalentador")
    flujo_unidad = models.ForeignKey(Unidades, models.PROTECT, default=6, related_name="flujo_unidad_sobrecalentador")

class DimensionesCaldera(models.Model):
    """
    Resumen:
        Modelo que tiene la información de las dimensiones de la caldera.

    Atributos:
        ancho: models.FloatField -> Ancho de la caldera
        largo: models.FloatField -> Largo de la caldera
        alto: models.FloatField -> Alto de la caldera
        dimensiones_unidad: Unidades -> Dimensión         
    """
    ancho = models.FloatField(null=True, blank=True)
    largo = models.FloatField(null=True, blank=True)
    alto = models.FloatField(null=True, blank=True)
    dimensiones_unidad = models.ForeignKey(Unidades, models.PROTECT, default=4)

class EspecificacionesCaldera(models.Model):
    """
    Resumen:
        Modelo que contiene la información específica de las calderas.

    Atributos:
        material: models.CharField -> Material de la caldera 
        area_transferencia_calor: models.FloatField -> Área de transferencia de calor de la caldera
        area_unidad: Unidades -> Unidad del área de transferencia 
        calor_intercambiado: models.FloatField -> Calor intercambiado por la caldera
        calor_unidad: Unidades -> Unidad del calor intercambiado
        capacidad: models.FloatField -> Capacidad de la caldera 
        capacidad_unidad: Unidades -> Unidad de la capacidad de la caldera 
        temp_diseno: models.FloatField -> Temperatura de diseño
        temp_operacion: models.FloatField -> Temperatura de operación
        temperatura_unidad: models.FloatField -> Unidad de las temperaturas
        presion_diseno: models.FloatField -> Presión de diseño
        presion_operacion: models.FloatField -> Presión de operación
        presion_unidad: models.FloatField ->  Unidad de las presiones
        carga: models.FloatField -> Carga de la caldera
        carga_unidad: models.FloatField ->  Unidad de la carga de la caldera
        eficiencia_termica: models.FloatField -> Eficiencia térmica de la caldera por diseño
    """
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
    """
    Resumen:
        Modelo que contiene la información general del combustible de la caldera.

    Atributos:
        nombre_gas: models.CharField -> Nombre del combustible gas (requerido)
        liquido: models.BooleanField -> ¿Hay una parte líquida en el combustible?
        nombre_liquido: models.CharField -> Nombre del combustible líquido
    """
    nombre_gas = models.CharField(max_length=45)
    liquido = models.BooleanField()
    nombre_liquido = models.CharField(max_length=45, null=True, blank = True)

class ComposicionCombustible(models.Model):
    """
    Resumen:
        Modelo que contiene la información de la composición de un fluido en el combustible.

    Atributos:
        porc_vol: models.FloatField -> Porcentaje de volumen del compuesto
        porc_aire: models.FloatField -> Porcentaje de volumen de aire del compuesto
        combustible: models.FloatField -> Combustible al cual está asociado la composición
        fluido: models.FloatField -> Fluido o Compuesto puro de la composición
    """
    porc_vol = models.FloatField()
    porc_aire = models.FloatField()
    combustible = models.ForeignKey(Combustible, models.PROTECT)
    fluido = models.ForeignKey(Fluido, models.PROTECT)

class Chimenea(models.Model):
    """
    Resumen:
        Modelo que contiene la información general de las dimensiones de la chimenea de la caldera.

    Atributos:
        diametro: models.FloatField -> Diámetro de la chimenea
        altura: models.FloatField -> Altura de la chimenea
        dimensiones_unidad: Unidades -> Unidad para las dimensiones
    """
    diametro = models.FloatField(null=True, blank = True)
    altura = models.FloatField(null=True, blank = True)
    dimensiones_unidad = models.ForeignKey(Unidades, models.PROTECT, default=4)

class Economizador(models.Model):
    """
    Resumen:
        Modelo que contiene la información general de las dimensiones del economizador en la caldera.

    Atributos:
        area_total_transferencia: models.FloatField -> Área total de transferencia del economizador
        diametro_tubos: models.FloatField -> Diámetro de los tubos
        numero_tubos: models.IntegerField -> Número de los tubos
        area_unidad: Unidades -> Unidad para las medidas de área
        diametro_unidad: Unidades -> Unidad para las medidas de los diámetros
    """
    area_total_transferencia = models.FloatField(null=True, blank = True)
    diametro_tubos = models.FloatField(null=True, blank = True)
    numero_tubos = models.IntegerField(null=True)

    area_unidad = models.ForeignKey(Unidades, models.PROTECT, default=3, related_name="area_unidad_economizador")
    diametro_unidad = models.ForeignKey(Unidades, models.PROTECT, default=4, related_name="diametro_unidad_economizador")

class Caldera(models.Model):
    """
    Resumen:
        Modelo que contiene la información general de identificación de Calderas. Es el modelo central de las calderas.

    Atributos:
        planta: models.ForeignKey -> Planta o Instalación donde se encuentra el equipo.
        tag: models.CharField -> Etiqueta única de identificación del equipo.
        descripcion: models.CharField -> Descripción de las funciones del equipo.
        fabricante: models.CharField -> Fabricante del equipo según ficha.
        modelo: models.CharField -> Modelo de la caldera.
        tipo_caldera: models.CharField -> Descripción del tipo de la caldera.
        accesorios: models.CharField -> Marca de los accesorios de la caldera.
        sobrecalentador: Sobrecalentador -> Sobrecalentador asociado a la caldera.
        tambor: Tambor -> Tambor asociado a la caldera.  
        dimensiones: DimensionesCaldera -> Dimensiones de la caldera.  
        especificaciones: EspecificacionesCalderas -> Especificaciones asociadas a la caldera.  
        combustible: Combustible -> Información del combustible utilizado en la caldera.  
        chimenea: Chimenea -> Datos de la chimenea asociada a la caldera. 
        economizador: Economizador -> Datos del economizador asociado a la caldera.  
        creado_al: models.DateTimeField -> Fecha y hora de creación de la caldera.
        editado_al: models.DateTimeField ->  Fecha y hora de última edición de la caldera.
        creado_por: models.ForeignKey -> Usuario que creó la caldera
        editado_por: models.ForeignKey ->  Usuario que editó por última vez la caldera
    """

    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, related_name="planta_caldera")
    tag = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")
    fabricante = models.CharField(max_length=45, null = True, blank = True)
    modelo = models.CharField(max_length=45, null = True, blank = True)
    tipo_caldera = models.CharField(max_length=50, null = True, blank = True)
    accesorios = models.CharField(max_length=45, null = True, blank = True)

    sobrecalentador = models.OneToOneField(Sobrecalentador, models.CASCADE)
    tambor = models.OneToOneField(Tambor, models.PROTECT)
    dimensiones = models.OneToOneField(DimensionesCaldera, models.PROTECT)
    especificaciones = models.OneToOneField(EspecificacionesCaldera, models.PROTECT)
    combustible = models.OneToOneField(Combustible, models.PROTECT)
    chimenea = models.OneToOneField(Chimenea, models.PROTECT)
    economizador = models.OneToOneField(Economizador, models.PROTECT)

    creado_al = models.DateTimeField(auto_now_add=True)
    editado_al = models.DateTimeField(null = True)
    creado_por = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="caldera_creada_por")
    editado_por = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null = True, related_name="caldera_editada_por")

class Caracteristica(models.Model):
    """
    Resumen:
        Modelo que contiene la información general de una característica

    Atributos:
        nombre: models.CharField -> Nombre de la característica
        tipo_unidad: models.CharField -> Tipo de Unidad asociada
        caldera: Caldera -> Caldera en la que se encuentra la característica
    """
    nombre = models.CharField(max_length=45)
    tipo_unidad = models.CharField(max_length=1)
    caldera = models.ForeignKey(Caldera, on_delete=models.PROTECT)

class ValorPorCarga(models.Model):
    """
    Resumen:
        Modelo que contiene la información del valor de una característica de la caldera por carga.

    Atributos:
        carga: models.FloatField -> Valor (PORCENTUAL) de la carga
        valor_num: models.FloatField -> Valor de la característica
        caracteristica: Caracteristica -> Característica a la que está asociado el valor y la carga
        unidad: Unidades -> Unidad de medida de la magnitud de la característica
    """
    carga = models.FloatField()
    valor_num = models.FloatField()
    caracteristica = models.ForeignKey(Caracteristica, models.PROTECT)
    unidad = models.ForeignKey(Unidades, models.PROTECT)

class Corriente(models.Model):
    """
    Resumen:
        Modelo que contiene la información general de las corrientes que circulan por la caldera.

    Atributos:
        TIPOS_CORRIENTES: list -> Lista de los tipos de corrientes que deben ser registrados en la caldera.

        numero: models.CharField -> Número asociado a la corriente.
        nombre: models.CharField -> Nombre asociado de la corriente.
        tipo: models.CharField -> Tipo de corriente registrada.
        flujo_masico: models.FloatField -> Flujo másico circulante
        flujo_masico_unidad: Unidades -> Unidad asociada al flujo másico
        densidad: models.FloatField -> Densidad del fluido circulante
        densidad_unidad: Unidades -> Unidad asociada a la densidad
        estado: models.CharField -> Estado (L o V) del fluido
        temp_operacion: models.FloatField -> Temperatura de operación de la corriente
        temp_operacion_unidad: Unidades -> Unidad de la temperatura de operación
        presion: models.FloatField -> Presión bajo la que está sometida la corriente 
        presion_unidad: Unidades -> Unidad de la presión
        caldera: Caldera -> Caldera de la corriente
    """

    TIPOS_CORRIENTES = [
        ('A', "Vapor de Alta Presión"),
        ('W', "Agua"),
        ('P', "Purga"),
        ('B', "Vapor de Baja Presión"),
    ]

    numero = models.CharField(max_length=20, null=True)
    nombre = models.CharField(max_length=55, null=True)
    tipo = models.CharField(max_length=1, choices=TIPOS_CORRIENTES)

    flujo_masico = models.FloatField(null=True)
    flujo_masico_unidad = models.ForeignKey(Unidades, models.PROTECT, default=6, related_name="flujomasico_unidad_corriente_calderas")
    densidad = models.FloatField(null=True, blank=True)
    densidad_unidad = models.ForeignKey(Unidades, models.PROTECT, default=43, related_name="densidad_unidad_corriente_corriente_calderas")
    estado = models.CharField(max_length=1, choices=[('L','Líquido'), ('V', 'Vapor')], null=True, blank=True)
    temp_operacion = models.FloatField(null=True, blank=True)
    temp_operacion_unidad = models.ForeignKey(Unidades, models.PROTECT, default=1, related_name="temp_operacion_unidad_corriente_calderas")
    presion = models.FloatField(null=True)
    presion_unidad = models.ForeignKey(Unidades, models.PROTECT, default=1, related_name="presion_unidad_corriente_calderas")
    caldera = models.ForeignKey(Caldera, on_delete=models.PROTECT)

## EVALUACIONES
class SalidaBalanceEnergia(models.Model):
    """
    Resumen:
        Modelo que contiene la información de balances de energía de salida de una evaluación.
    
    Atributos:
        energia_entrada_gas: models.FloatField -> Energía de entrada del combustible gas
        energia_entrada_aire: models.FloatField -> Energía de entrada del aire
        energia_total_entrada: models.FloatField -> Energía de entrada total
        energia_total_reaccion: models.FloatField -> Energía total de la reacción
        energia_horno: models.FloatField -> Energía total del horno
        energia_unidad: Unidades -> Unidad de Energía
    """
    energia_entrada_gas = models.FloatField()
    energia_entrada_aire = models.FloatField()
    energia_total_entrada = models.FloatField()
    energia_total_reaccion = models.FloatField()
    energia_horno = models.FloatField()

    energia_unidad = models.ForeignKey(Unidades, models.PROTECT, default=4, related_name="energia_salida_agua_evaluacion")

class SalidaLadoAgua(models.Model):
    """
    Resumen:
        Modelo que contiene la información de la salida del lado agua de una evaluación.
    
    Atributos:
        flujo_purga: models.FloatField -> Flujo de purga calculada
        energia_vapor: models.FloatField -> Energía de vapor calculada
        eficiencia: models.FloatField -> Eficiencia térmica calculada
        flujo_unidad: Unidades -> Unidad del flujo
    """
    flujo_purga = models.FloatField()
    energia_vapor = models.FloatField()
    eficiencia = models.FloatField()

    flujo_unidad = models.ForeignKey(Unidades, models.PROTECT, default=3, related_name="flujo_salida_agua_evaluacion")

class SalidaFracciones(models.Model):
    """
    Resumen:
        Modelo para almacenar la información de salida de evaluación correspondiente a las fracciones molares de los gases de combustión.

    Atributos:
        h2o: models.FloatField -> Fracción calculada de Agua
        co2: models.FloatField -> Fracción calculada de Dióxido de Carbono
        n2: models.FloatField -> Fracción calculada de Nitrógeno
        so2: models.FloatField -> Fracción calculada de Óxido de Azufre
        o2: models.FloatField -> Fracción calculada de Oxígeno
    """
    h2o = models.FloatField()
    co2 = models.FloatField()
    n2 = models.FloatField()
    so2 = models.FloatField()
    o2 = models.FloatField()

class SalidaBalanceMolar(models.Model):
    """
    Resumen:
        Modelo para almacenar la información de salida de evaluación correspondiente a las fracciones molares de los gases de combustión.

    Atributos:
        n_gas_entrada: models.FloatField -> Números de kmol/h calculados
        n_aire_gas_entrada: models.FloatField -> Números de kmol/h calculados
        n_total: models.FloatField -> Números de kmol/h calculados
    """
    n_gas_entrada = models.FloatField()
    n_aire_gas_entrada = models.FloatField()
    n_total = models.FloatField()

class SalidaFlujosEntrada(models.Model):
    """
    Resumen:
        Modelo para almacenar la información de salida de evaluación correspondiente a las fracciones molares de los gases de combustión.

    Atributos:
        flujo_gas_entrada: models.FloatField -> Flujo de gas de entrada
        flujo_aire_entrada: models.FloatField -> Flujo de aire de entrada
        flujo_combustion: models.FloatField -> Flujo de combustión
        flujo_combustion_vol: models.FloatField -> Flujo de combustión volumétrico
        porc_o2_exceso: models.FloatField -> Porcentaje de O2 en exceso
        flujo_masico_unidad: models.FloatField -> Unidades en la cual se encuentran las propiedades (másico)
        flujo_vol_unidad: models.FloatField -> Unidades en la cual se encuentran las propiedades (volumétrico)
    """
    flujo_gas_entrada = models.FloatField()
    flujo_aire_entrada = models.FloatField()
    flujo_combustion = models.FloatField()
    flujo_combustion_vol = models.FloatField()
    porc_o2_exceso = models.FloatField()

    flujo_masico_unidad = models.ForeignKey(Unidades, models.PROTECT, related_name="flujo_masico_unidad_salida_flujos_evaluacion")    
    flujo_vol_unidad = models.ForeignKey(Unidades, models.PROTECT, related_name="flujo_volumetrico_unidad_salida_flujos_evaluacion")

class Evaluacion(models.Model):
    """
    Resumen:
        Modelo general para almacenar la información de una evaluación realizada a una caldera en un momento determinado por un usuario.

    Atributos:
        nombre: models.CharField -> Nombre de la evaluación
        fecha: models.DateTimeField -> Fecha y hora de la evaluación realizada
        usuario: User -> Usuario que realizó la evaluación 
        salida_flujos: SalidaFlujosEntrada -> Datos de Salida de los flujos de entrada 
        salida_balance_molar: SalidaBalanceMolar -> Datos de salida del balance molar asociado
        salida_fracciones: SalidaFracciones -> Fracciones de los gases de salida calculados en la evaluación
        salida_balance_energia: SalidaBalanceEnergia -> Datos de salida de los balances de energia
        salida_lado_agua: SalidaLadoAgua -> Datos de Salida del lado de agua
        caldera: Caldera -> Caldera a la que está asociada la caldera
    """
    nombre = models.CharField(max_length=45)
    fecha = models.DateTimeField(auto_created=True)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, default=1, related_name="usuario_evaluacion_caldera")

    salida_flujos = models.ForeignKey(SalidaFlujosEntrada, models.PROTECT)
    salida_balance_molar = models.ForeignKey(SalidaBalanceMolar, models.PROTECT)
    salida_fracciones = models.ForeignKey(SalidaFracciones, models.PROTECT)
    salida_balance_energia = models.ForeignKey(SalidaBalanceEnergia, models.PROTECT)
    salida_lado_agua = models.ForeignKey(SalidaLadoAgua, models.PROTECT)
    caldera = models.ForeignKey(Caldera, models.PROTECT)

class EntradasFluidos(models.Model):
    """
    Resumen:
        Modelo general para almacenar la información de una evaluación realizada a una caldera en un momento determinado por un usuario.

    Atributos:
        nombre_fluido: models.CharField -> Nombre del fluido
        flujo: models.FloatField -> Flujo del fluido
        temperatura: models.FloatField -> Temperatura del fluido
        presion: models.FloatField -> Presión del fluido
        tipo_fluido: models.CharField -> Tipo de fluido de entrada de la evaluación
        humedad_relativa: models.FloatField -> % Humedad relativa. Se utiliza en el aire.
        evaluacion: Evaluacion -> Evaluación a la cual está asociada la entrada.
    """

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

class EntradaComposicion(models.Model):
    """
    Resumen:
        Modelo para almacenar la entrada de composición de los componentes de combostible.

    Atributos:
        parc_vol: models.FloatField -> Composición parcial (volumen) del fluido
        parc_aire: models.FloatField ->  Composición parcial aire
        normalizado: models.FloatField -> Composición normalizada (0-1)
        normalizado_aire: models.FloatField -> Composición normalizada aire (0-1)
        composicion: ComposicionCombustible ->  Composición original
        evaluacion: Evaluacion -> Evaluación asociada a 
    """
    parc_vol = models.FloatField()
    parc_aire = models.FloatField()
    normalizado = models.FloatField()
    normalizado_aire = models.FloatField(null=False, blank=True)
    composicion = models.ForeignKey(ComposicionCombustible, models.PROTECT)
    evaluacion = models.ForeignKey(Evaluacion, models.PROTECT, related_name="composiciones_evaluacion")