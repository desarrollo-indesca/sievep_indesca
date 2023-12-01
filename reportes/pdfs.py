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

sombreado = colors.Color(0.85, 0.85, 0.85)

basicTableStyle = TableStyle(
        [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), sombreado)
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
    '''
    Resumen:
        Función que genera un reporte en formato PDF dado el request, objetos, título y código del reporte.

    Parámetros:
        request: Petición HTTP
        object_list: Lista de objetos a mostrar en el reporte
        titulo: Título del reporte
        reporte: Código del reporte

    Devuelve:
        Un objeto HttpResponse con el reporte en formato PDF. Este simplemente debe ser enviado como respuesta al cliente.
    '''
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

    if reporte == 'ficha_tecnica_tubo_carcasa':
        return ficha_tecnica_tubo_carcasa(request, object_list)

def reporte_evaluacion(request, object_list):
    pass

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

def ficha_tecnica_tubo_carcasa(request, object_list):
    story = []
    story.append(Spacer(0,90))
    intercambiador = object_list

    # Primera Tabla: Datos Generales
    table = [
        [
            Paragraph("Tag", centrar_parrafo), 
            Paragraph(f"{intercambiador.tag}", centrar_parrafo), 
            Paragraph("Planta", centrar_parrafo),
            Paragraph(f"{intercambiador.planta.nombre}", centrar_parrafo)
        ],
        [
            Paragraph("Fabricante", centrar_parrafo), 
            Paragraph(f"{intercambiador.fabricante}", centrar_parrafo), 
            Paragraph("Tema", centrar_parrafo),
            Paragraph(f"{intercambiador.tema.codigo.upper()}", centrar_parrafo)
        ],
        [
            Paragraph("Flujo", centrar_parrafo), 
            Paragraph(f"{intercambiador.flujo_largo()}", centrar_parrafo), 
            Paragraph("Tipo", centrar_parrafo), 
            Paragraph(f"Tubo/Carcasa", centrar_parrafo), 
        ],
        [
            Paragraph("Servicio", centrar_parrafo), 
            Paragraph(f"{intercambiador.servicio}", centrar_parrafo)
        ],
        [
            Paragraph("Condiciones de Diseño", centrar_parrafo)
        ]
    ]
    estilo = TableStyle(
        [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (0, 3), sombreado),
            ('BACKGROUND', (2, 0), (2, 2), sombreado),
            ('SPAN', (1, 3), (3, 3)),
            ('SPAN', (0, 4), (-1, 4)),
            ('BACKGROUND', (0, 4), (-1, 4), sombreado),
        ]
    )

    table = Table(table)
    table.setStyle(estilo)
    story.append(table)

    propiedades = intercambiador.intercambiador()
    condicion_carcasa = propiedades.condicion_carcasa()
    condicion_tubo = propiedades.condicion_tubo()

    # Segunda Tabla: Condiciones de Diseño
    table = [
        [
            '',
            '',
            Paragraph("Lado Carcasa", centrar_parrafo),
            '',
            Paragraph(f"Lado Tubo", centrar_parrafo),
            ''
        ],
        [
            '', '',
            Paragraph(f"IN", centrar_parrafo),Paragraph(f"OUT", centrar_parrafo),
            Paragraph(f"IN", centrar_parrafo),Paragraph(f"OUT", centrar_parrafo)
        ],
        [
            'Fluido', '',
            Paragraph(f"{propiedades.fluido_carcasa if propiedades.fluido_carcasa else condicion_carcasa.fluido_etiqueta}", centrar_parrafo), '',
            Paragraph(f"{propiedades.fluido_tubo if propiedades.fluido_tubo else condicion_tubo.fluido_etiqueta}", centrar_parrafo),
        ],
        [
            f'Temperatura ({condicion_carcasa.temperaturas_unidad})', '',
            Paragraph(f"{condicion_carcasa.temp_entrada}", centrar_parrafo),Paragraph(f"{condicion_carcasa.temp_salida}", centrar_parrafo),
            Paragraph(f"{condicion_tubo.temp_entrada}", centrar_parrafo),Paragraph(f"{condicion_tubo.temp_salida}", centrar_parrafo),
        ],
        [
            f'Flujo Vapor ({condicion_carcasa.flujos_unidad})', '',
            Paragraph(f"{condicion_carcasa.flujo_vapor_entrada}", centrar_parrafo),Paragraph(f"{condicion_carcasa.flujo_vapor_salida}", centrar_parrafo),
            Paragraph(f"{condicion_tubo.flujo_vapor_entrada}", centrar_parrafo),Paragraph(f"{condicion_tubo.flujo_vapor_salida}", centrar_parrafo),
        ],
        [
            f'Flujo Líquido ({condicion_carcasa.flujos_unidad})', '',
            Paragraph(f"{condicion_carcasa.flujo_liquido_entrada}", centrar_parrafo),Paragraph(f"{condicion_carcasa.flujo_liquido_salida}", centrar_parrafo),
            Paragraph(f"{condicion_tubo.flujo_liquido_entrada}", centrar_parrafo),Paragraph(f"{condicion_tubo.flujo_liquido_salida}", centrar_parrafo),
        ],
        [
            f'Flujo Másico Total ({condicion_carcasa.flujos_unidad})', '',
            Paragraph(f"{condicion_carcasa.flujo_masico}", centrar_parrafo), '',
            Paragraph(f"{condicion_tubo.flujo_masico}", centrar_parrafo), ''
        ],
        [
            f'Cap. Calorífica Vap. ({condicion_carcasa.unidad_cp})', '',
            Paragraph(f"{condicion_carcasa.fluido_cp_liquido if condicion_carcasa.fluido_cp_liquido else ''}", centrar_parrafo), '',
            Paragraph(f"{condicion_tubo.fluido_cp_liquido if condicion_tubo.fluido_cp_liquido else ''}", centrar_parrafo), '',
        ],
        [
            f'Cap. Calorífica Líq. ({condicion_carcasa.unidad_cp})', '',
            Paragraph(f"{condicion_carcasa.fluido_cp_gas if condicion_carcasa.fluido_cp_gas else ''}", centrar_parrafo), '',
            Paragraph(f"{condicion_tubo.fluido_cp_gas if condicion_tubo.fluido_cp_gas else ''}", centrar_parrafo), '',
        ],
        [
            f'Temp. Saturación ({condicion_carcasa.temperaturas_unidad})', '',
            Paragraph(f"{condicion_carcasa.tsat if condicion_carcasa.tsat else ''}", centrar_parrafo), '',
            Paragraph(f"{condicion_tubo.tsat if condicion_tubo.tsat else ''}", centrar_parrafo), '',
        ],
        [
            f'Calor Latente (J/Kg)', '',
            Paragraph(f"{condicion_carcasa.hvap if condicion_carcasa.hvap else ''}", centrar_parrafo), '',
            Paragraph(f"{condicion_tubo.hvap if condicion_tubo.hvap else ''}", centrar_parrafo), '',
        ],
        [
            f'Cambio de Fase', '',
            Paragraph(f"{condicion_carcasa.cambio_fase_largo()}", centrar_parrafo), '',
            Paragraph(f"{condicion_tubo.cambio_fase_largo()}", centrar_parrafo), '',
        ],
        [
            f'Presión Entrada ({condicion_carcasa.unidad_presion})', '',
            Paragraph(f"{condicion_carcasa.presion_entrada}", centrar_parrafo), '',
            Paragraph(f"{condicion_tubo.presion_entrada}", centrar_parrafo), '',
        ],
        [
            f'Caída Presión Permitida ({condicion_carcasa.unidad_presion})', '',
            Paragraph(f"{condicion_carcasa.caida_presion_max}", centrar_parrafo), '',
            Paragraph(f"{condicion_tubo.caida_presion_max}", centrar_parrafo), '',
        ],
        [
            f'Caída Presión Mínima ({condicion_carcasa.unidad_presion})', '',
            Paragraph(f"{condicion_carcasa.caida_presion_min}", centrar_parrafo), '',
            Paragraph(f"{condicion_tubo.caida_presion_min}", centrar_parrafo), '',
        ],
        [
            f'Fouling ({propiedades.ensuciamiento_unidad})', '',
            Paragraph(f"{condicion_carcasa.fouling}", centrar_parrafo), '',
            Paragraph(f"{condicion_tubo.fouling}", centrar_parrafo), '',
        ],
        [
            f'Conexiones de Entrada', '',
            Paragraph(f"{propiedades.conexiones_salida_carcasa}", centrar_parrafo), '',
            Paragraph(f"{propiedades.conexiones_salida_tubos}", centrar_parrafo), '',
        ],
        [
            f'Conexiones de Salida', '',
            Paragraph(f"{propiedades.conexiones_entrada_carcasa}", centrar_parrafo), '',
            Paragraph(f"{propiedades.conexiones_entrada_tubos}", centrar_parrafo), '',
        ],
        [
            f'Pasos', '',
            Paragraph(f"{propiedades.numero_pasos_carcasa}", centrar_parrafo), '',
            Paragraph(f"{propiedades.numero_pasos_tubo}", centrar_parrafo), '',
        ],
        [
            Paragraph("Parámetros de Diseño", centrar_parrafo), '','','','',''
        ],
    ]

    estilo = TableStyle(
        [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

            ('SPAN', (0, 0), (1, 1)),
            ('SPAN', (2, 0), (3, 0)),
            ('SPAN', (4, 0), (5, 0)),

            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('SPAN', (0, 4), (1, 4)),
            ('SPAN', (0, 5), (1, 5)),
            ('SPAN', (0, 6), (1, 6)),
            ('SPAN', (0, 7), (1, 7)),
            ('SPAN', (0, 8), (1, 8)),
            ('SPAN', (0, 9), (1, 9)),
            ('SPAN', (0, 10), (1, 10)),
            ('SPAN', (0,11), (1, 11)),
            ('SPAN', (0,12), (1, 12)),
            ('SPAN', (0, 13), (1, 13)),
            ('SPAN', (0,14), (1,14)),
            ('SPAN', (0,15), (1,15)),
            ('SPAN', (0,16), (1,16)),
            ('SPAN', (0,17), (1,17)),
            ('SPAN', (0,18), (1,18)),

            ('SPAN', (2, 18), (3, 18)),
            ('SPAN', (4, 18), (5, 18)),

            ('SPAN', (2, 17), (3, 17)),
            ('SPAN', (4, 17), (5, 17)),

            ('SPAN', (2, 16), (3, 16)),
            ('SPAN', (4, 16), (5, 16)),

            ('SPAN', (2, 15), (3, 15)),
            ('SPAN', (4, 15), (5, 15)),

            ('SPAN', (2, 14), (3, 14)),
            ('SPAN', (4, 14), (5, 14)),

            ('SPAN', (2, 13), (3, 13)),
            ('SPAN', (4, 13), (5, 13)),

            ('SPAN', (2, 12), (3, 12)),
            ('SPAN', (4, 12), (5, 12)),

            ('SPAN', (2, 11), (3, 11)),
            ('SPAN', (4, 11), (5, 11)),

            ('SPAN', (2, 10), (3, 10)),
            ('SPAN', (4, 10), (5, 10)),

            ('SPAN', (2, 9), (3, 9)),
            ('SPAN', (4, 9), (5, 9)),

            ('SPAN', (2, 8), (3, 8)),
            ('SPAN', (4, 8), (5, 8)),

            ('SPAN', (2, 7), (3, 7)),
            ('SPAN', (4, 7), (5, 7)),

            ('SPAN', (2, 6), (3, 6)),
            ('SPAN', (4, 6), (5, 6)),

            ('SPAN', (2, 2), (3, 2)),
            ('SPAN', (4, 2), (5, 2)),
            ('SPAN', (0, 19), (-1, 19)),

            ('BACKGROUND', (2, 0), (-1, 1), sombreado),
            ('BACKGROUND', (0, 2), (1, 18), sombreado),
            ('BACKGROUND', (0, 19), (-1, 19), sombreado)

        ]
    )
    
    table = Table(table, colWidths=(1.97*inch,0.01*inch, 1.03*inch, 1.03*inch, 1.03*inch, 1.03*inch))
    table.setStyle(estilo)
    story.append(table)

    table = [
        [
            f'Calor ({propiedades.q_unidad})', Paragraph(f"{propiedades.q}", centrar_parrafo), '',
            f'U ({propiedades.u_unidad})', Paragraph(f"{propiedades.u}", centrar_parrafo), '',
        ],
        [
            f'Ensu. ({propiedades.ensuciamiento_unidad})', Paragraph(f"{propiedades.ensuciamiento}", centrar_parrafo), '',
            f'Área ({propiedades.area_unidad})', Paragraph(f"{propiedades.area}", centrar_parrafo), '',
        ],
        [
            f'Arr. Serie', Paragraph(f"{propiedades.arreglo_serie}", centrar_parrafo), '',
            f'Arr. Paralelo', Paragraph(f"{propiedades.arreglo_paralelo}", centrar_parrafo), '',
        ],
        [
            f'Arr. Serie', Paragraph(f"{propiedades.arreglo_serie}", centrar_parrafo), '',
            f'Arr. Paralelo', Paragraph(f"{propiedades.arreglo_paralelo}", centrar_parrafo), '',
        ],
        [
            f'No. Tubos', Paragraph(f"{propiedades.numero_tubos}", centrar_parrafo), '',
            f'Longitud ({propiedades.longitud_tubos_unidad})', Paragraph(f"{propiedades.longitud_tubos}", centrar_parrafo), '',
        ],
        [
            f'OD Tubos ({propiedades.diametro_tubos_unidad})', Paragraph(f"{propiedades.diametro_externo_tubos}", centrar_parrafo), '',
            f'ID Carcasa ({propiedades.diametro_tubos_unidad})', Paragraph(f"{propiedades.diametro_interno_carcasa}", centrar_parrafo), '',
        ],
        [
            f'Pitch ({propiedades.unidades_pitch})', Paragraph(f"{propiedades.pitch_tubos}", centrar_parrafo), '',
            f'Tipo del Tubo', Paragraph(f"{propiedades.tipo_tubo}", centrar_parrafo), '',
        ],
        [
            f'Material Carcasa', Paragraph(f"{propiedades.material_carcasa}", centrar_parrafo), '',
            f'Material Tubo', Paragraph(f"{propiedades.material_tubo}", centrar_parrafo), '',
        ],
        [
            f'Criticidad', Paragraph(f"{propiedades.criticidad_larga()}", centrar_parrafo), '',
        ],
    ]

    estilo = TableStyle(
        [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('SPAN', (1,0), (2,0)), ('SPAN', (4,0), (5,0)),
            ('SPAN', (1,1), (2,1)), ('SPAN', (4,1), (5,1)),
            ('SPAN', (1,2), (2,2)), ('SPAN', (4,2), (5,2)),
            ('SPAN', (1,3), (2,3)), ('SPAN', (4,3), (5,3)),
            ('SPAN', (1,4), (2,4)), ('SPAN', (4,4), (5,4)),
            ('SPAN', (1,5), (2,5)), ('SPAN', (4,5), (5,5)),
            ('SPAN', (1,6), (2,6)), ('SPAN', (4,6), (5,6)),
            ('SPAN', (1,7), (2,7)), ('SPAN', (4,7), (5,7)),
            ('SPAN', (1,8), (-1,8)),

            ('BACKGROUND', (0,0), (0,-1), sombreado),
            ('BACKGROUND', (3,0), (3,-2), sombreado)
        ],

    )

    table = Table(table, colWidths=(1.3*inch,0.85*inch,0.9*inch,1.3*inch,0.9*inch,0.85*inch))
    table.setStyle(estilo)
    story.append(table)

    return story