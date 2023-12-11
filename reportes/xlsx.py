import xlsxwriter
import datetime
from django.http import HttpResponse
from io import BytesIO
from intercambiadores.models import Planta, Complejo
from simulaciones_pequiven.settings import BASE_DIR
from calculos.unidades import transformar_unidades_presion

# Aquí irán los reportes en formato Excel
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def historico_evaluaciones(object_list, request):
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
        area = float(evaluacion.area_transferencia)
        eficiencia = float(evaluacion.eficiencia)
        efectividad = float(evaluacion.efectividad)
        ntu = float(evaluacion.ntu)
        u = float(evaluacion.u)
        caida_tubo, caida_carcasa = transformar_unidades_presion([evaluacion.caida_presion_in, evaluacion.caida_presion_ex], evaluacion.unidad_presion.pk, condicion_carcasa.unidad_presion.pk)
        ensuciamiento = float(evaluacion.ensuciamiento)
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
        
    response = HttpResponse(content_type='application/ms-excel', content=excel_io.getvalue())
    
    return response

def ficha_tecnica_tubo_carcasa_xlsx(intercambiador, request):
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
    worksheet.write(f'H{num}', f'{propiedades.fluido_carcasa}', bordered)
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
    worksheet.write(f'W{num}', f'{propiedades.fluido_tubo}', bordered)
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
    worksheet.write(f'AQ{num}', f'{propiedades.ensuciamiento})', bordered)
    worksheet.write(f'AR{num}', f'{propiedades.area})', bordered)
    worksheet.write(f'AS{num}', f'{propiedades.arreglo_serie})', bordered)
    worksheet.write(f'AT{num}', f'{propiedades.arreglo_paralelo})', bordered)
    worksheet.write(f'AU{num}', f'{propiedades.numero_tubos})', bordered)
    worksheet.write(f'AV{num}', f'{propiedades.longitud_tubos})', bordered)
    worksheet.write(f'AW{num}', f'{propiedades.diametro_externo_tubos})', bordered)
    worksheet.write(f'AX{num}', f'{propiedades.diametro_interno_carcasa})', bordered)
    worksheet.write(f'AY{num}', f'{propiedades.pitch_tubos})', bordered)
    worksheet.write(f'AZ{num}', f'{propiedades.tipo_tubo})', bordered)
    worksheet.write(f'BA{num}', f'{propiedades.material_carcasa}', bordered)
    worksheet.write(f'BB{num}', f'{propiedades.material_tubo}', bordered)
    worksheet.write(f'BC{num}', f'{propiedades.criticidad_larga()}', bordered)

    worksheet.write(f"E{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"E{num+2}", "Generado por " + request.user.get_full_name(), fecha)
    workbook.close()
    
    response = HttpResponse(content_type='application/ms-excel', content=excel_io.getvalue())
    
    return response


def reporte_tubo_carcasa(object_list, request):
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
    worksheet.write('C1', 'Reporte de Intercambiadores Tubo/Carcasa', bold)
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

    for i,intercambiador in enumerate(object_list):
        num += 1
        worksheet.write_number(f'A{num}', i+1, center_bordered)
        worksheet.write(f'B{num}', intercambiador.intercambiador.tag, center_bordered)
        worksheet.write(f'C{num}', intercambiador.intercambiador.planta.nombre, center_bordered)
        worksheet.write(f'D{num}', intercambiador.intercambiador.planta.complejo.nombre, center_bordered)
        worksheet.write(f'E{num}', intercambiador.intercambiador.servicio, bordered)
    
    worksheet.write(f"E{num+1}", datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), fecha)
    worksheet.write(f"E{num+2}", "Generado por " + request.user.get_full_name(), fecha)
    workbook.close()
    
    response = HttpResponse(content_type='application/ms-excel', content=excel_io.getvalue())
    
    return response