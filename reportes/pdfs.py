from reportlab.platypus import Table, Image, Paragraph, TableStyle, Table, SimpleDocTemplate, Spacer
from django.db.models import Sum
from reportlab.lib.pagesizes import A4
from io import BytesIO
from reportlab.lib.styles import ParagraphStyle
import datetime
from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.lib import colors
import numpy as np

# Aquí irán los reportes en formato PDF

prefijo = '' #Cambiar al hacer deployment en PythonAnywhere

basicTableStyle = TableStyle(
        [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.85, 0.85, 0.85))
        ])

headerStyle = ParagraphStyle(
            'header',
            fontSize=8,
            fontFamily='Junge',
            textTransform='uppercase'
    )

estiloMontos = TableStyle(
        [
            ('LINEABOVE', (0,1), (-1, 1), 1 ,colors.black),
            ('LINEABOVE', (0,2), (-1,-1), 1 ,colors.black, None, (2,2)),
            ('LINEBELOW', (0,2), (-1,-1), 1 ,colors.black, None, (2,2)),
            ('LINEBELOW', (0,2), (-2,-2), 1 ,colors.black, None, (2,2)),
        ])

centrar_parrafo = ParagraphStyle('', alignment=1)
parrafo_tabla = ParagraphStyle('', fontSize=9)
numero_tabla = ParagraphStyle('', fontSize=9, alignment=1)

def generar_pdf(request,object_list,titulo,reporte):
    def primera_pagina(canvas, doc):
        width, height = A4
        canvas.saveState()
        titleStyle = ParagraphStyle(
            'title',
            fontSize=20,
            fontFamily='Junge',
            textTransform='uppercase',
            alignment=1,
            leading=24,
            color = colors.red
        )
        
        i = Image('static/img/logo.png',width=55,height=55)
        i.wrapOn(canvas,width,height)
        i.drawOn(canvas,40,760)

        i = Image('static/img/icono_indesca.png',width=55,height=55)
        i.wrapOn(canvas,width,height)
        i.drawOn(canvas,500,760)

        header = Paragraph(reportHeader, titleStyle)
        header.wrapOn(canvas, width-200, height+350)
        header.drawOn(canvas,100,765)

        footer = Paragraph(f'<p>Reporte generado por el usuario {request.user.get_full_name()}. </p>', headerStyle)
        footer.wrapOn(canvas, width, height)
        footer.drawOn(canvas,30,745)

        time = Paragraph(date, headerStyle)
        time.wrapOn(canvas, width, height)
        time.drawOn(canvas,470,745)

        canvas.restoreState()

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "Página %d" % (doc.page)
        canvas.drawCentredString(
            4 * inch,
            0.3 * inch,
            page_number_text + ', ' + reportHeader + ', ' + date + '.'
        )
        canvas.restoreState()

    reportHeader = titulo
    
    date = datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,pagesize=A4, topMargin=30, bottomMargin=30)
    story = []
    
    fechaHeadingStyle = ParagraphStyle(
        'fechaHeading',
        fontSize=8.6,
    )

    fechaStyle = ParagraphStyle(
        'fecha',
        fontSize=6.5,
    )

    story = generar_historia(request, reporte, object_list)

    doc.build(story, 
        onFirstPage=primera_pagina,
        onLaterPages=add_footer,
    )
      
    response = HttpResponse(content_type='application/pdf')

    response.write(buff.getvalue())
    buff.close()

    return response

def generar_historia(request, reporte, object_list):
    # Colocar los tipos de reporte de la siguiente forma:
    if reporte == 'intercambiadores_tubo_carcasa':
        return intercambiadores_tubo_carcasa(request, object_list)

def intercambiadores_tubo_carcasa(request, object_list):
    story = []
    story.append(Spacer(0,60))
    
    table = [[Paragraph("#", centrar_parrafo), Paragraph("Tag", centrar_parrafo), Paragraph("Servicio", centrar_parrafo), Paragraph("Planta", centrar_parrafo)]]
    for n,x in enumerate(object_list):
        table.append([
            Paragraph(str(n+1), numero_tabla),
            Paragraph(x.intercambiador.tag, parrafo_tabla),
            Paragraph(x.intercambiador.servicio, parrafo_tabla),
            Paragraph(x.intercambiador.planta.complejo.nombre, parrafo_tabla)
        ])
        
    table = Table(table, colWidths=[0.5*inch, 2*inch, 3.2*inch, 1.5*inch])
    table.setStyle(basicTableStyle)
    story.append(table)
    return story

