from django.core.management.base import BaseCommand
from django.db import transaction
from intercambiadores.models import *
import csv
import datetime

class Command(BaseCommand):
    help = 'Carga las clases de unidades en la base de datos'

    def handle(self, *args, **options):
        with transaction.atomic():
            with open('intercambiadores/data/exchangers2.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file, delimiter=',')
                data = [row for row in csv_reader]

                for intercambiador in data:
                    if(Intercambiador.objects.filter(tag = intercambiador['tag']).exists()):
                        continue

                    metros = Unidades.objects.get(pk=4)

                    intercambiador = Intercambiador.objects.create(
                        tag = intercambiador['tag'],
                        fabricante = intercambiador['fabricante'],
                        planta = Planta.objects.get(nombre=intercambiador['planta'].upper()),
                        tema = Tema.objects.get(codigo=intercambiador['tema']),
                        servicio = intercambiador['servicio'],
                        arreglo_flujo = 'C',
                        criticidad = intercambiador['criticidad'],

                        creado_por = get_user_model().objects.first(),
                        creado_al = datetime.datetime.now(), 
                    )

                    def obtener_fluido(fluido):
                        fluido = fluido.lower()
                        
                        if("agua" in fluido or "vapor" == fluido or "vapor de alta" in fluido or "vapor de baja" in fluido):
                            return Fluido.objects.get(nombre__icontains = "agua")
                        elif("c2h4" in fluido or "etileno" in fluido):
                            return Fluido.objects.get(nombre__icontains = "etileno")
                        elif("c3h6" in fluido or "propileno" in fluido):
                            return Fluido.objects.get(nombre__icontains = "propileno")
                        elif("etileno" in fluido):
                            return Fluido.objects.get(nombre__icontains = "etileno")
                        elif("propano" in fluido):
                            return Fluido.objects.get(nombre__icontains = "propano")
                        elif("etano" in fluido):
                            return Fluido.objects.get(nombre__icontains = "etano")
                        elif(Fluido.objects.filter(nombre__icontains = fluido).exists()):
                            return Fluido.objects.get(nombre__icontains = fluido)

                    fluido_carcasa = obtener_fluido(intercambiador["fluido_c"].lower())
                    fluido_tubo = obtener_fluido(intercambiador["fluido_t"].lower())

                    propiedades = PropiedadesTuboCarcasa.objects.create(
                        intercambiador = intercambiador,
                        area = intercambiador['area'],
                        area_unidad = Unidades.objects.get(pk=3),
                        longitud_tubos = intercambiador['long_tubos'],
                        longitud_tubos_unidad = metros,
                        diametro_externo_tubos = intercambiador['od_tubos'],
                        diametro_interno_carcasa = intercambiador['id_carcasa'],
                        diametro_tubos_unidad = metros,
                        fluido_carcasa = fluido_carcasa,
                        material_carcasa = intercambiador["mat_carcasa"],
                        conexiones_entrada_carcasa = intercambiador["conexiones_entrada_c"],
                        conexiones_salida_carcasa = intercambiador["conexiones_salida_c"],
                        numero_tubos = intercambiador["n_tubos"],

                        material_tubo = intercambiador["mat_tubo"],
                        fluido_tubo = fluido_tubo,
                        tipo_tubo = TiposDeTubo.objects.get(nombre__icontains=intercambiador["tipo_tubo"]),
                        conexiones_entrada_tubos = intercambiador["conexiones_entrada_t"],
                        conexiones_salida_tubos = intercambiador["conexiones_salida_t"],
                        pitch_tubos = intercambiador["pitch"],
                        unidades_pitch = metros,

                        criticidad = intercambiador["criticidad"],
                        arreglo_serie = intercambiador["arreglos_serie"],
                        arreglo_paralelo = intercambiador["arreglos_paralelo"],
                        q = intercambiador["q"]
                    )

                    condiciones_tubo = CondicionesIntercambiador.objects.create(
                        intercambiador = propiedades,
                        lado = 'T',
                        temp_entrada = intercambiador["temp_entrada_t"],
                        temp_salida = intercambiador["temp_salida_t"],
                        temperaturas_unidad = Unidades.objects.get(pk=1),

                        flujo_masico = intercambiador["flujo_total_t"],
                        flujo_vapor_entrada = intercambiador["flujo_entrada_vaporc"],
                        flujo_vapor_salida = intercambiador["flujo_salida_vaporc"],
                        flujo_liquido_entrada = intercambiador["flujo_entrada_liquidot"],
                        flujo_liquido_salida = intercambiador["flujo_salida_liquidot"],
                        flujos_unidad = Unidades.objects.get(pk=6),
                        fluido_cp_liquido = (float(intercambiador["cp_entrada_liquido_t"])+float(intercambiador["cp_salida_liquido_t"]))/2 if intercambiador["cp_entrada_liquido_t"] != "" and intercambiador["cp_salida_liquido_t"] != "" else intercambiador["cp_entrada_liquido_t"] if intercambiador["cp_entrada_liquido_t"] != "" else intercambiador["cp_salida_liquido_t"],
                        fluido_cp_gas = (float(intercambiador["cp_entrada_gas_t"])+float(intercambiador["cp_salida_gas_t"]))/2 if intercambiador["cp_entrada_gas_t"] != "" and intercambiador["cp_salida_gas_t"] != "" else intercambiador["cp_entrada_liquido_t"] if intercambiador["cp_entrada_liquido_t"] != "" else intercambiador["cp_salida_liquido_t"],
                        fluido_etiqueta = intercambiador["fluido_t"].upper(),

                        cambio_de_fase = intercambiador["cambio_faset"],

                        presion_entrada = intercambiador["presion_entrada_t"],
                        caida_presion_max = intercambiador["caida_presion_max_t"],
                        caida_presion_min = intercambiador["caida_presion_min_t"],
                        unidad_presion = Unidades.objects.get(pk=7), 

                        fouling = intercambiador["fouling_t"],
                    )

                    condiciones_carcasa = CondicionesIntercambiador.objects.create(
                        intercambiador = propiedades,
                        lado = 'C',
                        temp_entrada = intercambiador["temp_entrada_c"],
                        temp_salida = intercambiador["temp_salida_c"],
                        temperaturas_unidad = Unidades.objects.get(pk=1),

                        flujo_masico = intercambiador["flujo_total_c"],
                        flujo_vapor_entrada = intercambiador["flujo_entrada_vaporc"],
                        flujo_vapor_salida = intercambiador["flujo_salida_vaporc"],
                        flujo_liquido_entrada = intercambiador["flujo_entrada_liquidoc"],
                        flujo_liquido_salida = intercambiador["flujo_salida_liquidoc"],
                        flujos_unidad = Unidades.objects.get(pk=6),
                        fluido_cp_liquido = (float(intercambiador["cp_entrada_liquido_c"])+float(intercambiador["cp_salida_liquido_c"]))/2 if intercambiador["cp_entrada_liquido_c"] != "" and intercambiador["cp_salida_liquido_c"] != "" else intercambiador["cp_entrada_liquido_c"] if intercambiador["cp_entrada_liquido_c"] != "" else intercambiador["cp_salida_liquido_c"],
                        fluido_cp_gas = (float(intercambiador["cp_entrada_gas_c"])+float(intercambiador["cp_salida_gas_c"]))/2 if intercambiador["cp_entrada_gas_c"] != "" and intercambiador["cp_salida_gas_c"] != "" else intercambiador["cp_entrada_liquido_c"] if intercambiador["cp_entrada_liquido_c"] != "" else intercambiador["cp_salida_liquido_c"],
                        fluido_etiqueta = intercambiador["fluido_c"].upper(),

                        cambio_de_fase = intercambiador["cambio_fase"],

                        presion_entrada = intercambiador["presion_entrada_c"],
                        caida_presion_max = intercambiador["caida_presion_max"],
                        caida_presion_min = intercambiador["caida_presion_min"],
                        unidad_presion = Unidades.objects.get(pk=7), 

                        fouling = intercambiador["fouling_c"],
                    )
