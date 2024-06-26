from .models import *

from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.forms import modelformset_factory

from simulaciones_pequiven.views import FiltradoSimpleMixin
from usuarios.views import SuperUserRequiredMixin 
from reportes.pdfs import generar_pdf
from reportes.xlsx import reporte_equipos
from .forms import *
from .constants import COMPUESTOS_AIRE

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
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["link_creacion"] = "creacion_caldera"

        return context

    def get_queryset(self):        
        new_context = self.get_caldera(True, self.filtrar_equipos())

        return new_context

class CreacionCaldera(SuperUserRequiredMixin, View):
    """
    Resumen:
        Vista para el registro de nuevas calderas en el sistema.
        Solo puede ser accedido por superusuarios.

    Atributos:
        success_message: str -> Mensaje al realizarse correctamente la creación
        titulo: str -> Título a mostrar en la vista
        template_name: str -> Dirección de la plantilla
    
    Métodos:
        get_context(self) -> dict
            Crea instancias de los formularios a ser utilizados y define el título de la vista.

        get(self, request, **kwargs) -> HttpResponse
            Renderiza el formulario con la plantilla correspondiente.

        almacenar_datos(self) -> HttpResponse
            Valida y almacena los datos de acuerdo a la lógica requerida para el almacenamiento de calderas por medio de los formularios.
            Si hay errores se levantará una Exception.

        post(self) -> HttpResponse
            Envía el request a los formularios y envía la respuesta al cliente.
    """

    success_message = "La nueva bomba ha sido registrada exitosamente. Los datos de instalación ya pueden ser cargados."
    titulo = 'SIEVEP - Creación de Bomba Centrífuga'
    template_name = 'calderas/creacion.html'

    def get_context(self):
        combustibles = ComposicionCombustible.objects.values('fluido').distinct()
        print(len(combustibles))

        combustible_forms = []

        for i,x in enumerate(combustibles):
            form = ComposicionCombustibleForm(prefix=f'combustible-{i}', initial={'fluido': x['fluido']})
            combustible_forms.append({
                'combustible': Fluido.objects.get(pk=x['fluido']),
                'form': form
            })
            
        return {
            'form_caldera': CalderaForm(prefix="caldera"), 
            'form_tambor': TamborForm(prefix="tambor"), 
            'form_chimenea': ChimeneaForm(prefix="chimenea"),
            'form_economizador': EconomizadorForm(prefix="economizador"),
            'form_tambor_superior': SeccionTamborForm(prefix="tambor-superior"), 
            'form_tambor_inferior': SeccionTamborForm(prefix="tambor-inferior"), 
            'form_sobrecalentador': SobrecalentadorForm(prefix="sobrecalentador"),
            'form_dimensiones_sobrecalentador': DimsSobrecalentadorForm(prefix="dimensiones-sobrecalentador"),
            'form_especificaciones': EspecificacionesCalderaForm(prefix="especificaciones-caldera"),
            'form_dimensiones_caldera': DimensionesCalderaForm(prefix="dimensiones-caldera"),
            'form_combustible': CombustibleForm(prefix="combustible"),
            'composicion_combustible_forms': combustible_forms,
            'compuestos_aire': COMPUESTOS_AIRE,
            'titulo': self.titulo
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context())
    
    def almacenar_datos(self):
        pass
    
    def post(self, request):
        # FORMS
        pass

        try:
            return self.almacenar_datos()
        except Exception as e:
            print(str(e))
            return render()