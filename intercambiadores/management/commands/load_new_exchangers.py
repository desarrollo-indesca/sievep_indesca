from django.core.management.base import BaseCommand
from intercambiadores.models import *
import csv

class Command(BaseCommand):
    help = 'Carga las clases de unidades en la base de datos'

    def handle(self, *args, **options):
        with open('intercambiadores/data/exchangers2.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            data = [row for row in csv_reader]

            for intercambiador in data:
                if(Intercambiador.objects.filter(tag = intercambiador['tag']).exists()):
                    continue

                intercambiador = Intercambiador.objects.create(
                    
                )
