from reportlab.platypus import Table, Image, Paragraph, TableStyle, Table, SimpleDocTemplate, Spacer
from django.db.models import Sum
from reportlab.lib.pagesizes import A4
from io import BytesIO
from reportlab.lib.styles import ParagraphStyle
import datetime
from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.lib import colors
from intercambiadores.models import Planta, Complejo

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
        footer.drawOn(canvas,40,745)

        time = Paragraph(date, headerStyle)
        time.wrapOn(canvas, width, height)
        time.drawOn(canvas,470,745)

        canvas.restoreState()

        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "Página %d" % (doc.page)
        canvas.drawCentredString(
            4 * inch,
            0.3 * inch,
            page_number_text + ', ' + reportHeader + ', ' + date + '.'
        )
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

    if(len(request.GET)):
        story.append(Paragraph("Datos de Filtrado", centrar_parrafo))
        table = [[Paragraph("Tag", centrar_parrafo), Paragraph("Servicio", centrar_parrafo), Paragraph("Planta", centrar_parrafo), Paragraph("Complejo", centrar_parrafo)]]
        table.append([
            Paragraph(request.GET['tag'], parrafo_tabla),
            Paragraph(request.GET['servicio'], parrafo_tabla),
            Paragraph(Planta.objects.get(pk=request.GET.get('planta')).nombre if request.GET.get('planta') else '', parrafo_tabla),
            Paragraph(Complejo.objects.get(pk=request.GET.get('complejo')).nombre if request.GET.get('complejo') else '', parrafo_tabla),
        ])

        table = Table(table)
        table.setStyle(basicTableStyle)

        story.append(table)
        story.append(Spacer(0,7))

    table = [[Paragraph("#", centrar_parrafo), Paragraph("Tag", centrar_parrafo), Paragraph("Servicio", centrar_parrafo), Paragraph("Planta", centrar_parrafo)]]
    for n,x in enumerate(object_list):
        table.append([
            Paragraph(str(n+1), numero_tabla),
            Paragraph(x.intercambiador.tag, parrafo_tabla),
            Paragraph(x.intercambiador.servicio, parrafo_tabla),
            Paragraph(x.intercambiador.planta.nombre, parrafo_tabla)
        ])
        
    table = Table(table, colWidths=[0.5*inch, 2*inch, 3.2*inch, 1.5*inch])
    table.setStyle(basicTableStyle)
    story.append(table)
    return story