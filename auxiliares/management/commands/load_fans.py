from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
import csv
from auxiliares.models import Ventilador, TipoVentilador, EspecificacionesVentilador, CondicionesTrabajoVentilador, CondicionesGeneralesVentilador
from intercambiadores.models import Unidades, Planta, Complejo

class Command(BaseCommand):
    help = "Carga las bombas de Servicios Industriales"

    def handle(self, *args, **options):
            # Creación de Servicios Industriales
            planta = Planta.objects.get_or_create(nombre="Servicios Industriales", complejo = Complejo.objects.get(pk=1))[0]

            with open('auxiliares/data/ventiladores.csv', 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=';')
                data = [row for row in csv_reader]

            TIPO = TipoVentilador.objects.get(pk = 1)

            for fan in data:
                print("------------------------------------")
                print(fan)
                print(f"VENTILADOR {fan['tag']}")

                if(Ventilador.objects.filter(tag = fan['tag']).exists()):
                    print("SKIP")
                    continue

                with transaction.atomic():
                    especificaciones = EspecificacionesVentilador.objects.create(
                        espesor = fan['espesor_carcasa'],
                        espesor_caja = fan['espesor_caja_entrada'],
                        espesor_unidad = Unidades.objects.get(simbolo = 'm'),
                        sello = fan['sello_eje'],
                        lubricante = fan['lubricante'],
                        refrigerante = fan['refrigerante'],
                        diametro = fan['diametro_ventilador'],
                        motor = fan['motor'],
                        acceso_aire = fan['acceso_aire']
                    )

                    print("ESPECIFICACIONES CREADAS")

                    condiciones_trabajo = CondicionesTrabajoVentilador.objects.create(
                        caudal_volumetrico = fan['caudal_volumetrico'],
                        caudal_volumetrico_unidad = Unidades.objects.get(pk = 50),
                        presion_entrada = float(fan['presion_entrada'])/1000,
                        presion_salida = float(fan['presion_salida'])/1000,
                        presion_unidad = Unidades.objects.get(pk = 26),
                        velocidad_funcionamiento = fan['velocidad_func'],
                        velocidad_funcionamiento_unidad = Unidades.objects.get(pk = 51),
                        temperatura = fan['temperatura'],
                        temperatura_unidad = Unidades.objects.get(pk = 1),
                        densidad = fan['densidad'],
                        densidad_unidad = Unidades.objects.get(pk = 43),
                        potencia_freno = fan['potencia_freno'],
                        potencia_freno_unidad = Unidades.objects.get(pk = 53),
                        calculo_densidad = 'M'
                    )

                    print("CONDICIONES DE TRABAJO CREADAS")

                    condiciones_adicionales = CondicionesTrabajoVentilador.objects.create(
                        caudal_volumetrico = fan['caudal_volumetrico_adicional'],
                        caudal_volumetrico_unidad = Unidades.objects.get(pk = 50),
                        presion_entrada = float(fan['presion_entrada_adicional'])/1000,
                        presion_salida = float(fan['presion_salida_adicional'])/1000,
                        presion_unidad = Unidades.objects.get(pk = 26),
                        velocidad_funcionamiento = fan['velocidad_funcionamiento_adicional'],
                        velocidad_funcionamiento_unidad = Unidades.objects.get(pk = 51),
                        temperatura = fan['temperatura_adicional'],
                        temperatura_unidad = Unidades.objects.get(pk = 1),
                        densidad = fan['densidad_adicional'],
                        densidad_unidad = Unidades.objects.get(pk = 43),
                        potencia_freno = fan['potencia_freno_adicional'],
                        potencia_freno_unidad = Unidades.objects.get(pk = 53),
                        calculo_densidad = 'M'
                    )

                    print("CONDICIONES ADICIONALES CREADAS")

                    condiciones_generales = CondicionesGeneralesVentilador.objects.create(
                        presion_barometrica = float(fan['presion_barometrica'])/1000,
                        presion_barometrica_unidad = Unidades.objects.get(pk = 26),

                        temp_ambiente = fan['temperatura_ambiente'],
                        temp_ambiente_unidad = Unidades.objects.get(pk = 1),

                        velocidad_diseno = fan['velocidad_diseno'],
                        velocidad_diseno_unidad = Unidades.objects.get(pk = 51),

                        temp_diseno = fan['temperatura_diseno'] if fan['temperatura_diseno'] != '' else None,
                        presion_diseno = fan['presion_diseno'] if fan['presion_diseno'] != '' else None
                    )

                    print("CONDICIONES GENERALES CREADAS")

                    Ventilador.objects.create(
                        planta = planta,
                        tag = fan['tag'].upper(),
                        descripcion = fan['descripcion'],
                        fabricante = fan['fabricante'],
                        modelo = fan['modelo'],
                        tipo_ventilador = TipoVentilador.objects.get(pk = 1),
                        condiciones_trabajo = condiciones_trabajo,
                        condiciones_generales = condiciones_generales,
                        condiciones_adicionales = condiciones_adicionales,
                        especificaciones = especificaciones,
                        creado_por = get_user_model().objects.get(pk = 1)
                    )
