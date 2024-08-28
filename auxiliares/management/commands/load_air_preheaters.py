from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
import csv
from auxiliares.models import PrecalentadorAire, EspecificacionesPrecalentadorAire, CondicionFluido, Composicion
from intercambiadores.models import Fluido, Unidades, Planta, Complejo

COMPOSICIONES_GAS = [
    {'cas': '124-38-9', 'porcentaje': 13.22},
    {'cas': '7446-09-5', 'porcentaje': 0.00},
    {'cas': '7727-37-9', 'porcentaje': 73.02},
    {'cas': '7782-44-7', 'porcentaje': 4.82},
    {'cas': '7732-18-5', 'porcentaje': 8.94},
]

COMPOSICIONES_AIRE = [
    {'cas': '7727-37-9', 'porcentaje': 76.70},
    {'cas': '7782-44-7', 'porcentaje': 23.30},
    {'cas': '7732-18-5', 'porcentaje': 0.0},
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('auxiliares/data/precalentadores_aire.csv', 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            data = [row for row in csv_reader]

        with transaction.atomic():
            for equipo in data:
                if not PrecalentadorAire.objects.filter(tag=equipo['tag']).exists():
                    especificaciones = EspecificacionesPrecalentadorAire.objects.create(
                        material = equipo['material'],
                        espesor = equipo['espesor'],
                        diametro = equipo['diametro'],
                        altura = equipo['altura'],
                        superficie_calentamiento = equipo['superficie_calentamiento'],
                        area_transferencia = equipo['area_total_transferencia'],
                        temp_operacion = equipo['temperatura_operacion'],
                        presion_operacion = equipo['presion_operacion'],
                    )

                    precalentador = PrecalentadorAire.objects.create(
                        tag = equipo['tag'],
                        fabricante = equipo['fabricante'],
                        descripcion = equipo['descripcion'],
                        modelo = equipo['modelo'],
                        tipo = equipo['tipo'],

                        especificaciones = especificaciones,
                        planta = Planta.objects.get(pk=3),
                        creado_por = get_user_model().objects.get(pk = 1),
                    )

                    condicion_aire = CondicionFluido.objects.create(
                        fluido = "A",
                        precalentador = precalentador,
                        temp_entrada = equipo['temp_entrada_aire'],                        
                        temp_salida = equipo['temp_salida_aire'],
                        presion_entrada = equipo['presion_entrada_aire'],                        
                        presion_salida = equipo['presion_salida_aire'],
                        caida_presion = equipo['caida_presion_aire'],
                    )

                    condicion_gas = CondicionFluido.objects.create(
                        fluido = "G",
                        precalentador = precalentador,
                        temp_entrada = equipo['temp_entrada_gases'],                        
                        temp_salida = equipo['temp_salida_gases'],
                        presion_entrada = equipo['presion_entrada_gases'],                        
                        presion_salida = equipo['presion_salida_gases'],
                        caida_presion = equipo['caida_presion_gases'],
                    )

                    for compuesto in COMPOSICIONES_GAS:
                        Composicion.objects.create(
                            condicion = condicion_gas,
                            fluido = Fluido.objects.get(cas=compuesto['cas']),
                            porcentaje = compuesto['porcentaje'],
                        )

                    for compuesto in COMPOSICIONES_AIRE:
                        Composicion.objects.create(
                            condicion = condicion_gas,
                            fluido = Fluido.objects.get(cas=compuesto['cas']),
                            porcentaje = compuesto['porcentaje'],
                        )
                   