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

            for precalentador in data:
                pass

        pass