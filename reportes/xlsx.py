import xlsxwriter
import datetime

# Aquí irán los reportes en formato Excel
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def reporte_tubo_carcasa(object_list): # JUSTO AHORA SOLO ESTÁ LA PRUEBA
    hora = datetime.datetime.now()
    nombre = f'reporte_tubo_carcasa_{hora.day}_{hora.hour}_{hora.second}_{hora.microsecond}.xlsx'
    workbook = xlsxwriter.Workbook(nombre)
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 20)

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    center = workbook.add_format()

    bold.set_align('vcenter')
    center.set_align('vcenter')
    bold.set_align('center')
    center.set_align('center')

    worksheet.insert_image(0, 0, 'C:\\Users\\rurdaneta\\sievep\\sievep_indesca\\static\\img\\logo.png', {'x_scale': 0.25, 'y_scale': 0.25})
    worksheet.write('C1', 'Reporte de Intercambiadores Tubo/Carcasa', bold)
    worksheet.insert_image(0, 4, 'C:\\Users\\rurdaneta\\sievep\\sievep_indesca\\static\\img\\icono_indesca.png', {'x_scale': 0.1, 'y_scale': 0.1})

    worksheet.write('A5', '#', bold)
    worksheet.write('B5', 'Tag', bold)
    worksheet.write('C5', 'Planta', bold)
    worksheet.write('D5', 'Complejo', bold)
    worksheet.write('E5', 'Servicio', bold)

    num = 6
    for i,intercambiador in enumerate(object_list):
        worksheet.write_number(f'A{num}', i+1, center)
        worksheet.write(f'B{num}', intercambiador.intercambiador.tag, center)
        worksheet.write(f'C{num}', intercambiador.intercambiador.planta.nombre, center)
        worksheet.write(f'D{num}', intercambiador.intercambiador.planta.complejo.nombre, center)
        worksheet.write(f'E{num}', intercambiador.intercambiador.servicio)
        
        num += 1

    workbook.close()

    return nombre