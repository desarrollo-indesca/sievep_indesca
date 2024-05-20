import xlsxwriter
import datetime
from django.http import HttpResponse
from io import BytesIO
from intercambiadores.models import Planta, Complejo
from simulaciones_pequiven.settings import BASE_DIR
from calculos.unidades import *

# Aquí irán los reportes en formato Excel
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def reporte_equipos(request, object_list, titulo: str, nombre: str):
    '''
    Resumen:
        Función que genera un reporte los datos generales de un equipo (filtradas o no) en formato XLSX.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)
    
    worksheet = workbook.add_worksheet()

    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 40)

    bold = workbook.add_format({'bold': True})
    bold_bordered = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    center_bordered = workbook.add_format({'border': 1})
    bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    bold_bordered.set_align('vcenter')
    center_bordered.set_align('vcenter')
    bold_bordered.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', titulo.title(), bold)
    worksheet.insert_image(0, 4, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    num = 6
    if(len(request.GET)):
        worksheet.write('A5', 'Filtros', bold_bordered)
        worksheet.write('B5', 'Tag', bold_bordered)
        worksheet.write('C5', 'Planta', bold_bordered)
        worksheet.write('D5', 'Complejo', bold_bordered)
        worksheet.write('E5', 'Servicio', bold_bordered)

        worksheet.write('B6', request.GET.get('tag', ''), center_bordered)
        worksheet.write('C6', Planta.objects.get(pk=request.GET.get('planta')).nombre if request.GET.get('planta') else '', center_bordered)
        worksheet.write('D6', Complejo.objects.get(pk=request.GET.get('complejo')).nombre if request.GET.get('complejo') else '', center_bordered)
        worksheet.write('E6', request.GET.get('servicio', request.GET.get('descripcion')), center_bordered)
        num = 8

    worksheet.write(f'A{num}', '#', bold_bordered)
    worksheet.write(f'B{num}', 'Tag', bold_bordered)
    worksheet.write(f'C{num}', 'Planta', bold_bordered)
    worksheet.write(f'D{num}', 'Complejo', bold_bordered)
    worksheet.write(f'E{num}', 'Descripción/Servicio', bold_bordered)

    for i,equipo in enumerate(object_list):
        num += 1
        worksheet.write_number(f'A{num}', i+1, center_bordered)
        worksheet.write(f'B{num}', equipo.tag, center_bordered)
        worksheet.write(f'C{num}', equipo.planta.nombre, center_bordered)
        worksheet.write(f'D{num}', equipo.planta.complejo.nombre, center_bordered)
        worksheet.write(f'E{num}', equipo.descripcion, bordered)
    
    worksheet.write(f"E{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"E{num+2}", "Generado por " + request.user.get_full_name(), fecha)
    workbook.close()
    
    return enviar_response(nombre, excel_io, fecha)

def enviar_response(nombre, archivo, fecha):
    response = HttpResponse(content_type='application/ms-excel', content=archivo.getvalue())
    fecha = datetime.datetime.now()
    response['Content-Disposition'] = f'attachment; filename="{nombre}_{fecha.year}_{fecha.month}_{fecha.day}_{fecha.hour}_{fecha.minute}.xlsx"'
    
    return response

# REPORTES DE INTERCAMBIADORES

def historico_evaluaciones(object_list, request):
    '''
    Resumen:
        Función que genera el histórico XLSX de evaluaciones realizadas a un intercambiador filtradas de acuerdo a lo establecido en el request.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)    
    worksheet = workbook.add_worksheet()

    intercambiador = object_list[0].intercambiador
    propiedades = intercambiador.intercambiador()
    condicion_carcasa = propiedades.condicion_carcasa() if intercambiador.tipo.pk == 1 else propiedades.condicion_externo()

    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 40)

    bold = workbook.add_format({'bold': True})
    bold_bordered = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    center_bordered = workbook.add_format({'border': 1})
    bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    bold_bordered.set_align('vcenter')
    center_bordered.set_align('vcenter')
    bold_bordered.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', 'Reporte de Histórico de Evaluaciones', bold)
    worksheet.insert_image(0, 4, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    worksheet.write('A5', 'Filtros', bold_bordered)
    worksheet.write('B5', 'Desde', bold_bordered)
    worksheet.write('C5', 'Hasta', bold_bordered)
    worksheet.write('D5', 'Usuario', bold_bordered)
    worksheet.write('E5', 'Nombre', bold_bordered)
    worksheet.write('F5', 'Equipo', bold_bordered)

    worksheet.write('B6', request.GET.get('desde', ''), center_bordered)
    worksheet.write('C6', Planta.objects.get(pk=request.GET.get('hasta')).nombre if request.GET.get('hasta') else '', center_bordered)
    worksheet.write('D6', Complejo.objects.get(pk=request.GET.get('usuario')).nombre if request.GET.get('usuario') else '', center_bordered)
    worksheet.write('E6', request.GET.get('nombre', ''), center_bordered)
    worksheet.write('F6', intercambiador.tag.upper(), center_bordered)
    num = 8

    worksheet.write(f'A{num}', '#', bold_bordered)
    worksheet.write(f'B{num}', 'Fecha', bold_bordered)
    worksheet.write(f'C{num}', f"Área ({propiedades.area_unidad})", bold_bordered)
    worksheet.write(f'D{num}', "Eficiencia (%)", bold_bordered)
    worksheet.write(f'E{num}', "Efectividad (%)", bold_bordered)
    worksheet.write(f"F{num}", f"U ({propiedades.u_unidad})", bold_bordered)
    worksheet.write(f"G{num}", f"NTU", bold_bordered)
    worksheet.write(f"H{num}", f"Ens. ({propiedades.ensuciamiento_unidad})", bold_bordered)
    worksheet.write(f"I{num}", f"C.P. Tubo ({condicion_carcasa.unidad_presion})", bold_bordered)
    worksheet.write(f"J{num}", f"C.P. Carcasa ({condicion_carcasa.unidad_presion})", bold_bordered)

    for i,evaluacion in enumerate(object_list):
        area = round(transformar_unidades_area([float(evaluacion.area_transferencia)], evaluacion.area_diseno_unidad.pk, propiedades.area_unidad.pk)[0], 2)
        eficiencia = float(evaluacion.eficiencia)
        efectividad = float(evaluacion.efectividad)
        ntu = float(evaluacion.ntu)
        u = round(transformar_unidades_u([float(evaluacion.u)], evaluacion.u_diseno_unidad.pk, propiedades.u_unidad.pk)[0], 2)
        caida_tubo, caida_carcasa = transformar_unidades_presion([evaluacion.caida_presion_in, evaluacion.caida_presion_ex], evaluacion.unidad_presion.pk, condicion_carcasa.unidad_presion.pk)
        caida_tubo, caida_carcasa = round(caida_tubo,4), round(caida_carcasa, 4)
        ensuciamiento = round(transformar_unidades_ensuciamiento([float(evaluacion.ensuciamiento)], evaluacion.ensuc_diseno_unidad.pk, propiedades.ensuciamiento_unidad.pk)[0],6)
        fecha_ev = evaluacion.fecha.strftime('%d/%m/%Y %H:%M')

        num += 1
        worksheet.write(f'A{num}', i+1, center_bordered)
        worksheet.write(f'B{num}', fecha_ev, center_bordered)
        worksheet.write_number(f'C{num}', area, center_bordered)
        worksheet.write_number(f'D{num}', eficiencia, center_bordered)
        worksheet.write_number(f'E{num}', efectividad, bordered)
        worksheet.write_number(f'F{num}', u, bordered)
        worksheet.write_number(f'G{num}', ntu, bordered)
        worksheet.write_number(f'H{num}', ensuciamiento, bordered)
        worksheet.write_number(f'I{num}', caida_tubo, bordered)
        worksheet.write_number(f'J{num}', caida_carcasa, bordered)

    worksheet.write(f"J{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"J{num+2}", "Generado por " + request.user.get_full_name(), fecha)
    workbook.close()
        
    return enviar_response(f'historico_evaluaciones_intercambiador_{intercambiador.tag}', excel_io, fecha)

def ficha_tecnica_tubo_carcasa_xlsx(intercambiador, request):
    '''
    Resumen:
        Función que genera los datos de ficha técnica en formato XLSX de un intercambiador tubo/carcasa.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)
    
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    bold_bordered = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    center_bordered = workbook.add_format({'border': 1})
    bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    bold_bordered.set_align('vcenter')
    center_bordered.set_align('vcenter')
    bold_bordered.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', f'Ficha Técnica Intercambiador {intercambiador.tag}', bold)
    worksheet.insert_image(0, 7, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    num = 6
    propiedades = intercambiador.intercambiador()
    condiciones_tubo = propiedades.condicion_tubo()
    condiciones_carcasa = propiedades.condicion_carcasa()

    worksheet.write(f'A{num}', 'Tag', bold_bordered)
    worksheet.write(f'B{num}', 'Complejo', bold_bordered)
    worksheet.write(f'C{num}', 'Planta', bold_bordered)
    worksheet.write(f'D{num}', 'Tema', bold_bordered)
    worksheet.write(f'E{num}', 'Fabricante', bold_bordered)
    worksheet.write(f'F{num}', 'Flujo', bold_bordered)
    worksheet.write(f'G{num}', 'Servicio', bold_bordered)
    worksheet.write(f'H{num}', 'Fluido Carcasa', bold_bordered)
    worksheet.write(f'E{num}', f'Temp. IN Carcasa ({condiciones_carcasa.temperaturas_unidad})', bold_bordered)
    worksheet.write(f'I{num}',  f'Temp. OUT Carcasa ({condiciones_carcasa.temperaturas_unidad})', bold_bordered)
    worksheet.write(f'J{num}', f'Flujo Vap. IN Carcasa ({condiciones_carcasa.flujos_unidad})', bold_bordered)
    worksheet.write(f'K{num}', f'Flujo Vap. OUT Carcasa ({condiciones_carcasa.flujos_unidad})', bold_bordered)
    worksheet.write(f'J{num}', f'Flujo Líq. IN Carcasa ({condiciones_carcasa.flujos_unidad})', bold_bordered)
    worksheet.write(f'K{num}', f'Flujo Líq. OUT Carcasa ({condiciones_carcasa.flujos_unidad})', bold_bordered)
    worksheet.write(f'L{num}', f'Flujo Másico Total Carcasa ({condiciones_carcasa.flujos_unidad})', bold_bordered)
    worksheet.write(f'M{num}', f'Cp Prom. Vapor Carcasa ({condiciones_carcasa.unidad_cp})', bold_bordered)
    worksheet.write(f'N{num}', f'Cp Prom. Líquido Carcasa ({condiciones_carcasa.unidad_cp})', bold_bordered)
    worksheet.write(f'O{num}', f'Cambio de Fase Carcasa', bold_bordered)
    worksheet.write(f'P{num}', f'Presión Entrada  Carcasa({condiciones_carcasa.unidad_presion})', bold_bordered)
    worksheet.write(f'Q{num}', f'Caída Presión Máx. Carcasa ({condiciones_carcasa.unidad_presion})', bold_bordered)
    worksheet.write(f'R{num}', f'Caída Presión Mín. Carcasa ({condiciones_carcasa.unidad_presion})', bold_bordered)
    worksheet.write(f'S{num}', f'Fouling Carcasa ({propiedades.ensuciamiento_unidad})', bold_bordered)
    worksheet.write(f'T{num}', f'Conexiones Entrada Carcasa', bold_bordered)
    worksheet.write(f'U{num}', f'Conexiones Salida Carcasa', bold_bordered)
    worksheet.write(f'V{num}', f'Pasos Carcasa', bold_bordered)
    worksheet.write(f'W{num}', 'Fluido Tubo', bold_bordered)
    worksheet.write(f'X{num}', f'Temp. IN Tubo ({condiciones_tubo.temperaturas_unidad})', bold_bordered)
    worksheet.write(f'Y{num}',  f'Temp. OUT Tubo ({condiciones_tubo.temperaturas_unidad})', bold_bordered)
    worksheet.write(f'Z{num}', f'Flujo Vap. IN Tubo ({condiciones_tubo.flujos_unidad})', bold_bordered)
    worksheet.write(f'AA{num}', f'Flujo Vap. OUT Tubo ({condiciones_tubo.flujos_unidad})', bold_bordered)
    worksheet.write(f'AB{num}', f'Flujo Líq. IN Tubo ({condiciones_tubo.flujos_unidad})', bold_bordered)
    worksheet.write(f'AC{num}', f'Flujo Líq. OUT Tubo ({condiciones_tubo.flujos_unidad})', bold_bordered)
    worksheet.write(f'AD{num}', f'Flujo Másico Total Tubo ({condiciones_tubo.flujos_unidad})', bold_bordered)
    worksheet.write(f'AE{num}', f'Cp Prom. Vapor Tubo ({condiciones_tubo.unidad_cp})', bold_bordered)
    worksheet.write(f'AF{num}', f'Cp Prom. Líquido Tubo ({condiciones_tubo.unidad_cp})', bold_bordered)
    worksheet.write(f'AG{num}', f'Cambio de Fase Tubo', bold_bordered)
    worksheet.write(f'AH{num}', f'Presión Entrada Tubo({condiciones_tubo.unidad_presion})', bold_bordered)
    worksheet.write(f'AI{num}', f'Caída Presión Máx. Tubo ({condiciones_tubo.unidad_presion})', bold_bordered)
    worksheet.write(f'AJ{num}', f'Caída Presión Mín. Tubo ({condiciones_tubo.unidad_presion})', bold_bordered)
    worksheet.write(f'AK{num}', f'Fouling Tubo ({propiedades.ensuciamiento_unidad})', bold_bordered)
    worksheet.write(f'AL{num}', f'Conexiones Entrada Tubo', bold_bordered)
    worksheet.write(f'AM{num}', f'Conexiones Salida Tubo', bold_bordered)
    worksheet.write(f'AN{num}', f'Pasos Tubo', bold_bordered)
    worksheet.write(f'AO{num}', f'Calor ({propiedades.q_unidad})', bold_bordered)
    worksheet.write(f'AP{num}', f'U ({propiedades.u_unidad})', bold_bordered)
    worksheet.write(f'AQ{num}', f'Ensuciamiento ({propiedades.ensuciamiento_unidad})', bold_bordered)
    worksheet.write(f'AR{num}', f'Área ({propiedades.area_unidad})', bold_bordered)
    worksheet.write(f'AS{num}', f'Arreglo Serie', bold_bordered)
    worksheet.write(f'AT{num}', f'Arreglo Paralelo', bold_bordered)
    worksheet.write(f'AU{num}', f'Núm. Tubos', bold_bordered)
    worksheet.write(f'AV{num}', f'Long. Tubos ({propiedades.longitud_tubos_unidad})', bold_bordered)
    worksheet.write(f'AW{num}', f'OD Tubos ({propiedades.diametro_tubos_unidad})', bold_bordered)
    worksheet.write(f'AX{num}', f'ID Carcasa ({propiedades.diametro_tubos_unidad})', bold_bordered)
    worksheet.write(f'AY{num}', f'Pitch ({propiedades.unidades_pitch})', bold_bordered)
    worksheet.write(f'AZ{num}', f'Tipo Tubo', bold_bordered)
    worksheet.write(f'BA{num}', f'Material Carcasa', bold_bordered)
    worksheet.write(f'BB{num}', f'Material Tubo', bold_bordered)
    worksheet.write(f'BC{num}', f'Criticidad', bold_bordered)

    num += 1

    worksheet.write(f'A{num}', intercambiador.tag, bordered)
    worksheet.write(f'B{num}', intercambiador.planta.complejo.nombre, bordered)
    worksheet.write(f'C{num}', intercambiador.planta.nombre, bordered)
    worksheet.write(f'D{num}', intercambiador.tema.codigo, bordered)
    worksheet.write(f'E{num}', intercambiador.fabricante, bordered)
    worksheet.write(f'F{num}', intercambiador.flujo_largo(), bordered)
    worksheet.write(f'G{num}', intercambiador.servicio, bordered)
    worksheet.write(f'H{num}', f'{propiedades.fluido_carcasa if propiedades.fluido_carcasa else condiciones_carcasa.fluido_etiqueta}', bordered)
    worksheet.write(f'E{num}', f'{condiciones_carcasa.temp_entrada}', bordered)
    worksheet.write(f'I{num}', f'{condiciones_carcasa.temp_salida}', bordered)
    worksheet.write(f'J{num}', f'{condiciones_carcasa.flujo_vapor_entrada}', bordered)
    worksheet.write(f'K{num}', f'{condiciones_carcasa.flujo_vapor_salida}', bordered)
    worksheet.write(f'J{num}', f'{condiciones_carcasa.flujo_liquido_entrada}', bordered)
    worksheet.write(f'K{num}', f'{condiciones_carcasa.flujo_liquido_salida}', bordered)
    worksheet.write(f'L{num}', f'{condiciones_carcasa.flujo_masico}', bordered)
    worksheet.write(f'M{num}', f'{condiciones_carcasa.fluido_cp_gas}', bordered)
    worksheet.write(f'N{num}', f'{condiciones_carcasa.fluido_cp_liquido}', bordered)
    worksheet.write(f'O{num}', condiciones_carcasa.cambio_fase_largo(), bordered)
    worksheet.write(f'P{num}', f'{condiciones_carcasa.presion_entrada}', bordered)
    worksheet.write(f'Q{num}', f'{condiciones_carcasa.caida_presion_max}', bordered)
    worksheet.write(f'R{num}', f'{condiciones_carcasa.caida_presion_min}', bordered)
    worksheet.write(f'S{num}', f'{condiciones_carcasa.fouling}', bordered)
    worksheet.write(f'T{num}', f'{propiedades.conexiones_entrada_carcasa}', bordered)
    worksheet.write(f'U{num}', f'{propiedades.conexiones_salida_carcasa}', bordered)
    worksheet.write(f'V{num}', f'{propiedades.numero_pasos_carcasa}', bordered)
    worksheet.write(f'W{num}', f'{propiedades.fluido_tubo if propiedades.fluido_tubo else condiciones_tubo.fluido_etiqueta}', bordered)
    worksheet.write(f'X{num}', f'{condiciones_tubo.temp_entrada}', bordered)
    worksheet.write(f'Y{num}', f'{condiciones_tubo.temp_salida}', bordered)
    worksheet.write(f'Z{num}', f'{condiciones_tubo.flujo_vapor_entrada}', bordered)
    worksheet.write(f'AA{num}', f'{condiciones_tubo.flujo_vapor_salida}', bordered)
    worksheet.write(f'AB{num}', f'{condiciones_tubo.flujo_liquido_entrada}', bordered)
    worksheet.write(f'AC{num}', f'{condiciones_tubo.flujo_liquido_salida}', bordered)
    worksheet.write(f'AD{num}', f'{condiciones_tubo.flujo_masico}', bordered)
    worksheet.write(f'AE{num}', f'{condiciones_tubo.fluido_cp_gas}', bordered)
    worksheet.write(f'AF{num}', f'{condiciones_tubo.fluido_cp_liquido}', bordered)
    worksheet.write(f'AG{num}', condiciones_tubo.cambio_fase_largo(), bordered)
    worksheet.write(f'AH{num}', f'{condiciones_tubo.presion_entrada}', bordered)
    worksheet.write(f'AI{num}', f'{condiciones_tubo.caida_presion_max}', bordered)
    worksheet.write(f'AJ{num}', f'{condiciones_tubo.caida_presion_min}', bordered)
    worksheet.write(f'AK{num}', f'{condiciones_tubo.fouling}', bordered)
    worksheet.write(f'AL{num}', f'{propiedades.conexiones_entrada_tubos}', bordered)
    worksheet.write(f'AM{num}', f'{propiedades.conexiones_salida_tubos}', bordered)
    worksheet.write(f'AN{num}', f'{propiedades.numero_pasos_tubo}', bordered)
    worksheet.write(f'AO{num}', f'{propiedades.q}', bordered)
    worksheet.write(f'AP{num}', f'{propiedades.u}', bordered)
    worksheet.write(f'AQ{num}', f'{propiedades.ensuciamiento}', bordered)
    worksheet.write(f'AR{num}', f'{propiedades.area}', bordered)
    worksheet.write(f'AS{num}', f'{propiedades.arreglo_serie}', bordered)
    worksheet.write(f'AT{num}', f'{propiedades.arreglo_paralelo}', bordered)
    worksheet.write(f'AU{num}', f'{propiedades.numero_tubos}', bordered)
    worksheet.write(f'AV{num}', f'{propiedades.longitud_tubos}', bordered)
    worksheet.write(f'AW{num}', f'{propiedades.diametro_externo_tubos}', bordered)
    worksheet.write(f'AX{num}', f'{propiedades.diametro_interno_carcasa}', bordered)
    worksheet.write(f'AY{num}', f'{propiedades.pitch_tubos}', bordered)
    worksheet.write(f'AZ{num}', f'{propiedades.tipo_tubo}', bordered)
    worksheet.write(f'BA{num}', f'{propiedades.material_carcasa}', bordered)
    worksheet.write(f'BB{num}', f'{propiedades.material_tubo}', bordered)
    worksheet.write(f'BC{num}', f'{propiedades.criticidad_larga()}', bordered)

    worksheet.write(f"E{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"E{num+2}", "Generado por " + request.user.get_full_name(), fecha)
    workbook.close()
    
    return enviar_response(f'ficha_tecnica_tubo_carcasa_{intercambiador.tag}', excel_io, fecha)

def ficha_tecnica_doble_tubo_xlsx(intercambiador, request):
    '''
    Resumen:
        Función que genera los datos de ficha técnica en formato XLSX de un intercambiador doble tubo.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)
    
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    bold_bordered = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    center_bordered = workbook.add_format({'border': 1})
    bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    bold_bordered.set_align('vcenter')
    center_bordered.set_align('vcenter')
    bold_bordered.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', f'Ficha Técnica Intercambiador {intercambiador.tag}', bold)
    worksheet.insert_image(0, 7, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    num = 6
    propiedades = intercambiador.intercambiador()
    condiciones_tubo = propiedades.condicion_interno()
    condiciones_carcasa = propiedades.condicion_externo()

    worksheet.write(f'A{num}', 'Tag', bold_bordered)
    worksheet.write(f'B{num}', 'Complejo', bold_bordered)
    worksheet.write(f'C{num}', 'Planta', bold_bordered)
    worksheet.write(f'D{num}', 'Tema', bold_bordered)
    worksheet.write(f'E{num}', 'Fabricante', bold_bordered)
    worksheet.write(f'F{num}', 'Flujo', bold_bordered)
    worksheet.write(f'G{num}', 'Servicio', bold_bordered)
    worksheet.write(f'H{num}', 'Fluido Externo', bold_bordered)
    worksheet.write(f'E{num}', f'Temp. IN Externo ({condiciones_carcasa.temperaturas_unidad})', bold_bordered)
    worksheet.write(f'I{num}', f'Temp. OUT Externo ({condiciones_carcasa.temperaturas_unidad})', bold_bordered)
    worksheet.write(f'J{num}', f'Flujo Vap. IN Externo ({condiciones_carcasa.flujos_unidad})', bold_bordered)
    worksheet.write(f'K{num}', f'Flujo Vap. OUT Externo ({condiciones_carcasa.flujos_unidad})', bold_bordered)
    worksheet.write(f'J{num}', f'Flujo Líq. IN Externo ({condiciones_carcasa.flujos_unidad})', bold_bordered)
    worksheet.write(f'K{num}', f'Flujo Líq. OUT Externo ({condiciones_carcasa.flujos_unidad})', bold_bordered)
    worksheet.write(f'L{num}', f'Flujo Másico Total Externo ({condiciones_carcasa.flujos_unidad})', bold_bordered)
    worksheet.write(f'M{num}', f'Cp Prom. Vapor Externo ({condiciones_carcasa.unidad_cp})', bold_bordered)
    worksheet.write(f'N{num}', f'Cp Prom. Líquido Externo ({condiciones_carcasa.unidad_cp})', bold_bordered)
    worksheet.write(f'O{num}', f'Cambio de Fase Externo', bold_bordered)
    worksheet.write(f'P{num}', f'Presión Entrada  Externo({condiciones_carcasa.unidad_presion})', bold_bordered)
    worksheet.write(f'Q{num}', f'Caída Presión Máx. Externo ({condiciones_carcasa.unidad_presion})', bold_bordered)
    worksheet.write(f'R{num}', f'Caída Presión Mín. Externo ({condiciones_carcasa.unidad_presion})', bold_bordered)
    worksheet.write(f'S{num}', f'Fouling Externo ({propiedades.ensuciamiento_unidad})', bold_bordered)
    worksheet.write(f'T{num}', f'Conexiones Entrada Externo', bold_bordered)
    worksheet.write(f'U{num}', f'Conexiones Salida Externo', bold_bordered)
    worksheet.write(f'V{num}', f'Arreglos en Serie Externo', bold_bordered)
    worksheet.write(f'W{num}', f'Arreglos en Paralelo Externo', bold_bordered)
    worksheet.write(f'X{num}', f'Fluido Interno', bold_bordered)
    worksheet.write(f'Y{num}', f'Temp. IN Interno ({condiciones_tubo.temperaturas_unidad})', bold_bordered)
    worksheet.write(f'Z{num}',  f'Temp. OUT Interno ({condiciones_tubo.temperaturas_unidad})', bold_bordered)
    worksheet.write(f'AA{num}', f'Flujo Vap. IN Interno ({condiciones_tubo.flujos_unidad})', bold_bordered)
    worksheet.write(f'AB{num}', f'Flujo Vap. OUT Interno ({condiciones_tubo.flujos_unidad})', bold_bordered)
    worksheet.write(f'AC{num}', f'Flujo Líq. IN Interno ({condiciones_tubo.flujos_unidad})', bold_bordered)
    worksheet.write(f'AD{num}', f'Flujo Líq. OUT Interno ({condiciones_tubo.flujos_unidad})', bold_bordered)
    worksheet.write(f'AE{num}', f'Flujo Másico Total Interno ({condiciones_tubo.flujos_unidad})', bold_bordered)
    worksheet.write(f'AF{num}', f'Cp Prom. Vapor Interno ({condiciones_tubo.unidad_cp})', bold_bordered)
    worksheet.write(f'AG{num}', f'Cp Prom. Líquido Interno ({condiciones_tubo.unidad_cp})', bold_bordered)
    worksheet.write(f'AH{num}', f'Cambio de Fase Interno', bold_bordered)
    worksheet.write(f'AI{num}', f'Presión Entrada Interno({condiciones_tubo.unidad_presion})', bold_bordered)
    worksheet.write(f'AJ{num}', f'Caída Presión Máx. Interno ({condiciones_tubo.unidad_presion})', bold_bordered)
    worksheet.write(f'AK{num}', f'Caída Presión Mín. Interno ({condiciones_tubo.unidad_presion})', bold_bordered)
    worksheet.write(f'AL{num}', f'Fouling Interno ({propiedades.ensuciamiento_unidad})', bold_bordered)
    worksheet.write(f'AM{num}', f'Conexiones Entrada Interno', bold_bordered)
    worksheet.write(f'AN{num}', f'Conexiones Salida Interno', bold_bordered)
    worksheet.write(f'AO{num}', f'Arreglos en Serie Externo', bold_bordered)
    worksheet.write(f'AP{num}', f'Arreglos en Paralelo Externo', bold_bordered)
    worksheet.write(f'AQ{num}', f'Calor ({propiedades.q_unidad})', bold_bordered)
    worksheet.write(f'AR{num}', f'U ({propiedades.u_unidad})', bold_bordered)
    worksheet.write(f'AS{num}', f'Ensuciamiento ({propiedades.ensuciamiento_unidad})', bold_bordered)
    worksheet.write(f'AT{num}', f'Área ({propiedades.area_unidad})', bold_bordered)
    worksheet.write(f'AU{num}', f'Núm. Tubos', bold_bordered)
    worksheet.write(f'AV{num}', f'Long. Tubos ({propiedades.longitud_tubos_unidad})', bold_bordered)
    worksheet.write(f'AW{num}', f'OD Tubo Externo ({propiedades.diametro_tubos_unidad})', bold_bordered)
    worksheet.write(f'AX{num}', f'OD Tubo Interno ({propiedades.diametro_tubos_unidad})', bold_bordered)
    worksheet.write(f'AY{num}', f'Tipo Tubo', bold_bordered)
    worksheet.write(f'AZ{num}', f'Material Tubo Externo', bold_bordered)
    worksheet.write(f'BA{num}', f'Material Tubo Interno', bold_bordered)
    worksheet.write(f'BB{num}', f'Criticidad', bold_bordered)
    worksheet.write(f'BC{num}', f'Número de Aletas', bold_bordered)
    worksheet.write(f'BD{num}', f'Altura Alteras ({propiedades.diametro_tubos_unidad})', bold_bordered)

    num += 1

    worksheet.write(f'A{num}', intercambiador.tag, bordered)
    worksheet.write(f'B{num}', intercambiador.planta.complejo.nombre, bordered)
    worksheet.write(f'C{num}', intercambiador.planta.nombre, bordered)
    worksheet.write(f'D{num}', intercambiador.tema.codigo, bordered)
    worksheet.write(f'E{num}', intercambiador.fabricante, bordered)
    worksheet.write(f'F{num}', intercambiador.flujo_largo(), bordered)
    worksheet.write(f'G{num}', intercambiador.servicio, bordered)
    worksheet.write(f'H{num}', f'{propiedades.fluido_ex if propiedades.fluido_ex else condiciones_carcasa.fluido_etiqueta}', bordered)
    worksheet.write(f'E{num}', f'{condiciones_carcasa.temp_entrada}', bordered)
    worksheet.write(f'I{num}', f'{condiciones_carcasa.temp_salida}', bordered)
    worksheet.write(f'J{num}', f'{condiciones_carcasa.flujo_vapor_entrada}', bordered)
    worksheet.write(f'K{num}', f'{condiciones_carcasa.flujo_vapor_salida}', bordered)
    worksheet.write(f'J{num}', f'{condiciones_carcasa.flujo_liquido_entrada}', bordered)
    worksheet.write(f'K{num}', f'{condiciones_carcasa.flujo_liquido_salida}', bordered)
    worksheet.write(f'L{num}', f'{condiciones_carcasa.flujo_masico}', bordered)
    worksheet.write(f'M{num}', f'{condiciones_carcasa.fluido_cp_gas}', bordered)
    worksheet.write(f'N{num}', f'{condiciones_carcasa.fluido_cp_liquido}', bordered)
    worksheet.write(f'O{num}', condiciones_carcasa.cambio_fase_largo(), bordered)
    worksheet.write(f'P{num}', f'{condiciones_carcasa.presion_entrada}', bordered)
    worksheet.write(f'Q{num}', f'{condiciones_carcasa.caida_presion_max}', bordered)
    worksheet.write(f'R{num}', f'{condiciones_carcasa.caida_presion_min}', bordered)
    worksheet.write(f'S{num}', f'{condiciones_carcasa.fouling}', bordered)
    worksheet.write(f'T{num}', f'{propiedades.conexiones_entrada_ex}', bordered)
    worksheet.write(f'U{num}', f'{propiedades.conexiones_salida_ex}', bordered)
    worksheet.write(f'V{num}', f'{propiedades.arreglo_serie_ex}', bordered)
    worksheet.write(f'W{num}', f'{propiedades.arreglo_paralelo_ex}', bordered)
    worksheet.write(f'X{num}', f'{propiedades.fluido_in if propiedades.fluido_in else condiciones_tubo.fluido_etiqueta}', bordered)
    worksheet.write(f'Y{num}', f'{condiciones_tubo.temp_entrada}', bordered)
    worksheet.write(f'Z{num}', f'{condiciones_tubo.temp_salida}', bordered)
    worksheet.write(f'AA{num}', f'{condiciones_tubo.flujo_vapor_entrada}', bordered)
    worksheet.write(f'AB{num}', f'{condiciones_tubo.flujo_vapor_salida}', bordered)
    worksheet.write(f'AC{num}', f'{condiciones_tubo.flujo_liquido_entrada}', bordered)
    worksheet.write(f'AD{num}', f'{condiciones_tubo.flujo_liquido_salida}', bordered)
    worksheet.write(f'AE{num}', f'{condiciones_tubo.flujo_masico}', bordered)
    worksheet.write(f'AF{num}', f'{condiciones_tubo.fluido_cp_gas}', bordered)
    worksheet.write(f'AG{num}', f'{condiciones_tubo.fluido_cp_liquido}', bordered)
    worksheet.write(f'AH{num}', condiciones_tubo.cambio_fase_largo(), bordered)
    worksheet.write(f'AI{num}', f'{condiciones_tubo.presion_entrada}', bordered)
    worksheet.write(f'AJ{num}', f'{condiciones_tubo.caida_presion_max}', bordered)
    worksheet.write(f'AK{num}', f'{condiciones_tubo.caida_presion_min}', bordered)
    worksheet.write(f'AL{num}', f'{condiciones_tubo.fouling}', bordered)
    worksheet.write(f'AM{num}', f'{propiedades.conexiones_entrada_in}', bordered)
    worksheet.write(f'AN{num}', f'{propiedades.conexiones_salida_in}', bordered)
    worksheet.write(f'AO{num}', f'{propiedades.arreglo_serie_in}', bordered)
    worksheet.write(f'AP{num}', f'{propiedades.arreglo_paralelo_in}', bordered)
    worksheet.write(f'AQ{num}', f'{propiedades.q}', bordered)
    worksheet.write(f'AR{num}', f'{propiedades.u}', bordered)
    worksheet.write(f'AS{num}', f'{propiedades.ensuciamiento}', bordered)
    worksheet.write(f'AT{num}', f'{propiedades.area}', bordered)
    worksheet.write(f'AU{num}', f'{propiedades.numero_tubos}', bordered)
    worksheet.write(f'AV{num}', f'{propiedades.longitud_tubos}', bordered)
    worksheet.write(f'AW{num}', f'{propiedades.diametro_externo_ex}', bordered)
    worksheet.write(f'AX{num}', f'{propiedades.diametro_externo_in}', bordered)
    worksheet.write(f'AY{num}', f'{propiedades.tipo_tubo}', bordered)
    worksheet.write(f'AZ{num}', f'{propiedades.material_ex}', bordered)
    worksheet.write(f'BA{num}', f'{propiedades.material_in}', bordered)
    worksheet.write(f'BB{num}', f'{propiedades.criticidad_larga()}', bordered)
    worksheet.write(f'BC{num}', f'{propiedades.numero_aletas}', bordered)
    worksheet.write(f'BD{num}', f'{propiedades.altura_aletas}', bordered)

    worksheet.write(f"E{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"E{num+2}", "Generado por " + request.user.get_full_name(), fecha)
    workbook.close()
    
    return enviar_response(f'intercambiador_doble_tubo_ficha_tecnica_{intercambiador.tag}', excel_io, fecha)

def reporte_intercambiadores(object_list, request):
    '''
    Resumen:
        Función que genera los datos generales de un intercambiador en formato XLSX.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)
    
    worksheet = workbook.add_worksheet()

    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 40)

    bold = workbook.add_format({'bold': True})
    bold_bordered = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    center_bordered = workbook.add_format({'border': 1})
    bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    bold_bordered.set_align('vcenter')
    center_bordered.set_align('vcenter')
    bold_bordered.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', f'Reporte de Intercambiadores {"Tubo/Carcasa" if object_list[0].intercambiador.tipo.pk == 1 else "Doble Tubo"}', bold)
    worksheet.insert_image(0, 4, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    num = 6
    if(len(request.GET)):
        worksheet.write('A5', 'Filtros', bold_bordered)
        worksheet.write('B5', 'Tag', bold_bordered)
        worksheet.write('C5', 'Planta', bold_bordered)
        worksheet.write('D5', 'Complejo', bold_bordered)
        worksheet.write('E5', 'Servicio', bold_bordered)

        worksheet.write('B6', request.GET.get('tag', ''), center_bordered)
        worksheet.write('C6', Planta.objects.get(pk=request.GET.get('planta')).nombre if request.GET.get('planta') else '', center_bordered)
        worksheet.write('D6', Complejo.objects.get(pk=request.GET.get('complejo')).nombre if request.GET.get('complejo') else '', center_bordered)
        worksheet.write('E6', request.GET.get('servicio', ''), center_bordered)
        num = 8

    worksheet.write(f'A{num}', '#', bold_bordered)
    worksheet.write(f'B{num}', 'Tag', bold_bordered)
    worksheet.write(f'C{num}', 'Planta', bold_bordered)
    worksheet.write(f'D{num}', 'Complejo', bold_bordered)
    worksheet.write(f'E{num}', 'Servicio', bold_bordered)
    worksheet.write(f'F{num}', 'Criticidad', bold_bordered)

    for i,intercambiador in enumerate(object_list):
        datos =  intercambiador.intercambiador
        num += 1
        worksheet.write_number(f'A{num}', i+1, center_bordered)
        worksheet.write(f'B{num}', datos.tag, center_bordered)
        worksheet.write(f'C{num}', datos.planta.nombre, center_bordered)
        worksheet.write(f'D{num}', datos.planta.complejo.nombre, center_bordered)
        worksheet.write(f'E{num}', datos.servicio, bordered)
        worksheet.write(f'F{num}', intercambiador.criticidad_larga(), bordered)
    
    worksheet.write(f"E{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"E{num+2}", "Generado por " + request.user.get_full_name(), fecha)
    workbook.close()
    
    return enviar_response(f'intercambiadores_{datos.tag}', excel_io, fecha)

# REPORTES DE BOMBAS CENTRÍFUGAS
def ficha_instalacion_bomba_centrifuga(bomba, request):
    '''
    Resumen:
        Función que genera los datos de ficha de instalación en formato XLSX de una bomba centrífuga.
    '''

    def anadir_header_tuberias(worksheet, num, estilo):
        worksheet.write(f"A{num}", "# Tramo", estilo)
        worksheet.write(f"B{num}", "Longitud Total", estilo)
        worksheet.write(f"C{num}", "Longitud Unidad", estilo)
        worksheet.write(f"D{num}", "Diámetro Interno", estilo)  
        worksheet.write(f"E{num}", "Diámetro Unidad", estilo)
        worksheet.write(f"F{num}", "Material", estilo)
        worksheet.write(f"G{num}", "Codos 90°", estilo)    
        worksheet.write(f"H{num}", "Codos 90° Radio Largo", estilo)    
        worksheet.write(f"I{num}", "Codos 90° Roscados", estilo)    
        worksheet.write(f"J{num}", "Codos 45°", estilo)    
        worksheet.write(f"K{num}", "Codos 45° Roscados", estilo)
        worksheet.write(f"L{num}", "Codos 180°", estilo)    
        worksheet.write(f"M{num}", "Válvulas de Compuerta Abiertas", estilo)    
        worksheet.write(f"N{num}", "Válvulas de Compuertas a 3/4", estilo)    
        worksheet.write(f"O{num}", "Válvulas de Compuertas a 1/2", estilo)    
        worksheet.write(f"P{num}", "Válvulas de Compuertas a 1/4", estilo)    
        worksheet.write(f"Q{num}", "Válvulas Mariposa 2\"-8\"", estilo)
        worksheet.write(f"R{num}", "Válvulas Mariposa 10\"-14\"", estilo)
        worksheet.write(f"S{num}", "Válvulas Mariposa 16\"-24\"", estilo)
        worksheet.write(f"T{num}", "Válvulas Check Giratorias", estilo)
        worksheet.write(f"U{num}", "Válvulas Check Bola", estilo)
        worksheet.write(f"V{num}", "Válvulas Disco Bisagra", estilo)
        worksheet.write(f"W{num}", "Válvulas Disco Vástago", estilo)
        worksheet.write(f"X{num}", "Válvulas Globo", estilo)
        worksheet.write(f"Y{num}", "Válvulas Ángulo", estilo)
        worksheet.write(f"Z{num}", "Conexiones T Flujo Directo", estilo)
        worksheet.write(f"AA{num}", "Conexiones T Flujo Ramal", estilo)

        num += 1

        return(worksheet, num)
    
    def anadir_datos_tuberias(worksheet, num, i, tramo, estilo):
        worksheet.write(f"A{num}", i, estilo)
        worksheet.write(f"B{num}", tramo.longitud_tuberia, estilo)
        worksheet.write(f"C{num}", tramo.longitud_tuberia_unidad.simbolo, estilo)
        worksheet.write(f"D{num}", tramo.diametro_tuberia, estilo)  
        worksheet.write(f"E{num}", tramo.diametro_tuberia_unidad.simbolo, estilo)
        worksheet.write(f"F{num}", tramo.material_tuberia.nombre, estilo)
        worksheet.write(f"G{num}", tramo.numero_codos_90, estilo)    
        worksheet.write(f"H{num}", tramo.numero_codos_90_rl, estilo)    
        worksheet.write(f"I{num}", tramo.numero_codos_90_ros, estilo)    
        worksheet.write(f"J{num}", tramo.numero_codos_45, estilo)    
        worksheet.write(f"K{num}", tramo.numero_codos_45_ros, estilo)
        worksheet.write(f"L{num}", tramo.numero_codos_180, estilo)    
        worksheet.write(f"M{num}", tramo.numero_valvulas_compuerta, estilo)    
        worksheet.write(f"N{num}", tramo.numero_valvulas_compuerta_abierta_3_4, estilo)    
        worksheet.write(f"O{num}", tramo.numero_valvulas_compuerta_abierta_1_2, estilo)    
        worksheet.write(f"P{num}", tramo.numero_valvulas_compuerta_abierta_1_4, estilo)    
        worksheet.write(f"Q{num}", tramo.numero_valvulas_mariposa_2_8, estilo)
        worksheet.write(f"R{num}", tramo.numero_valvulas_mariposa_10_14, estilo)
        worksheet.write(f"S{num}", tramo.numero_valvulas_mariposa_16_24, estilo)
        worksheet.write(f"T{num}", tramo.numero_valvula_giratoria, estilo)
        worksheet.write(f"U{num}", tramo.numero_valvula_bola, estilo)
        worksheet.write(f"V{num}", tramo.numero_valvula_bisagra, estilo)
        worksheet.write(f"W{num}", tramo.numero_valvula_vastago, estilo)
        worksheet.write(f"X{num}", tramo.numero_valvula_globo, estilo)
        worksheet.write(f"Y{num}", tramo.numero_valvula_angulo, estilo)
        worksheet.write(f"Z{num}", tramo.conexiones_t_directo, estilo)
        worksheet.write(f"AA{num}", tramo.conexiones_t_ramal, estilo)

        num += 2

        return worksheet

    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)
    
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    header = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    center_bordered = workbook.add_format({'border': 1})
    bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    header.set_align('vcenter')
    center_bordered.set_align('vcenter')
    header.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', f'Ficha Instalación Bomba Centrífuga {bomba.tag}', bold)
    worksheet.insert_image(0, 7, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    num = 6

    instalacion_succion = bomba.instalacion_succion
    instalacion_descarga = bomba.instalacion_descarga

    worksheet.write(f'A{num}', 'Tag', header)
    worksheet.write(f'B{num}', 'Elevación Succión', header)
    worksheet.write(f'C{num}', 'Elevación Descarga', header)
    worksheet.write(f'D{num}', 'Unidad Elevación', header)
    
    num += 1

    worksheet.write(f'A{num}', bomba.tag, bordered)
    worksheet.write(f'B{num}', instalacion_succion.elevacion, bordered)
    worksheet.write(f'C{num}', instalacion_descarga.elevacion, bordered)
    worksheet.write(f'D{num}', instalacion_succion.elevacion_unidad.simbolo, bordered)

    num += 2

    worksheet,num = anadir_header_tuberias(worksheet, num, header)
    for i,tramo in enumerate(instalacion_succion.tuberias.all()):
        worksheet = anadir_datos_tuberias(worksheet, num, i, tramo, center_bordered)
        num += 1

    num += 2

    worksheet,num = anadir_header_tuberias(worksheet, num, header)
    for i,tramo in enumerate(instalacion_descarga.tuberias.all()):
        worksheet = anadir_datos_tuberias(worksheet, num, i, tramo, center_bordered)
        num += 1

    worksheet.write(f"E{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"E{num+2}", "Generado por " + request.user.get_full_name(), fecha)

    workbook.close()
    
    return enviar_response(f'ficha_instalacion_bomba_centrifuga_{bomba.tag}', excel_io, fecha)

def ficha_tecnica_bomba_centrifuga(bomba, request):
    '''
    Resumen:
        Función que genera los datos de ficha técnica en formato XLSX de un intercambiador tubo/carcasa.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)
    
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    identificacion = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    condiciones_diseno_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'red'})
    condiciones_fluido_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'cyan'})
    especificaciones_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'green'})
    construccion_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'purple'})
    motor_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'gray'})
    center_bordered = workbook.add_format({'border': 1})
    bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    identificacion.set_align('vcenter')
    center_bordered.set_align('vcenter')
    identificacion.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', f'Ficha Técnica Bomba Centrífuga {bomba.tag}', bold)
    worksheet.insert_image(0, 7, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    num = 6

    condiciones_diseno = bomba.condiciones_diseno
    condiciones_fluido = condiciones_diseno.condiciones_fluido
    especificaciones = bomba.especificaciones_bomba
    construccion = bomba.detalles_construccion
    motor = bomba.detalles_motor

    worksheet.write(f'A{num}', 'Tag', identificacion)
    worksheet.write(f'B{num}', 'Complejo', identificacion)
    worksheet.write(f'C{num}', 'Planta', identificacion)
    worksheet.write(f'D{num}', 'Tipo', identificacion)
    worksheet.write(f'E{num}', 'Fabricante', identificacion)
    worksheet.write(f'F{num}', 'Modelo', identificacion)
    worksheet.write(f'G{num}', 'Descripción', identificacion)
    worksheet.write(f'H{num}', f'Capacidad ({condiciones_diseno.capacidad_unidad})', condiciones_diseno_estilo)
    worksheet.write(f'I{num}', f'Presión Succión ({condiciones_diseno.presion_unidad})', condiciones_diseno_estilo)
    worksheet.write(f'J{num}', f'Presión Descarga ({condiciones_diseno.presion_unidad})', condiciones_diseno_estilo)
    worksheet.write(f'K{num}', f'Presión Diferencial ({condiciones_diseno.presion_unidad})', condiciones_diseno_estilo)
    worksheet.write(f'L{num}', f'NPSHa ({condiciones_diseno.npsha_unidad})', condiciones_diseno_estilo)
    worksheet.write(f'M{num}', f'Fluido', condiciones_fluido_estilo)
    worksheet.write(f'N{num}', f'Temp. Operación ({condiciones_fluido.temperatura_unidad})', condiciones_fluido_estilo)
    worksheet.write(f'O{num}', f'Presión Vapor ({condiciones_fluido.presion_vapor_unidad})', condiciones_fluido_estilo)
    worksheet.write(f'P{num}', f'Temp. Presión Vapor ({condiciones_fluido.temperatura_unidad})', condiciones_fluido_estilo)
    worksheet.write(f'Q{num}', f'Densidad ({condiciones_fluido.densidad_unidad if condiciones_fluido.densidad_unidad else "RELATIVA"})', condiciones_fluido_estilo)
    worksheet.write(f'R{num}', f'Viscosidad ({condiciones_fluido.viscosidad_unidad})', condiciones_fluido_estilo)
    worksheet.write(f'S{num}', f'¿Corrosivo/Erosivo?', condiciones_fluido_estilo)
    worksheet.write(f'T{num}', f'Peligroso', condiciones_fluido_estilo)
    worksheet.write(f'U{num}', f'Inflamable', condiciones_fluido_estilo)
    worksheet.write(f'V{num}', f'Concentración H2S ({condiciones_fluido.concentracion_unidad})', condiciones_fluido_estilo)
    worksheet.write(f'W{num}', f'Concentración Cloro ({condiciones_fluido.concentracion_unidad})', condiciones_fluido_estilo)
    worksheet.write(f'X{num}', f'Número de Curva', especificaciones_estilo)
    worksheet.write(f'Y{num}', f'Velocidad (RPM)', especificaciones_estilo)
    worksheet.write(f'Z{num}', f'Potencia Máxima ({especificaciones.potencia_unidad})', especificaciones_estilo)
    worksheet.write(f'AA{num}', f'Eficiencia (%)', especificaciones_estilo)
    worksheet.write(f'AB{num}', f'NPSHr ({especificaciones.npshr_unidad})', especificaciones_estilo)
    worksheet.write(f'AC{num}', f'Cabezal Total ({especificaciones.cabezal_unidad})', especificaciones_estilo)
    worksheet.write(f'AD{num}', f'Diámetro Interno Succión ({especificaciones.id_unidad})', especificaciones_estilo)
    worksheet.write(f'AE{num}', f'Diámetro Interno Descarga ({especificaciones.id_unidad})', especificaciones_estilo)
    worksheet.write(f'AF{num}', f'Número de Etapas', especificaciones_estilo)
    worksheet.write(f'AG{num}', f'Conexión Succión', construccion_estilo)
    worksheet.write(f'AH{num}', f'Tamaño Rating Succión', construccion_estilo)
    worksheet.write(f'AI{num}', f'Conexión Descarga', construccion_estilo)
    worksheet.write(f'AJ{num}', f'Tamaño Rating Descarga', construccion_estilo)
    worksheet.write(f'AK{num}', f'Carcasa Dividida', construccion_estilo)
    worksheet.write(f'AL{num}', f'Modelo', construccion_estilo)
    worksheet.write(f'AM{num}', f'Fabricante de Sello', construccion_estilo)
    worksheet.write(f'AN{num}', f'Tipo', construccion_estilo)
    worksheet.write(f'AO{num}', f'Tipo de Carcasa 1', construccion_estilo)
    worksheet.write(f'AP{num}', f'Tipo de Carcasa 2', construccion_estilo)
    worksheet.write(f'AQ{num}', f'Potencia ({motor.potencia_motor_unidad})', motor_estilo)
    worksheet.write(f'AR{num}', f'Velocidad (RPM)', motor_estilo)
    worksheet.write(f'AS{num}', f'Factor de Servicio', motor_estilo)
    worksheet.write(f'AT{num}', f'Posición', motor_estilo)
    worksheet.write(f'AU{num}', f'Voltaje ({motor.voltaje_unidad})', motor_estilo)
    worksheet.write(f'AV{num}', f'Fases', motor_estilo)
    worksheet.write(f'AW{num}', f'Frecuencia ({motor.frecuencia_unidad})', motor_estilo)
    worksheet.write(f'AX{num}', f'Aislamiento', motor_estilo)
    worksheet.write(f'AY{num}', f'Método Arranque', motor_estilo)

    num += 1

    worksheet.write(f'A{num}', bomba.tag, bordered)
    worksheet.write(f'B{num}', bomba.planta.complejo.nombre, bordered)
    worksheet.write(f'C{num}', bomba.planta.nombre, bordered)
    worksheet.write(f'D{num}', bomba.tipo_bomba.nombre, bordered)
    worksheet.write(f'E{num}', bomba.fabricante, bordered)
    worksheet.write(f'F{num}', bomba.modelo, bordered)
    worksheet.write(f'G{num}', bomba.descripcion, bordered)
    worksheet.write(f'H{num}', f'{condiciones_diseno.capacidad if condiciones_diseno.capacidad else ""}', bordered)
    worksheet.write(f'I{num}', f'{condiciones_diseno.presion_succion if condiciones_diseno.presion_succion else ""}', bordered)
    worksheet.write(f'J{num}', f'{condiciones_diseno.presion_descarga if condiciones_diseno.presion_descarga else ""}', bordered)
    worksheet.write(f'K{num}', f'{condiciones_diseno.presion_diferencial if condiciones_diseno.presion_diferencial else ""}', bordered)
    worksheet.write(f'L{num}', f'{condiciones_diseno.npsha if condiciones_diseno.npsha else ""}', bordered)
    worksheet.write(f'M{num}', f'{condiciones_fluido.fluido if condiciones_fluido.fluido else condiciones_fluido.nombre_fluido}', bordered)
    worksheet.write(f'N{num}', f'{condiciones_fluido.temperatura_operacion if condiciones_fluido.temperatura_operacion else ""}', bordered)
    worksheet.write(f'O{num}', f'{condiciones_fluido.presion_vapor if condiciones_fluido.presion_vapor else ""}', bordered)
    worksheet.write(f'P{num}', f'{condiciones_fluido.temperatura_presion_vapor if condiciones_fluido.temperatura_presion_vapor else ""}', bordered)
    worksheet.write(f'Q{num}', f'{condiciones_fluido.densidad if condiciones_fluido.densidad else ""}', bordered)
    worksheet.write(f'R{num}', f'{condiciones_fluido.viscosidad if condiciones_fluido.viscosidad else ""}', bordered)
    worksheet.write(f'S{num}', f'{condiciones_fluido.corrosividad_largo()}', bordered)
    worksheet.write(f'T{num}', f'{condiciones_fluido.peligroso_largo()}', bordered)
    worksheet.write(f'U{num}', f'{condiciones_fluido.inflamable_largo()}', bordered)
    worksheet.write(f'V{num}', f'{condiciones_fluido.concentracion_h2s if condiciones_fluido.concentracion_h2s else ""}', bordered)
    worksheet.write(f'W{num}', f'{condiciones_fluido.concentracion_cloro if condiciones_fluido.concentracion_cloro else ""}', bordered)
    worksheet.write(f'X{num}', f'{especificaciones.numero_curva if especificaciones.numero_curva else ""}', bordered)
    worksheet.write(f'Y{num}', f'{especificaciones.velocidad if especificaciones.velocidad else ""}', bordered)
    worksheet.write(f'Z{num}', f'{especificaciones.potencia_maxima if especificaciones.potencia_maxima else ""}', bordered)
    worksheet.write(f'AA{num}', f'{especificaciones.eficiencia if especificaciones.eficiencia else ""}', bordered)
    worksheet.write(f'AB{num}', f'{especificaciones.npshr if especificaciones.npshr else ""}', bordered)
    worksheet.write(f'AC{num}', f'{especificaciones.cabezal_total if especificaciones.cabezal_total else ""}', bordered)
    worksheet.write(f'AD{num}', f'{especificaciones.succion_id if especificaciones.succion_id else ""}', bordered)
    worksheet.write(f'AE{num}', f'{especificaciones.descarga_id if especificaciones.descarga_id else ""}', bordered)
    worksheet.write(f'AF{num}', f'{especificaciones.numero_etapas if especificaciones.numero_etapas else ""}', bordered)
    worksheet.write(f'AG{num}', f'{construccion.conexion_succion if construccion.conexion_succion else ""}', bordered)
    worksheet.write(f'AH{num}', f'{construccion.tamano_rating_succion if construccion.tamano_rating_succion else ""}', bordered)
    worksheet.write(f'AI{num}', f'{construccion.conexion_descarga if construccion.conexion_descarga else ""}', bordered)
    worksheet.write(f'AJ{num}', f'{construccion.tamano_rating_descarga if construccion.tamano_rating_descarga else ""}', bordered)
    worksheet.write(f'AK{num}', f'{construccion.carcasa_dividida if construccion.carcasa_dividida else ""}', bordered)
    worksheet.write(f'AL{num}', f'{construccion.modelo_construccion if construccion.modelo_construccion else ""}', bordered)
    worksheet.write(f'AM{num}', f'{construccion.fabricante_sello if construccion.fabricante_sello else ""}', bordered)
    worksheet.write(f'AN{num}', f'{construccion.tipo if construccion.tipo else ""}', bordered)
    worksheet.write(f'AO{num}', f'{construccion.tipo_carcasa1 if construccion.tipo_carcasa1 else ""}', bordered)
    worksheet.write(f'AP{num}', f'{construccion.tipo_carcasa2 if construccion.tipo_carcasa2 else ""}', bordered)
    worksheet.write(f'AQ{num}', f'{motor.potencia_motor if motor.potencia_motor else ""}', bordered)
    worksheet.write(f'AR{num}', f'{motor.velocidad_motor if motor.velocidad_motor else ""}', bordered)
    worksheet.write(f'AS{num}', f'{motor.factor_de_servicio if motor.factor_de_servicio else ""}', bordered)
    worksheet.write(f'AT{num}', f'{motor.posicion_largo() if motor.posicion_largo else ""}', bordered)
    worksheet.write(f'AU{num}', f'{motor.voltaje if motor.voltaje else ""}', bordered)
    worksheet.write(f'AV{num}', f'{motor.fases if motor.fases else ""}', bordered)
    worksheet.write(f'AW{num}', f'{motor.frecuencia if motor.frecuencia else ""}', bordered)
    worksheet.write(f'AX{num}', f'{motor.aislamiento if motor.aislamiento else ""}', bordered)
    worksheet.write(f'AY{num}', f'{motor.arranque if motor.arranque else ""}', bordered)

    worksheet.write(f"E{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"E{num+2}", "Generado por " + request.user.get_full_name(), fecha)

    # Leyenda

    worksheet.write(f"A{num+1}", "Datos de Identificación", identificacion)
    worksheet.write(f"A{num+2}", "Condiciones de Diseño", condiciones_diseno_estilo)
    worksheet.write(f"A{num+3}", "Condiciones del Fluido", condiciones_fluido_estilo)
    worksheet.write(f"A{num+4}", "Especificaciones de la Bomba", especificaciones_estilo)
    worksheet.write(f"A{num+5}", "Especificaciones de Construcción", construccion_estilo)
    worksheet.write(f"A{num+6}", "Especificaciones del Motor", motor_estilo)

    workbook.close()

    return enviar_response(f'ficha_tecnica_bomba_centrifuga_{bomba.tag}', excel_io, fecha)

def historico_evaluaciones_bombas(object_list, request):
    '''
    Resumen:
        Función que genera el histórico XLSX de evaluaciones realizadas a una bomba filtradas de acuerdo a lo establecido en el request.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)    
    worksheet = workbook.add_worksheet()

    bomba = object_list[0].equipo
    
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 40)

    bold = workbook.add_format({'bold': True})
    bold_bordered = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    center_bordered = workbook.add_format({'border': 1})
    bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    bold_bordered.set_align('vcenter')
    center_bordered.set_align('vcenter')
    bold_bordered.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', 'Reporte de Histórico de Evaluaciones', bold)
    worksheet.insert_image(0, 4, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    worksheet.write('A5', 'Filtros', bold_bordered)
    worksheet.write('B5', 'Desde', bold_bordered)
    worksheet.write('C5', 'Hasta', bold_bordered)
    worksheet.write('D5', 'Usuario', bold_bordered)
    worksheet.write('E5', 'Nombre', bold_bordered)
    worksheet.write('F5', 'Equipo', bold_bordered)

    worksheet.write('B6', request.GET.get('desde', ''), center_bordered)
    worksheet.write('C6', Planta.objects.get(pk=request.GET.get('hasta')).nombre if request.GET.get('hasta') else '', center_bordered)
    worksheet.write('D6', Complejo.objects.get(pk=request.GET.get('usuario')).nombre if request.GET.get('usuario') else '', center_bordered)
    worksheet.write('E6', request.GET.get('nombre', ''), center_bordered)
    worksheet.write('F6', bomba.tag.upper(), center_bordered)
    num = 8

    worksheet.write(f'A{num}', '#', bold_bordered)
    worksheet.write(f'B{num}', 'Fecha', bold_bordered)
    worksheet.write(f'C{num}', "Eficiencia (%)", bold_bordered)
    worksheet.write(f'D{num}', "Potencia Calculada (%)", bold_bordered)
    worksheet.write(f"E{num}", f"Unidad Potencia", bold_bordered)
    worksheet.write(f'F{num}', "Cabezal Total", bold_bordered)
    worksheet.write(f'G{num}', "Unidad Cabezal", bold_bordered)
    worksheet.write(f"H{num}", f"Velocidad Específica (RPM)", bold_bordered)
    worksheet.write(f"I{num}", f"NPSHa", bold_bordered)
    worksheet.write(f"J{num}", f"Unidad NPSHa", bold_bordered)
    worksheet.write(f"K{num}", f"Cavita", bold_bordered)

    for i,evaluacion in enumerate(object_list):
        salida = evaluacion.salida
        entrada = evaluacion.entrada
        eficiencia = salida.eficiencia
        potencia = salida.potencia
        potencia_unidad = salida.potencia_unidad.simbolo
        cabezal_total = salida.cabezal_total
        cabezal_total_unidad = salida.cabezal_total_unidad.simbolo
        velocidad_especifica = salida.velocidad
        npsha = salida.npsha
        npsha_unidad = entrada.npshr_unidad.simbolo
        cavita = salida.cavita
        fecha_ev = evaluacion.fecha.strftime('%d/%m/%Y %H:%M')

        num += 1
        worksheet.write(f'A{num}', i+1, center_bordered)
        worksheet.write(f'B{num}', fecha_ev, center_bordered)
        worksheet.write_number(f'C{num}', eficiencia, center_bordered)
        worksheet.write_number(f'D{num}', potencia, center_bordered)
        worksheet.write(f'E{num}', potencia_unidad, bordered)
        worksheet.write_number(f'F{num}', cabezal_total, bordered)
        worksheet.write(f'G{num}', cabezal_total_unidad, bordered)
        worksheet.write_number(f'H{num}', velocidad_especifica, bordered)
        worksheet.write_number(f'I{num}', npsha, bordered)
        worksheet.write(f'J{num}', npsha_unidad, bordered)
        worksheet.write(f'K{num}', cavita, bordered)

    worksheet.write(f"J{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"J{num+2}", "Generado por " + request.user.get_full_name(), fecha)
    workbook.close()
        
    return enviar_response('historico_evaluaciones_bombas', excel_io, fecha)

# REPORTE DE VENTILADORES
def historico_evaluaciones_ventiladores(object_list, request):
    '''
    Resumen:
        Función que genera el histórico XLSX de evaluaciones realizadas a un ventilador filtradas de acuerdo a lo establecido en el request.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)    
    worksheet = workbook.add_worksheet()

    ventilador = object_list[0].equipo
    
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 40)

    bold = workbook.add_format({'bold': True})
    bold_bordered = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    center_bordered = workbook.add_format({'border': 1})
    bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    bold_bordered.set_align('vcenter')
    center_bordered.set_align('vcenter')
    bold_bordered.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', 'Reporte de Histórico de Evaluaciones', bold)
    worksheet.insert_image(0, 4, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    worksheet.write('A5', 'Filtros', bold_bordered)
    worksheet.write('B5', 'Desde', bold_bordered)
    worksheet.write('C5', 'Hasta', bold_bordered)
    worksheet.write('D5', 'Usuario', bold_bordered)
    worksheet.write('E5', 'Nombre', bold_bordered)
    worksheet.write('F5', 'Equipo', bold_bordered)

    worksheet.write('B6', request.GET.get('desde', ''), center_bordered)
    worksheet.write('C6', Planta.objects.get(pk=request.GET.get('hasta')).nombre if request.GET.get('hasta') else '', center_bordered)
    worksheet.write('D6', Complejo.objects.get(pk=request.GET.get('usuario')).nombre if request.GET.get('usuario') else '', center_bordered)
    worksheet.write('E6', request.GET.get('nombre', ''), center_bordered)
    worksheet.write('F6', ventilador.tag.upper(), center_bordered)
    num = 8

    worksheet.write(f'A{num}', '#', bold_bordered)
    worksheet.write(f'B{num}', 'Fecha', bold_bordered)
    worksheet.write(f'C{num}', "Eficiencia (%)", bold_bordered)
    worksheet.write(f'D{num}', "Potencia Calculada", bold_bordered)
    worksheet.write(f"E{num}", f"Unidad Potencia", bold_bordered)

    for i,evaluacion in enumerate(object_list):
        salida = evaluacion.salida
        eficiencia = salida.eficiencia
        
        potencia_calculada = salida.potencia_calculada
        potencia_unidad = salida.potencia_calculada_unidad
        fecha_ev = evaluacion.fecha.strftime('%d/%m/%Y %H:%M')

        num += 1
        worksheet.write(f'A{num}', i+1, center_bordered)
        worksheet.write(f'B{num}', fecha_ev, center_bordered)
        worksheet.write_number(f'C{num}', eficiencia, center_bordered)
        worksheet.write_number(f'D{num}', potencia_calculada, center_bordered)
        worksheet.write(f'E{num}', potencia_unidad.simbolo, bordered)

    worksheet.write(f"J{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"J{num+2}", "Generado por " + request.user.get_full_name(), fecha)
    workbook.close()
        
    return enviar_response('historico_evaluaciones_ventiladores', excel_io, fecha)

def ficha_tecnica_ventilador(_, ventilador, request):
    '''
    Resumen:
        Función que genera los datos de ficha técnica en formato XLSX de un ventilador de caldera.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)
    
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    identificacion = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    condiciones_generales_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'red'})
    condiciones_trabajo_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'cyan'})
    condiciones_adicionales_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'green'})
    especificaciones_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'purple'})
    center_bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    identificacion.set_align('vcenter')
    center_bordered.set_align('vcenter')
    identificacion.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', f'Ficha Técnica Ventilador {ventilador.tag}', bold)
    worksheet.insert_image(0, 7, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    num = 6

    condiciones_adicionales = ventilador.condiciones_adicionales
    condiciones_trabajo = ventilador.condiciones_trabajo
    condiciones_generales = ventilador.condiciones_generales
    especificaciones = ventilador.especificaciones

    worksheet.write(f'A{num}', 'Tag', identificacion)
    worksheet.write(f'B{num}', 'Complejo', identificacion)
    worksheet.write(f'C{num}', 'Planta', identificacion)
    worksheet.write(f'D{num}', 'Tipo', identificacion)
    worksheet.write(f'E{num}', 'Fabricante', identificacion)
    worksheet.write(f'F{num}', 'Modelo', identificacion)
    worksheet.write(f'G{num}', 'Descripción', identificacion)
    worksheet.write(f'H{num}', f'Presión Barométrica ({condiciones_generales.presion_barometrica_unidad})', condiciones_generales_estilo)
    worksheet.write(f'I{num}', f'Temp. Ambiente ({condiciones_generales.temp_ambiente_unidad})', condiciones_generales_estilo)
    worksheet.write(f'J{num}', f'Velocidad de Diseño ({condiciones_generales.velocidad_diseno_unidad})', condiciones_generales_estilo)
    worksheet.write(f'K{num}', f'Temperatura de Diseño ({condiciones_generales.temp_ambiente_unidad})', condiciones_generales_estilo)
    worksheet.write(f'L{num}', f'Presión de Diseño ({condiciones_generales.presion_barometrica_unidad})', condiciones_generales_estilo)
    worksheet.write(f'M{num}', f'Flujo ({condiciones_trabajo.flujo_unidad})', condiciones_trabajo_estilo)
    worksheet.write(f'N{num}', f'Densidad ({condiciones_trabajo.densidad_unidad})', condiciones_trabajo_estilo)
    worksheet.write(f'O{num}', f'Presión Entrada ({condiciones_trabajo.presion_unidad})', condiciones_trabajo_estilo)
    worksheet.write(f'P{num}', f'Presión Salida ({condiciones_trabajo.presion_unidad}G)', condiciones_trabajo_estilo)
    worksheet.write(f'Q{num}', f'Veloc. Func. ({condiciones_trabajo.velocidad_funcionamiento_unidad})', condiciones_trabajo_estilo)
    worksheet.write(f'R{num}', f'Temperatura ({condiciones_trabajo.temperatura_unidad})', condiciones_trabajo_estilo)
    worksheet.write(f'S{num}', f'Potencia Ventilador ({condiciones_trabajo.potencia_freno_unidad})', condiciones_trabajo_estilo)
    worksheet.write(f'T{num}', f'Potencia de Freno ({condiciones_trabajo.potencia_freno_unidad})', condiciones_trabajo_estilo)
    worksheet.write(f'U{num}', f'Flujo ({condiciones_adicionales.flujo_unidad})', condiciones_adicionales_estilo)
    worksheet.write(f'V{num}', f'Densidad ({condiciones_adicionales.densidad_unidad})', condiciones_adicionales_estilo)
    worksheet.write(f'W{num}', f'Presión Entrada ({condiciones_adicionales.presion_unidad})', condiciones_adicionales_estilo)
    worksheet.write(f'X{num}', f'Presión Salida ({condiciones_adicionales.presion_unidad}G)', condiciones_adicionales_estilo)
    worksheet.write(f'Y{num}', f'Veloc. Func. ({condiciones_adicionales.velocidad_funcionamiento_unidad})', condiciones_adicionales_estilo)
    worksheet.write(f'Z{num}', f'Temperatura ({condiciones_adicionales.temperatura_unidad})', condiciones_adicionales_estilo)
    worksheet.write(f'AA{num}', f'Potencia Ventilador ({condiciones_adicionales.potencia_freno_unidad})', condiciones_adicionales_estilo)
    worksheet.write(f'AB{num}', f'Potencia de Freno ({condiciones_adicionales.potencia_freno_unidad})', condiciones_adicionales_estilo)
    worksheet.write(f'AC{num}', f'Espesor Carcasa ({especificaciones.espesor_unidad})', especificaciones_estilo)
    worksheet.write(f'AD{num}', f'Espesor Caja Entrada ({especificaciones.espesor_unidad})', especificaciones_estilo)
    worksheet.write(f'AE{num}', f'Sello del Eje', especificaciones_estilo)
    worksheet.write(f'AF{num}', f'Lubricante', especificaciones_estilo)
    worksheet.write(f'AG{num}', f'Refrigerante', especificaciones_estilo)
    worksheet.write(f'AH{num}', f'Diámetro', especificaciones_estilo)
    worksheet.write(f'AI{num}', f'Motor', especificaciones_estilo)
    worksheet.write(f'AJ{num}', f'Acceso de Aire', especificaciones_estilo)
    worksheet.write(f'AK{num}', f'Potencia Motor ({especificaciones.potencia_motor_unidad})', especificaciones_estilo)
    worksheet.write(f'AL{num}', f'Velocidad Motor ({especificaciones.velocidad_motor_unidad})', especificaciones_estilo)

    num += 1
    
    worksheet.write(f'A{num}', ventilador.tag, identificacion)
    worksheet.write(f'B{num}', ventilador.planta.complejo.nombre, identificacion)
    worksheet.write(f'C{num}', ventilador.planta.nombre, identificacion)
    worksheet.write(f'D{num}', ventilador.tipo_ventilador.nombre, identificacion)
    worksheet.write(f'E{num}', ventilador.fabricante, identificacion)
    worksheet.write(f'F{num}', ventilador.modelo, identificacion)
    worksheet.write(f'G{num}', ventilador.descripcion, identificacion)
    worksheet.write(f'H{num}', condiciones_generales.presion_barometrica, condiciones_generales_estilo)
    worksheet.write(f'I{num}', condiciones_generales.temp_ambiente, condiciones_generales_estilo)
    worksheet.write(f'J{num}', condiciones_generales.velocidad_diseno, condiciones_generales_estilo)
    worksheet.write(f'K{num}', condiciones_generales.temp_diseno, condiciones_generales_estilo)
    worksheet.write(f'L{num}', condiciones_generales.presion_diseno, condiciones_generales_estilo)
    worksheet.write(f'M{num}', condiciones_trabajo.flujo, condiciones_trabajo_estilo)
    worksheet.write(f'N{num}', condiciones_trabajo.densidad, condiciones_trabajo_estilo)
    worksheet.write(f'O{num}', condiciones_trabajo.presion_entrada, condiciones_trabajo_estilo)
    worksheet.write(f'P{num}', condiciones_trabajo.presion_salida, condiciones_trabajo_estilo)
    worksheet.write(f'Q{num}', condiciones_trabajo.velocidad_funcionamiento, condiciones_trabajo_estilo)
    worksheet.write(f'R{num}', condiciones_trabajo.temperatura, condiciones_trabajo_estilo)
    worksheet.write(f'S{num}', condiciones_trabajo.potencia, condiciones_trabajo_estilo)
    worksheet.write(f'T{num}', condiciones_trabajo.potencia_freno, condiciones_trabajo_estilo)
    worksheet.write(f'U{num}', condiciones_adicionales.flujo, condiciones_adicionales_estilo)
    worksheet.write(f'V{num}', condiciones_adicionales.densidad, condiciones_adicionales_estilo)
    worksheet.write(f'W{num}', condiciones_adicionales.presion_entrada, condiciones_adicionales_estilo)
    worksheet.write(f'X{num}', condiciones_adicionales.presion_salida, condiciones_adicionales_estilo)
    worksheet.write(f'Y{num}', condiciones_adicionales.velocidad_funcionamiento, condiciones_adicionales_estilo)
    worksheet.write(f'Z{num}', condiciones_adicionales.temperatura, condiciones_adicionales_estilo)
    worksheet.write(f'AA{num}', condiciones_adicionales.potencia, condiciones_adicionales_estilo)
    worksheet.write(f'AB{num}', condiciones_adicionales.potencia_freno, condiciones_adicionales_estilo)
    worksheet.write(f'AC{num}', especificaciones.espesor, especificaciones_estilo)
    worksheet.write(f'AD{num}', especificaciones.espesor_caja, especificaciones_estilo)
    worksheet.write(f'AE{num}', especificaciones.sello, especificaciones_estilo)
    worksheet.write(f'AF{num}', especificaciones.lubricante, especificaciones_estilo)
    worksheet.write(f'AG{num}', especificaciones.refrigerante, especificaciones_estilo)
    worksheet.write(f'AH{num}', especificaciones.diametro, especificaciones_estilo)
    worksheet.write(f'AI{num}', especificaciones.motor, especificaciones_estilo)
    worksheet.write(f'AJ{num}', especificaciones.acceso_aire, especificaciones_estilo)
    worksheet.write(f'AK{num}', especificaciones.potencia_motor, especificaciones_estilo)
    worksheet.write(f'AL{num}', especificaciones.velocidad_motor, especificaciones_estilo)

    worksheet.write(f"J{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"J{num+2}", "Generado por " + request.user.get_full_name(), fecha)

    worksheet.write(f"A{num+2}", "Datos de Identificación", identificacion)
    worksheet.write(f"A{num+3}", "Condiciones de Trabajo", condiciones_trabajo_estilo)
    worksheet.write(f"A{num+4}", "Condiciones Adicionales", condiciones_adicionales_estilo)
    worksheet.write(f"A{num+5}", "Especificaciones del Ventilador", especificaciones_estilo)
    workbook.close()
        
    return enviar_response(f'ficha_tecnica_ventilador_{ventilador.tag}', excel_io, fecha)

# REPORTE DE TURBINAS DE VAPOR
def historico_evaluaciones_turbinas_vapor(object_list, request):
    '''
    Resumen:
        Función que genera el histórico XLSX de evaluaciones realizadas a una turbina de vapor filtradas de acuerdo a lo establecido en el request.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)    
    worksheet = workbook.add_worksheet()

    ventilador = object_list[0].equipo
    
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 40)

    bold = workbook.add_format({'bold': True})
    bold_bordered = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    center_bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    bold_bordered.set_align('vcenter')
    center_bordered.set_align('vcenter')
    bold_bordered.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', 'Reporte de Histórico de Evaluaciones', bold)
    worksheet.insert_image(0, 4, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    worksheet.write('A5', 'Filtros', bold_bordered)
    worksheet.write('B5', 'Desde', bold_bordered)
    worksheet.write('C5', 'Hasta', bold_bordered)
    worksheet.write('D5', 'Usuario', bold_bordered)
    worksheet.write('E5', 'Nombre', bold_bordered)
    worksheet.write('F5', 'Equipo', bold_bordered)

    worksheet.write('B6', request.GET.get('desde', ''), center_bordered)
    worksheet.write('C6', Planta.objects.get(pk=request.GET.get('hasta')).nombre if request.GET.get('hasta') else '', center_bordered)
    worksheet.write('D6', Complejo.objects.get(pk=request.GET.get('usuario')).nombre if request.GET.get('usuario') else '', center_bordered)
    worksheet.write('E6', request.GET.get('nombre', ''), center_bordered)
    worksheet.write('F6', ventilador.tag.upper(), center_bordered)
    num = 8

    worksheet.write(f'A{num}', '#', bold_bordered)
    worksheet.write(f'B{num}', 'Fecha', bold_bordered)
    worksheet.write(f'C{num}', "Eficiencia (%)", bold_bordered)
    worksheet.write(f'D{num}', "Potencia Calculada", bold_bordered)
    worksheet.write(f"E{num}", f"Unidad Potencia", bold_bordered)

    for i,evaluacion in enumerate(object_list):
        salida = evaluacion.salida
        eficiencia = salida.eficiencia
        
        potencia_calculada = salida.potencia_calculada
        fecha_ev = evaluacion.fecha.strftime('%d/%m/%Y %H:%M')

        num += 1
        worksheet.write(f'A{num}', i+1, center_bordered)
        worksheet.write(f'B{num}', fecha_ev, center_bordered)
        worksheet.write_number(f'C{num}', eficiencia, center_bordered)
        worksheet.write_number(f'D{num}', potencia_calculada, center_bordered)
        worksheet.write(f"E{num}", evaluacion.entrada.potencia_real_unidad.simbolo, center_bordered)

    worksheet.write(f"J{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"J{num+2}", "Generado por " + request.user.get_full_name(), fecha)
    workbook.close()
        
    return enviar_response('historico_evaluaciones_turbinas_vapor', excel_io, fecha)

def ficha_tecnica_turbina_vapor(_, turbina, request):
    '''
    Resumen:
        Función que genera los datos de ficha técnica en formato XLSX de una Turbina de Vapor.
    '''
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)
    
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    identificacion = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'yellow'})
    especificaciones_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'red'})
    corrientes_estilo = workbook.add_format({'bold': True, 'border': 1,'bg_color': 'cyan'})
    center_bordered = workbook.add_format({'border': 1})
    fecha =  workbook.add_format({'border': 1})

    fecha.set_align('right')
    identificacion.set_align('vcenter')
    center_bordered.set_align('vcenter')
    identificacion.set_align('center')
    center_bordered.set_align('center')

    worksheet.insert_image(0, 0, BASE_DIR.__str__() + '\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', f'Ficha Técnica Turbina de Vapor {turbina.tag}', bold)
    worksheet.insert_image(0, 7, BASE_DIR.__str__() + '\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    num = 6

    especificaciones = turbina.especificaciones

    worksheet.write(f'A{num}', 'Tag', identificacion)
    worksheet.write(f'B{num}', 'Complejo', identificacion)
    worksheet.write(f'C{num}', 'Planta', identificacion)
    worksheet.write(f'D{num}', 'Fabricante', identificacion)
    worksheet.write(f'E{num}', 'Modelo', identificacion)
    worksheet.write(f'F{num}', 'Descripción', identificacion)
    worksheet.write(f'G{num}', f'Potencia ({especificaciones.potencia_unidad})', especificaciones_estilo)
    worksheet.write(f'H{num}', f'Potencia Máxima ({especificaciones.potencia_unidad})', especificaciones_estilo)
    worksheet.write(f'I{num}', f'Velocidad ({especificaciones.velocidad_unidad})', especificaciones_estilo)
    worksheet.write(f'J{num}', f'Presión de Entrada ({especificaciones.presion_entrada_unidad}g)', especificaciones_estilo)
    worksheet.write(f'K{num}', f'Temperatura de Entrada ({especificaciones.temperatura_entrada_unidad})', especificaciones_estilo)
    worksheet.write(f'L{num}', f'Contra Presión ({especificaciones.contra_presion_unidad})', especificaciones_estilo)

    num += 1
    
    worksheet.write(f'A{num}', turbina.tag, center_bordered)
    worksheet.write(f'B{num}', turbina.planta.complejo.nombre, center_bordered)
    worksheet.write(f'C{num}', turbina.planta.nombre, center_bordered)
    worksheet.write(f'D{num}', turbina.fabricante, center_bordered)
    worksheet.write(f'E{num}', turbina.modelo, center_bordered)
    worksheet.write(f'F{num}', turbina.descripcion, center_bordered)
    worksheet.write(f'G{num}', especificaciones.potencia, center_bordered)
    worksheet.write(f'H{num}', especificaciones.potencia_max, center_bordered)
    worksheet.write(f'I{num}', especificaciones.velocidad, center_bordered)
    worksheet.write(f'J{num}', especificaciones.presion_entrada, center_bordered)
    worksheet.write(f'K{num}', especificaciones.temperatura_entrada, center_bordered)
    worksheet.write(f'L{num}', especificaciones.contra_presion, center_bordered)

    num += 2
    worksheet.write(f'A{num}', "Datos de las Corrientes Circulantes por la Turbina", corrientes_estilo)

    num += 1
    datos_corrientes = turbina.datos_corrientes
    flujo_unidad = datos_corrientes.flujo_unidad
    entalpia_unidad = datos_corrientes.entalpia_unidad
    presion_unidad = datos_corrientes.presion_unidad
    temperatura_unidad = datos_corrientes.temperatura_unidad

    worksheet.write(f'A{num}', "# Corriente", corrientes_estilo)
    worksheet.write(f'B{num}', "Descripción", corrientes_estilo)
    worksheet.write(f'C{num}', f"Flujo ({flujo_unidad})", corrientes_estilo)
    worksheet.write(f'D{num}', f"Entalpía ({entalpia_unidad})", corrientes_estilo)
    worksheet.write(f'E{num}', f"Presión ({presion_unidad}g)", corrientes_estilo)
    worksheet.write(f'F{num}', f"Temperatura ({temperatura_unidad})", corrientes_estilo)
    worksheet.write(f'G{num}', "Fase", corrientes_estilo)

    for corriente in datos_corrientes.corrientes.all():
        num += 1
        
        worksheet.write(f'A{num}', corriente.numero_corriente, center_bordered)
        worksheet.write(f'B{num}', corriente.descripcion_corriente, center_bordered)
        worksheet.write(f'C{num}', corriente.flujo, center_bordered)
        worksheet.write(f'D{num}', corriente.entalpia, center_bordered)
        worksheet.write(f'E{num}', corriente.presion, center_bordered)
        worksheet.write(f'F{num}', corriente.temperatura, center_bordered)
        worksheet.write(f'G{num}', corriente.fase_largo(), center_bordered)

    worksheet.write(f"J{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"J{num+2}", "Generado por " + request.user.get_full_name(), fecha)

    worksheet.write(f"A{num+2}", "Datos de Identificación", identificacion)
    worksheet.write(f"A{num+3}", "Especificaciones", especificaciones_estilo)
    worksheet.write(f"A{num+4}", "Corrientes", corrientes_estilo)
    workbook.close()
        
    return enviar_response(f'ficha_tecnica_turbina_vapor_{turbina.tag}', excel_io, fecha)
