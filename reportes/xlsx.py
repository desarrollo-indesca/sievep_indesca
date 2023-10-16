import xlsxwriter
import datetime
from django.http import HttpResponse
from io import BytesIO
from intercambiadores.models import Planta, Complejo
from simulaciones_pequiven.settings import BASE_DIR

# Aquí irán los reportes en formato Excel
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def reporte_tubo_carcasa(object_list, request): # JUSTO AHORA SOLO ESTÁ LA PRUEBA
    excel_io = BytesIO()
    workbook = xlsxwriter.Workbook(excel_io)
    
    hora = datetime.datetime.now()
    nombre = f'reporte_tubo_carcasa_{hora.day}_{hora.hour}_{hora.second}_{hora.microsecond}.xlsx'
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 40)

    # Add a bold format to use to highlight cells.
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