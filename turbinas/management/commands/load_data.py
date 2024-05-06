from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
import csv
from auxiliares.models import Ventilador, TipoVentilador, EspecificacionesVentilador, CondicionesTrabajoVentilador, CondicionesGeneralesVentilador
from intercambiadores.models import Unidades, Planta, Complejo

class Command(BaseCommand):
    help = "Carga los datos de las turbinas de vapor de Servicios Industriales"

    def handle(self, *args, **options):
        pass