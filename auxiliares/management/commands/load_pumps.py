from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic
from intercambiadores.models import Unidades, Planta, Complejo
import csv

class Command(BaseCommand):
    help = "Carga las bombas de Servicios Industriales"

    def handle(self, *args, **options):
        with atomic():
            planta = Planta.objects.get_or_create(nombre="Servicios Industriales", complejo = Complejo.objects.get(pk=1))
            print(planta)