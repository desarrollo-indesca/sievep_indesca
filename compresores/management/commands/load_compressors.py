from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from intercambiadores.models import Planta
from compresores.models import *
import csv
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Load compressors from data/compresores.csv into the database"

    def handle(self, *args, **options):
        User = get_user_model()
        with transaction.atomic():
            try:
                with open('data/compresores.csv', 'r') as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        tipo_compresor, _ = TipoCompresor.objects.get_or_create(nombre=row['tipo'].strip())
                        planta = Planta.objects.get(nombre=row['planta'].strip())
                        
                        creado_por = User.objects.get(username=row['creado_por'])
                        editado_por = User.objects.get(username=row['editado_por']) if row['editado_por'] else None

                        compresor, created = Compresor.objects.update_or_create(
                            tag=row['tag'].strip(),
                            defaults={
                                'descripcion': row['descripcion'].strip(),
                                'fabricante': row['fabricante'].strip() if row['fabricante'] else None,
                                'modelo': row['modelo'].strip() if row['modelo'] else None,
                                'planta': planta,
                                'tipo': tipo_compresor,
                                'creado_por': creado_por,
                                'editado_por': editado_por,
                            }
                        )

                        PropiedadesCompresor.objects.update_or_create(
                            compresor=compresor,
                            defaults={
                                'numero_impulsores': row['n_impulsores'].strip() if row['numero_impulsores'] else None,
                                'material_carcasa': row['mat_carcasa'].strip() if row['material_carcasa'] else None,
                                'tipo_lubricante': row['tipo_lubricante_rot'].strip() if row['tipo_lubricante_rot'] else None,
                                'tipo_lubricacion': TipoLubricacion.objects.get_or_create(nombre=row['tipo_lubricacion'].strip())[0],
                                'tipo_sello': row['tipo_sello'].strip() if row['tipo_sello'] else None,
                                'velocidad_max_continua': row['vel_maxc'].strip() if row['vel_maxc'] else None,
                                'velocidad_rotacion': row['vel_rot'].strip() if row['vel_rot'] else None,
                                'unidad_velocidad': Unidades.objects.get(pk=52),
                                'potencia_requerida': row['preq'].strip() if row['preq'] else None,
                                'unidad_potencia': Unidades.objects.get(pk=53),
                            }
                        )

                        for i in range(1, 6):
                            etapa_numero = i
                            EtapaCompresor.objects.update_or_create(
                                compresor=compresor,
                                numero=etapa_numero,
                                defaults={
                                    'nombre_fluido': row[f'gas_e{etapa_numero}'].strip() if row[f'gas_e{etapa_numero}'] else None,
                                    'volumen_diseno': row[f'vol_e{etapa_numero}_dis'].strip() if row[f'vol_e{etapa_numero}_dis'] else None,
                                    'volumen_normal': row[f'vol_e{etapa_numero}_normal'].strip() if row[f'vol_e{etapa_numero}_normal'] else None,
                                    'flujo_masico': row[f'fmasico_e{etapa_numero}'].strip() if row[f'fmasico_e{etapa_numero}'] else None,
                                    'flujo_molar': row[f'fmolar_e{etapa_numero}'].strip() if row[f'fmolar_e{etapa_numero}'] else None,
                                    'densidad': row[f'densidad_e{etapa_numero}'].strip() if row[f'densidad_e{etapa_numero}'] else None,
                                    'aumento_estimado': row[f'aumento_est_e{etapa_numero}'].strip() if row[f'aumento_est_e{etapa_numero}'] else None,
                                    'rel_compresion': row[f'rel_comp_e{etapa_numero}'].strip() if row[f'rel_comp_e{etapa_numero}'] else None,
                                    'potencial_nominal': row[f'pot_nom_e{etapa_numero}'].strip() if row[f'pot_nom_e{etapa_numero}'] else None,
                                    'potencia_req': row[f'pot_req_e{etapa_numero}'].strip() if row[f'pot_req_e{etapa_numero}'] else None,
                                    'eficiencia_isentropica': row[f'ef_is_e{etapa_numero}'].strip() if row[f'ef_is_e{etapa_numero}'] else None,
                                    'eficiencia_politropica': row[f'ef_pol_e{etapa_numero}'].strip() if row[f'ef_pol_e{etapa_numero}'] else None,
                                    'cabezal_politropico': row[f'cab_pol_e{etapa_numero}'].strip() if row[f'cab_pol_e{etapa_numero}'] else None,
                                    'humedad_relativa': row[f'hum_rel_e{etapa_numero}'].strip() if row[f'hum_rel_e{etapa_numero}'] else None,
                                }
                            )

                            # TODO: Unidades
                            # TODO: Lados
                            # TODO: Casos restantes

                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Compresor '{compresor.tag}' created successfully"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"Compresor '{compresor.tag}' updated successfully"))
            except Exception as e:
                raise CommandError(f"Error loading compressors: {e}")

