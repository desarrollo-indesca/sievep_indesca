from django.core.management.base import BaseCommand
from django.db import transaction
from intercambiadores.models import *
from calculos.evaluaciones import *
import csv
import datetime

class Command(BaseCommand):
    help = 'Carga las clases de unidades en la base de datos'

    def handle(self, *args, **options):
        intercambiadores = Intercambiador.objects.all()

        with transaction.atomic():
            for intercambiador in intercambiadores:
                intercambiadorp = intercambiador.intercambiador()
                if(type(intercambiadorp) == PropiedadesTuboCarcasa):
                    condicion_carcasa = intercambiadorp.condicion_carcasa()
                    condicion_tubo = intercambiadorp.condicion_tubo()

                    if(not intercambiadorp.fluido_carcasa):
                        if("mp-vapor" in condicion_carcasa.fluido_etiqueta.lower()):
                            intercambiadorp.fluido_carcasa = Fluido.objects.get(nombre="AGUA")

                    if(not intercambiadorp.fluido_tubo):
                        if("mp-vapor" in condicion_tubo.fluido_etiqueta.lower()):
                            intercambiadorp.fluido_tubo = Fluido.objects.get(nombre="AGUA")

                    intercambiadorp.save()

