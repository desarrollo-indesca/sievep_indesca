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