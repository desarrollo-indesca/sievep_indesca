from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Prefetch
from simulaciones_pequiven.views import FiltradoSimpleMixin
from .models import *
from reportes.pdfs import generar_pdf
from reportes.xlsx import reporte_equipos

class CargarCompresorMixin():
    """
    Resumen:
        Mixin para optimizar las consultas de compresores.
    """

    def get_compresor(self, prefetch = True, queryset = True):
        if(not queryset):
            if(self.kwargs.get('pk')):
                compresor = Compresor.objects.filter(pk = self.kwargs['pk'])
            else:
                compresor = Compresor.objects.none()
        else:
            compresor = queryset

        if(prefetch):
            compresor = compresor.select_related(
                'creado_por', 'editado_por', 'planta'
            )
        
        if(not queryset):
            if(compresor):
                return compresor[0]

        return compresor

# Create your views here.

class ConsultaCompresores(FiltradoSimpleMixin, CargarCompresorMixin, LoginRequiredMixin, ListView):
    '''
    Resumen:
        Vista para la consulta de los compresores.
        Hereda de ListView.
        Hereda del Mixin para optimizar consultas.
        Pueden acceder usuarios que hayan iniciado sesión.
        Se puede generar una ficha del equipo a través de esta vista.

    Atributos:
        model: Model -> Modelo del cual se extraerán los elementos de la lista.
        template_name: str -> Plantilla a renderizar
        paginate_by: str -> Número de elementos a mostrar a a la vez
        titulo: str -> Título de la vista

    Métodos:
        post(self, request, *args, **kwargs) -> HttpResponse
            Se utiliza para la generación de reportes de ficha o de compresores.

        get_context_data(self, **kwargs) -> dict
            Genera el contexto necesario en la vista para la renderización de la plantilla

        get_queryset(self) -> QuerySet
            Obtiene el QuerySet de la lista de acuerdo al modelo del atributo.
            Hace el filtrado correspondiente y prefetching necesario para reducir las queries.
    '''
    model = Compresor
    template_name = 'compresores/consulta.html'
    paginate_by = 10
    titulo = "SIEVEP - Consulta de Compresores"

    def post(self, request, *args, **kwargs):
        reporte_ficha = self.reporte_ficha(request)
        if(reporte_ficha): # Si se está deseando generar un reporte de ficha, se genera
            return reporte_ficha

        if(request.POST.get('tipo') == 'pdf'): # Reporte de turbinas de vapor en PDF
            return generar_pdf(request, self.get_queryset(), 'Reporte de Listado de Compresores', 'compresores')
        
        if(request.POST.get('tipo') == 'xlsx'): # reporte de turbinas de vapor en XLSX
            return reporte_equipos(request, self.get_queryset(), 'Listado de Compresores', 'listado_compresores')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permisos"] = {
            'creacion': self.request.user.is_superuser or self.request.user.usuario_planta.filter(crear = True).exists(),
            'ediciones':list(self.request.user.usuario_planta.filter(edicion = True).values_list('planta__pk', flat=True)),
            'instalaciones':list(self.request.user.usuario_planta.filter(edicion_instalacion = True).values_list('planta__pk', flat=True)),
            'duplicaciones':list(self.request.user.usuario_planta.filter(duplicacion = True).values_list('planta__pk', flat=True)),
            'evaluaciones': list(self.request.user.usuario_planta.filter(ver_evaluaciones = True).values_list('planta__pk', flat=True)),
        }

        return context

    def get_queryset(self):        
        new_context = self.get_compresor(True, self.filtrar_equipos())

        return new_context
