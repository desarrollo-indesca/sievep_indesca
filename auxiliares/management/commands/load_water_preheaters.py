from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
import csv
from auxiliares.models import PrecalentadorAgua, SeccionesPrecalentadorAgua, EspecificacionesPrecalentadorAgua
from intercambiadores.models import Unidades, Planta, Complejo

class Command(BaseCommand):
    help = "Carga los precalentadores de servicios industriales AMC"

    def handle(self, *args, **options):
        
        with transaction.atomic():
            # Crear unidades de velocidad lineal
            Unidades.objects.get_or_create(
                simbolo = 'm/s',
                tipo = "s"
            ) 

            Unidades.objects.get_or_create(
                simbolo = 'km/h',
                tipo = "s"
            ) 

            Unidades.objects.get_or_create(
                simbolo = 'milla/h',
                tipo = "s"
            ) 

            # Cargo de precalentadores
            with open('auxiliares/data/precalentadores.csv', 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=';')
                data = [row for row in csv_reader]

            usuario = get_user_model().objects.get(pk = 1)
            for precalentador in data:
                # Precalentador Base
                precalentador_bdd = PrecalentadorAgua.objects.get_or_create(
                    tag = precalentador['tag'],
                    descripcion = precalentador['descripcion'],
                    fabricante = precalentador['fabricante'],
                    planta = Planta.objects.get(pk=precalentador['planta']),
                    creado_por = usuario
                )

                # Sección 1: Agua
                SeccionesPrecalentadorAgua.objects.get_or_create(
                    presion_entrada = precalentador.get('presion_entrada_agua'),
                    caida_presion = precalentador.get('caida_presion_agua'),
                    entalpia_entrada = precalentador.get('entalpia_entrada_agua'),
                    entalpia_salida = precalentador.get('entalpia_salida_agua'),
                    flujo_masico_entrada = precalentador.get('flujo_masico_entrada_agua'),
                    flujo_masico_salida = precalentador.get('flujo_masico_salida_agua'),
                    temp_entrada = precalentador.get('temp_entrada_agua'),
                    temp_salida = precalentador.get('temp_salida_agua'),
                    velocidad_promedio = precalentador.get('velocidad_promedio_agua'),
                    tipo = 'A',
                    precalentador = precalentador_bdd,
                )

                # Sección 2: Vapor
                SeccionesPrecalentadorAgua.objects.get_or_create(
                    presion_entrada = precalentador.get('presion_entrada_vapor'),
                    caida_presion = precalentador.get('caida_presion_vapor'),
                    entalpia_entrada = precalentador.get('entalpia_entrada_vapor'),
                    entalpia_salida = precalentador.get('entalpia_salida_vapor'),
                    flujo_masico_entrada = precalentador.get('flujo_masico_entrada_vapor'),
                    flujo_masico_salida = precalentador.get('flujo_masico_salida_vapor'),
                    temp_entrada = precalentador.get('temp_entrada_vapor'),
                    temp_salida = precalentador.get('temp_salida_vapor'),
                    velocidad_promedio = precalentador.get('velocidad_promedio_vapor'),
                    tipo = 'V',
                    precalentador = precalentador_bdd,
                )

                # Sección 3: Drenaje 
                SeccionesPrecalentadorAgua.objects.get_or_create(
                    presion_entrada = precalentador.get('presion_entrada_drenaje'),
                    caida_presion = precalentador.get('caida_presion_drenaje'),
                    entalpia_entrada = precalentador.get('entalpia_entrada_drenaje'),
                    entalpia_salida = precalentador.get('entalpia_salida_drenaje'),
                    flujo_masico_entrada = precalentador.get('flujo_masico_entrada_drenaje'),
                    flujo_masico_salida = precalentador.get('flujo_masico_salida_drenaje'),
                    temp_entrada = precalentador.get('temp_entrada_drenaje'),
                    temp_salida = precalentador.get('temp_salida_drenaje'),
                    velocidad_promedio = precalentador.get('velocidad_promedio_drenaje'),
                    tipo = 'D',
                    precalentador = precalentador_bdd,
                )

                # Especificaciones 1: Drenaje
                EspecificacionesPrecalentadorAgua.objects.get_or_create(
                    
                )

                # Especificaciones 2: Reducción de Desobrecalentamiento

                # Especificaciones 3: Condensado

        pass