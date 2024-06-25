from .models import *

from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from simulaciones_pequiven.views import FiltradoSimpleMixin
from reportes.pdfs import generar_pdf
from reportes.xlsx import reporte_equipos

# Create your views here.
class CargarCalderasMixin():
    """
    Resumen:
        Mixin para optimizar las consultas de calderas.
    """

    def get_caldera(self, prefetch = True, caldera_q = True):
        if(not caldera_q):
            if(self.kwargs.get('pk')):
                caldera = Caldera.objects.filter(pk = self.kwargs['pk'])
            else:
                caldera = Caldera.objects.none()
        else:
            caldera = caldera_q

        if(prefetch):
            caldera = caldera.select_related(
                "creado_por", "planta__complejo",
                "sobrecalentador", "sobrecalentador__temperatura_unidad",
                "sobrecalentador__presion_unidad", "sobrecalentador__flujo_unidad",
                
                "sobrecalentador__dims", "sobrecalentador__dims__area_unidad", 
                "sobrecalentador__dims__diametro_unidad",
               
                "dimensiones", "dimensiones__dimensiones_unidad",
                
                "especificaciones", "especificaciones__area_unidad",
                "especificaciones__calor_unidad", "especificaciones__capacidad_unidad",
                "especificaciones__temperatura_unidad", "especificaciones__presion_unidad",
                "especificaciones__carga_unidad",
                
                "chimenea", "chimenea__dimensiones_unidad", 
                
                "economizador", "economizador__area_unidad", "economizador__diametro_unidad",
            )
            caldera = caldera.prefetch_related(
                Prefetch("corrientes_caldera", Corriente.objects.select_related("flujo_masico_unidad",
                    "densidad_unidad", "temp_operacion_unidad", "presion_unidad")),

                Prefetch("combustible", Combustible.objects.prefetch_related(
                    Prefetch("composicion_combustible_caldera", ComposicionCombustible.objects.select_related(
                        "fluido"
                    ))
                )),

                Prefetch("caracteristicas_caldera", Caracteristica.objects.prefetch_related(
                    Prefetch("valores_por_carga", ValorPorCarga.objects.select_related("unidad"))
                )),

                Prefetch("tambor", Tambor.objects.select_related("temperatura_unidad", "presion_unidad").prefetch_related(
                    Prefetch("secciones_tambor", SeccionTambor.objects.select_related("dimensiones_unidad"))
                ))
            )
        
        if(not caldera_q):
            if(caldera):
                return caldera[0]

        return caldera

class ConsultaCalderas(FiltradoSimpleMixin, CargarCalderasMixin, LoginRequiredMixin, ListView):
    '''
    Resumen:
        Vista para la consulta de las calderas.
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
            Se utiliza para la generación de reportes de ficha o de calderas.

        get(self, request, *args, **kwargs) -> HttpResponse
            Se renderiza la página en su página y filtrado correcto.

        get_context_data(self, **kwargs) -> dict
            Genera el contexto necesario en la vista para la renderización de la plantilla

        get_queryset(self) -> QuerySet
            Obtiene el QuerySet de la lista de acuerdo al modelo del atributo.
            Hace el filtrado correspondiente y prefetching necesario para reducir las queries.
    '''
    model = Caldera
    template_name = 'calderas/consulta.html'
    paginate_by = 10
    titulo = "SIEVEP - Consulta de Calderas"

    def post(self, request, *args, **kwargs):
        reporte_ficha = self.reporte_ficha(request)
        if(reporte_ficha): # Si se está deseando generar un reporte de ficha, se genera
            return reporte_ficha

        if(request.POST.get('tipo') == 'pdf'): # Reporte de turbinas de vapor en PDF
            return generar_pdf(request, self.get_queryset(), 'Reporte de Listado de Calderas', 'calderas')
        
        if(request.POST.get('tipo') == 'xlsx'): # reporte de turbinas de vapor en XLSX
            return reporte_equipos(request, self.get_queryset(), 'Listado de Calderas', 'listado_calderas')
        
    def get_queryset(self):        
        new_context = self.get_caldera(True, self.filtrar_equipos())

        return new_context
    