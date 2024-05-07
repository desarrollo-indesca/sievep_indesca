from typing import Any
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from simulaciones_pequiven.views import ConsultaEvaluacion, ReportesFichasMixin, FiltrarEvaluacionesMixin

from usuarios.views import SuperUserRequiredMixin
from calculos.unidades import *
from reportes.pdfs import generar_pdf
from reportes.xlsx import reporte_equipos
from .models import *

# Create your views here.
class ReportesFichasTurbinasMixin(ReportesFichasMixin):
    model_ficha = TurbinaVapor
    reporte_ficha_xlsx = None
    titulo_reporte_ficha = "Ficha Técnica de la Turbina"
    codigo_reporte_ficha = "ficha_tecnica_turbina_vapor"

class ConsultaTurbinasVapor(LoginRequiredMixin, ListView, ReportesFichasTurbinasMixin):
    '''
    Resumen:
        Vista para la consulta de las turbinas de vapor.
        Hereda de ListView.
        Pueden acceder usuarios que hayan iniciado sesión.
        Se puede generar una ficha del equipo a través de esta vista.

    Atributos:
        model: Model -> Modelo del cual se extraerán los elementos de la lista.
        template_name: str -> Plantilla a renderizar
        paginate_by: str -> Número de elementos a mostrar a a la vez

    Métodos:
        post(self, request, *args, **kwargs) -> HttpResponse
            Se utiliza para la generación de reportes de ficha o de ventiladores.

        get(self, request, *args, **kwargs) -> HttpResponse
            Se renderiza la página en su página y filtrado correcto.

        get_context_data(self, **kwargs) -> dict
            Genera el contexto necesario en la vista para la renderización de la plantilla

        get_queryset(self) -> QuerySet
            Obtiene el QuerySet de la lista de acuerdo al modelo del atributo.
            Hace el filtrado correspondiente y prefetching necesario para reducir las queries.
    '''
    model = TurbinaVapor
    template_name = 'turbinas_vapor/consulta.html'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        reporte_ficha = self.reporte_ficha(request)
        if(reporte_ficha): # Si se está deseando generar un reporte de ficha, se genera
            return reporte_ficha

        if(request.POST.get('tipo') == 'pdf'): # Reporte de ventiladores en PDF
            return generar_pdf(request, self.get_queryset(), 'Reporte de Turbinas de Vapor', 'turbinas_vapor')
        
        if(request.POST.get('tipo') == 'xlsx'): # reporte de ventiladores en XLSX
            return reporte_equipos(request, self.get_queryset(), 'Listado de Turbinas de Vapor', 'listado_ventiladores')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:        
        if(request.GET.get('page')):
            request.session['pagina_consulta'] = request.GET['page']
        else:
            request.session['pagina_consulta'] = 1
        
        request.session['tag_consulta'] = request.GET.get('tag') if request.GET.get('tag') else ''
        request.session['descripcion_consulta'] = request.GET.get('descripcion') if request.GET.get('descripcion') else ''
        request.session['complejo_consulta'] = request.GET.get('complejo') if request.GET.get('complejo') else ''
        request.session['planta_consulta'] = request.GET.get('planta') if request.GET.get('planta') else ''
        
        return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "SIEVEP - Consulta de Turbinas de Vapor"
        context['complejos'] = Complejo.objects.all()

        if(self.request.GET.get('complejo')):
            context['plantas'] = Planta.objects.filter(complejo= self.request.GET.get('complejo'))

        context['tag'] = self.request.GET.get('tag', '')
        context['descripcion'] = self.request.GET.get('descripcion', '')
        context['complejox'] = self.request.GET.get('complejo')
        context['plantax'] = self.request.GET.get('planta')

        if(context['complejox']):
            context['complejox'] = int(context['complejox'])
        
        if(context['plantax']):
            context['plantax'] = int(context['plantax'])

        context['link_creacion'] = 'creacion_ventilador'

        return context
    
    def get_queryset(self):
        tag = self.request.GET.get('tag', '')
        descripcion = self.request.GET.get('descripcion', '')
        complejo = self.request.GET.get('complejo', '')
        planta = self.request.GET.get('planta', '')

        new_context = None

        if(planta != '' and complejo != ''):
            new_context = self.model.objects.filter(
                planta__pk=planta
            )
        elif(complejo != ''):
            new_context = new_context.filter(
                planta__complejo__pk=complejo
            ) if new_context else self.model.objects.filter(
                planta__complejo__pk=complejo
            )

        if(not(new_context is None)):
            new_context = new_context.filter(
                descripcion__icontains = descripcion,
                tag__icontains = tag
            )
        else:
            new_context = self.model.objects.filter(
                descripcion__icontains = descripcion,
                tag__icontains = tag
            )

        new_context = new_context.select_related(
            'generador_electrico', 
            'generador_electrico__ciclos_unidad',
            'generador_electrico__potencia_real_unidad',
            'generador_electrico__potencia_aparente_unidad',
            'generador_electrico__velocidad_unidad',
            'generador_electrico__corriente_electrica_unidad',
            'generador_electrico__voltaje_unidad',
            
            'planta', 'planta__complejo',
            
            'especificaciones', 
            'especificaciones__potencia_unidad',
            'especificaciones__velocidad_unidad',
            'especificaciones__presion_entrada_unidad',
            'especificaciones__temperatura_entrada_unidad',
            'especificaciones__contra_presion_unidad',
            
            'datos_corrientes',
            'datos_corrientes__flujo_unidad',            
            'datos_corrientes__entalpia_unidad',            
            'datos_corrientes__presion_unidad',
            'datos_corrientes__temperatura_unidad' 
        )

        new_context = new_context.prefetch_related(
           'datos_corrientes__corrientes'
        )

        return new_context
