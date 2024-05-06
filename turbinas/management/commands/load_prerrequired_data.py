from django.core.management.base import BaseCommand
from intercambiadores.models import Unidades

class Command(BaseCommand):
    help = "Carga los datos requeridos para la carga de las turbinas de vapor"

    def handle(self, *args, **options):
        pass