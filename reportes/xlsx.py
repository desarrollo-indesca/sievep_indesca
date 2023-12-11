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