def estado_cuenta(request, object_list):
    import locale
    locale.setlocale(locale.LC_TIME, "es_VE")
    date = datetime.datetime.now().strftime('%a, %d/%m/%Y %H:%M:%S')

    tabla = Table([[Paragraph("REPÚBLICA BOLIVARIANA DE VENEZUELA", ParagraphStyle('', alignment=1)), Paragraph(f'<b>FECHA DE EXPEDICIÓN:</b> {date}', ParagraphStyle('', alignment=2))],
        [Paragraph("ALCALDÍA BOLIVARIANA DEL MUNICIPIO SUCRE", ParagraphStyle('', alignment=1)), Paragraph(f'<b>PATENTE: {object_list[0].cod_con.numpatente}</b>', ParagraphStyle('', alignment=2, textColor=colors.red)) if object_list[0].cod_con else ''],
        [Paragraph("DIRECCIÓN DE ADMINISTRACIÓN TRIBUTARIA", ParagraphStyle('', alignment=1)), ''],
        [Paragraph("G-20001595-0", ParagraphStyle('', alignment=1)), '']], colWidths=(6*inch, 2*inch), hAlign="RIGHT")

    story = [tabla, Spacer(0, 20), Paragraph("<b>ESTADO DE CUENTA</b>", ParagraphStyle('', alignment=1, fontSize=15)), Spacer(0,10)]

    if object_list[0].cod_con:
        tabla_contr = Table([
            [Paragraph("<b>RUBRO:</b>"), "PATENTE DE VEHÍCULOS"],
            [Paragraph("<b>CÉDULA / RIF:</b>"), Paragraph(object_list[0].cod_con.ced_rif)],
            [Paragraph("<b>NOMBRE:</b>"), Paragraph(object_list[0].cod_con.nom_con.upper())],
            [Paragraph("<b> DIRECCIÓN:</b>"), Paragraph(object_list[0].cod_con.dir_cont.upper())],
        ], colWidths=(2*inch, 7.5*inch), hAlign="CENTER")
    else:
        tabla_contr = Table([
            [Paragraph("<b>RUBRO:</b>"), "PATENTE DE VEHÍCULOS"],
            [Paragraph("<b>CÉDULA / RIF:</b>"), Paragraph(object_list[0].ced_rif)],
            [Paragraph("<b>NOMBRE:</b>"), Paragraph(object_list[0].dueno().nombre_apellido.upper())],
            [Paragraph("<b> DIRECCIÓN:</b>"), Paragraph(object_list[0].dueno().direccion.upper())],
        ], colWidths=(2*inch, 7.5*inch), hAlign="CENTER")        

    tabla_contr.setStyle(basicTableStyle)
    story.append(tabla_contr)

    total_deuda = 0

    tdata = [[Paragraph("<b>DESCRIPCIÓN</b>"), Paragraph("<b>SIN DESCUENTO</b>"),
            Paragraph("<b>DESCUENTO</b>"), Paragraph("<b>MONTO</b>")]]

    for v in object_list:
        total = 0
        pendientes = Rcrecveh.objects.filter(cod_veh = v.cod_veh, descripcion__isnull = True, estutus = 0)
        if pendientes.exists() and not v.exo_veh:
            ano = pendientes.first().fec_rec.year - 1
            for p in pendientes:
                if (ano != p.fec_rec.year and not (p.fec_rec.year - 1 == ano and p.fec_rec.month == 1)):
                    ano += 1

                    if len(tdata) > 1 or 'descripcion' in locals():
                        tdata.append([descripcion, str(total_local), "0.00", str(total_local)])
                    
                    descripcion = f"{v.pla_veh} {p.fec_rec.year} I " if p.fec_rec.month == 4 else f"{v.pla_veh} {p.fec_rec.year} II " if p.fec_rec.month == 7 else f"{v.pla_veh} {p.fec_rec.year} III "  if p.fec_rec.month == 10 else f"{v.pla_veh} {p.fec_rec.year-1} IV "
                    total_local = 0
                elif((p.fec_rec.year == ano + 1 and p.fec_rec.month == 1) and ('descripcion' in locals() and str(p.fec_rec.year-1) not in descripcion)):
                    if len(tdata) > 1 or 'descripcion' in locals():
                        tdata.append([descripcion, str(total_local), "0.00", str(total_local)])
                    descripcion = f"{v.pla_veh} {p.fec_rec.year} I " if p.fec_rec.month == 4 else f"{v.pla_veh} {p.fec_rec.year} II " if p.fec_rec.month == 7 else f"{v.pla_veh} {p.fec_rec.year} III "  if p.fec_rec.month == 10 else f"{v.pla_veh} {p.fec_rec.year-1} IV "
                    total_local = 0
                else:
                    try:
                        print(2)
                        descripcion += f"I " if p.fec_rec.month == 4 else f"II " if p.fec_rec.month == 7 else f"III "  if p.fec_rec.month == 10 else f"IV "
                    except:
                        print(3)
                        descripcion = f"{v.pla_veh} {p.fec_rec.year} I " if p.fec_rec.month == 4 else f"{v.pla_veh} {p.fec_rec.year} II " if p.fec_rec.month == 7 else f"{v.pla_veh} {p.fec_rec.year} III "  if p.fec_rec.month == 10 else f"{v.pla_veh} {p.fec_rec.year-1} IV "
                
                if 'total_local' not in locals():
                    total_local = 0

                total_local += p.mon_pag
                total += p.mon_pag
            
            total_deuda += total
        elif v.exo_veh:
            descripcion = f"{v.pla_veh} - EXONERADO"
            total_local = 0
    
    try:
        tdata.append([descripcion, str(total_local), "0.00", str(total_local)])
    except:
        print("Sin datos")
    
    tabla = Table(tdata, colWidths=(4*inch, 1.83*inch,1.83*inch,1.83*inch))
    tabla.setStyle(estiloMontos)
    story.append(tabla)

    tabla = Table([
        ['', Paragraph(f"<b>SUBTOTAL Bs:</b>"), Paragraph(f'Bs. {total_deuda}')],
        [Paragraph(f"<b>ELABORADO POR:</b> {request.session['usuario']['nombre']}"), Paragraph("<b>TOTAL DESCUENTO:</b>"), Paragraph(f"{0.00}")],
        [Paragraph(f"<b>VALOR DEL PETRO:</b> Bs. {CotizacionPetro.objects.last().valor}"),Paragraph("<b>TOTAL Bs:</b>"), Paragraph(f"<b>Bs. {total_deuda}</b>")],
        [Paragraph("<b>VÁLIDO POR 5 DÍAS</b>"),Paragraph(f"<b>TOTAL Pt:</b>"), Paragraph(f"{round(total_deuda/CotizacionPetro.objects.last().valor, 6)}")]]
    , colWidths=(5.83*inch,1.83*inch,1.83*inch), hAlign="RIGHT")

    tabla.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1, 0), 1 ,colors.black),
    ]))
    story.append(tabla)

    return story