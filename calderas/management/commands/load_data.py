from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
import csv
from calderas.models import *

class Command(BaseCommand):
    help = "Carga las calderas de servicios industriales AMC a la BDD del SIEVEP"

    composiciones = {
        "Metano": {
            "porc_vol": 70.86
        },
        "Etano": {
            "porc_vol": 14.38
        },
        "Propano": {
            "porc_vol": 6.43
        },
        "Isobutano": {
            "porc_vol": 1.13
        },
        "Butano": {
            "porc_vol": 1.93
        },
        "Isopentano": {
            "porc_vol": 0.58
        },
        "Pentano": {
            "porc_vol": 0.58
        },
        "Hexano": {
            "porc_vol": 0.36
        },
        "Hidrógeno": {
            "porc_vol": 0
        },
        "Sulfuro de Hidrógeno": {
            "porc_vol": 0
        },
        "Agua": {
            "porc_vol": 0
        },
        "Nitrógeno": {
            "porc_vol": 0.62,
            "porc_aire": 79
        },
        "Dióxido de Azufre": {
            "porc_vol": 0
        },
        "Oxígeno": {
            "porc_vol": 0,
            "porc_aire": 21
        },
    }

    calderas_con_caracteristicas = ["C-14", "C-15", "C-16", "C-17"]
    porcentajes_carga = [25, 50, 75, 100]
    caracteristicas = [
        ("Vapor", "vapor", "F", 54),
        ("Duración de la carga", "duracion_carga", "I", 63),
        ("Aire de Exceso en la Salida (%)", "aire_exceso", None, None),
        ("Continuous Blowdown", "continuous_blowdown", "F", 54),
        ("Combustible", "combustible", "F", 54),
        ("Aire de Combustión", "aire_combustion", "F", 54),
        ("Gas Combustible en la Salida", "gas_combustible_salida", "F", 54),
        ("Vapor en la Salida del Precalentador", "vapor_precalentador", "P", 33),
        ("Operación Mínima en el Tambor", "operacion_minima_tambor", "P", 33),
        ("Caída de Presión en Tambor en la Salida Precalentador", "caida_presion_minima_tambor", "P", 33),
        ("Vapor Sobrecalentado", "vapor_sobrecalentado", "T", 1),
        ("Gas Combustible de Salida FRN", "gas_combustible_FRN", "T", 1),
        ("Gas Combustible en la Salida Rehervidor", "gas_combustible_rehervidor", "T", 1),
        ("Gas Combustible en Válvula Autocontrol", "gas_combustible_autocontrol", "T", 1),
        ("Agua en la Entrada del Economizador", "agua_entrada_economizador", "T", 1),
        ("Agua de Entrada a Rehervidor", "agua_entrada_rehervidor", "T", 1),
        ("Sobrecalentador", "sobrecalentador", "P", 33),
        ("Sección de Caldera", "seccion_caldera", "P", 33),
        ("(%) Gas Seco", "gas_seco", None, None),
        ("H2 y H2O en el combustible (%)", "h2_combustible", None, None),
        ("Aire Húmedo (%)", "aire_humedo", None, None),
        ("Combustible no Quemado (%)", "combustible_no_quemado", None, None),
        ("Radiación (%)", "radiacion", None, None),
        ("Error de manufactura  (%)", "error_manufactura", None, None),
        ("Pérdida de Calor Total (%)", "perdida_calor_total", None, None),
        ("Eficiencia (%)", "eficiencia", None, None),
        ("Máximo de concentracion de Partículas en el Rehervidor", "maximo_particulas", '%', 37),
        ("FGR (%)", "fgr", None, None)
    ]

    def handle(self, *args, **options):
        data = []

        with open('auxiliares/data/ventiladores.csv', 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            data = [row for row in csv_reader]


        for caldera in data:
            with transaction.atomic():
                # Componentes que no hagan referencia al modelo Caldera
                tambor = Tambor.objects.create(
                    presion_operacion = data["presion_operacion_tambor"],
                    temp_operacion = data["temp_operacion_tambor"],
                    presion_diseno = data["presion_diseno_tambor"],
                    temp_diseno = data["temp_diseno_tambor"],
                    material = data["material_tambor"]
                )

                tambor_sup = SeccionTambor.objects.create(
                    seccion = "S",
                    diametro = data["diametro_tambor_sup"],
                    longitud = data["longitud_tambor_sup"],
                    tambor = tambor             
                )

                tambor_inf = SeccionTambor.objects.create(
                    seccion = "I",
                    diametro = data["diametro_tambor_inf"],
                    longitud = data["longitud_tambor_inf"],
                    tambor = tambor             
                )

                dims_sobrecalentador = DimsSobrecalentador.objects.create(
                    area_total_transferencia = data["area_total_sobrecalentador"],
                    diametro_tubos = data["diametro_tubos_sobrecalentador"],
                    num_tubos = data["numero_tubos_sobrecalentador"]
                )

                sobrecalentador = Sobrecalentador.objects.create(
                    presion_operacion = data["presion_operacion_sobrecalentador"],
                    temp_operacion = data["temp_operacion_sobrecalentador"],
                    presion_diseno = data["presion_diseno_sobrecalentador"],
                    flujo_max_continuo = data["flujo_max_continuo_sobrecalentador"],
                    dims = dims_sobrecalentador
                )

                dims_caldera = DimensionesCaldera.objects.create(
                    ancho = data["ancho"],
                    largo = data["largo"],
                    alto = data["alto"]
                )

                especificaciones = EspecificacionesCaldera.objects.create(
                    material = data["material"],
                    area_transferencia_calor = data["area_total_transferencia"],
                    calor_intercambiado = data["calor_intercambiado"],
                    capacidad = data["capacidad"],
                    temp_diseno = data["temp_diseno"],
                    temp_operacion = data["temp_operacion"],
                    presion_diseno = data["presion_diseno"],
                    presion_operacion = data["presion_operacion"],
                    carga = data["carga"]
                )

                combustible = Combustible.objects.create(
                    nombre_gas = "Gas Natural",
                    liquido = False
                )

                compuestos = []

                for compuesto,porcentajes in self.composiciones.items():
                    fluido = Fluido.objects.get(nombre = compuesto)
                    compuestos.append(ComposicionCombustible(
                        porc_vol = porcentajes.get("porc_vol"),
                        porc_aire = porcentajes.get("porc_aire"),
                        combustible = combustible,
                        fluido = fluido
                    ))

                chimenea = Chimenea.objects.create(
                    diametro = data["diametro_chimenea"],
                    altura = data["altura_chimenea"],
                )

                economizador = Economizador.objects.create(
                    area_total_transferencia = data["area_total_economizador"],
                    diametro_tubos = data["diametro_tubos_economizador"],
                    numero_tubos = data["numero_tubos_economizador"] 
                )

                # Modelo de Caldera

                caldera = Caldera.objects.create(
                    tag = data["tag"],
                    planta = Planta.objects.get(pk=3),
                    descripcion = data["descripcion"],
                    fabricante = data["fabricante"],
                    modelo = data["modelo"],
                    tipo_caldera = data["tipo_caldera"],
                    accesorios = data["accesorios"],
                    creado_por = get_user_model().objects.get(pk = 1)
                )

                # Corrientes y otros modelos que hagan referencia a la caldera

                if(caldera.tag in self.calderas_con_caracteristicas):                    
                    for caracteristica in self.caracteristicas:
                        car = Caracteristica.objects.create(
                            nombre = caracteristica[0],
                            tipo_unidad = caracteristica[2],
                            caldera = caldera
                        )
                        
                        for porcentaje in self.porcentajes_carga:
                            carga = ValorPorCarga.objects.create(
                                carga = porcentaje,
                                valor_num = data[f"{caracteristica[1]}_{porcentaje}"],
                                caracteristica = car,
                                unidad = Unidades.objects.get(pk = caracteristica[3])
                            )

                    # Ciclo de corrientes
                    Corriente.objects.create(
                        numero = "Corriente #5",
                        nombre = "Vapor sobrecalentado antes Atemperación",
                        tipo = "P",
                        flujo_masico = data.get("flujo_c5_2", data.get("flujo_vapor_c5_2")),
                        densidad = data["densidad_c5_2"],
                        estado = None,
                        temp_operacion = data["temp_c5_2"],
                        presion = data["presion_c5_2"],
                        caldera = caldera,                   
                    )

                    Corriente.objects.create(
                        numero = "Corriente #6",
                        nombre = "Vapor de Baja Presión",
                        tipo = "B",
                        flujo_masico = data.get("flujo_c6_2", data.get("flujo_vapor_c6_2")),
                        temp_operacion = data["temp_c6_2"],
                        presion = data["presion_c6_2"],
                        caldera = caldera,                   
                    )

                    Corriente.objects.create(
                        numero = "Corriente #3",
                        nombre = "Agua de Alimentación a Caldera",
                        tipo = "W",
                        flujo_masico = data.get("flujo_c3", data.get("flujo_vapor_c3")),
                        densidad = data["densidad_c3"],
                        estado = data["estado_c3"],
                        temp_operacion = data["temp_operacion_c3"],
                        presion = data["presion_c3"],
                        caldera = caldera,                   
                    )

                    Corriente.objects.create(
                        numero = "Corriente #7",
                        nombre = "Vapor de Alta Saturado al Sistema de Automatización",
                        tipo = "A",
                        flujo_masico = data.get("flujo_c7", data.get("flujo_vapor_c7")),
                        densidad = data["densidad_c7"],
                        temp_operacion = data["temp_c7"],
                        presion = data["presion_c7"],
                        caldera = caldera,                   
                    )
                else:
                    # Ciclo de corrientes
                    Corriente.objects.create(
                        numero = "Corriente #3",
                        nombre = "Agua de Alimentación a Caldera",
                        tipo = "W",
                        flujo_masico = data.get("flujo_c3", data.get("flujo_vapor_c3")),
                        densidad = data["densidad_c3"],
                        estado = data["estado_c3"],
                        temp_operacion = data["temp_operacion_c3"],
                        presion = data["presion_c3"],
                        caldera = caldera,                   
                    )

                    Corriente.objects.create(
                        numero = "Corriente #5",
                        nombre = "Vapor sobrecalentado antes Atemperación",
                        tipo = "B",
                        flujo_masico = data.get("flujo_c5", data.get("flujo_vapor_c5")),
                        densidad = data["densidad_c5"],
                        estado = data["estado_c5"],
                        temp_operacion = data["temp_operacion_c5"],
                        presion = data["presion_c5"],
                        caldera = caldera,                   
                    )

                    Corriente.objects.create(
                        numero = "Corriente #6",
                        nombre = "Purga Continua",
                        tipo = "P",
                        flujo_masico = data.get("flujo_c6", data.get("flujo_vapor_c6")),
                        densidad = data["densidad_c6"],
                        estado = data["estado_c6"],
                        temp_operacion = data["temp_operacion_c6"],
                        presion = data["presion_c6"],
                        caldera = caldera,                   
                    )

                    Corriente.objects.create(
                        numero = "Corriente #9",
                        nombre = "Vapor de Alta Saturado al Sistema de Automatización",
                        tipo = "A",
                        flujo_masico = data.get("flujo_c9", data.get("flujo_vapor_c9")),
                        densidad = data["densidad_c9"],
                        estado = data["estado_c9"],
                        temp_operacion = data["temp_operacion_c9"],
                        presion = data["presion_c9"],
                        caldera = caldera,                   
                    )