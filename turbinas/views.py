from typing import Any
import datetime
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
from .forms import *

# Create your views here.
class ObtenerTurbinVaporMixin():
    def get_turbina(self):
        turbina = TurbinaVapor.objects.filter(pk=self.kwargs['pk']).select_related(
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

        turbina = turbina.prefetch_related(
           'datos_corrientes__corrientes'
        )

        return turbina.first()

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
            Se utiliza para la generación de reportes de ficha o de turbinas de vapor.

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

        if(request.POST.get('tipo') == 'pdf'): # Reporte de turbinas de vapor en PDF
            return generar_pdf(request, self.get_queryset(), 'Reporte de Turbinas de Vapor', 'turbinas_vapor')
        
        if(request.POST.get('tipo') == 'xlsx'): # reporte de turbinas de vapor en XLSX
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

        context['link_creacion'] = 'creacion_turbina_vapor'

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
    
class CreacionTurbinaVapor(SuperUserRequiredMixin, View):
    """
    Resumen:
        Vista para la creación o registro de nuevas turbinas de vapor.
        Solo puede ser accedido por superusuarios.

    Atributos:
        success_message: str -> Mensaje a ser enviado al usuario al registrar exitosamente una turbina.
        titulo: str -> Título de la vista
    
    Métodos:
        get_context(self) -> dict
            Crea instancias de los formularios a ser utilizados y define el título de la vista.

        get(self, request, **kwargs) -> HttpResponse
            Renderiza el formulario con la plantilla correspondiente.

        almacenar_datos(self) -> HttpResponse
            Valida y almacena los datos de acuerdo a la lógica requerida para el almacenamiento de bombas por medio de los formularios.
            Si hay errores se levantará una Exception.

        post(self) -> HttpResponse
            Envía el request a los formularios y envía la respuesta al cliente.
    """

    success_message = "La nueva turbina de vapor ha sido registrada exitosamente."
    titulo = 'SIEVEP - Creación de Turbina de Vapor'
    template_name = 'turbinas_vapor/creacion.html'

    def get_context(self):
        return {
            'form_turbina': TurbinaVaporForm(), 
            'form_especificaciones': EspecificacionesTurbinaVaporForm(), 
            'form_generador': GeneradorElectricoForm(), 
            'form_datos_corrientes': DatosCorrientesForm(),
            'forms_corrientes': corrientes_formset(queryset=Corriente.objects.none()),
            'titulo': self.titulo
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context())
    
    def almacenar_datos(self, form_turbina, form_especificaciones, form_generador,
                            form_datos_corrientes, forms_corrientes):
        
        valid = True # Inicialmente se considera válido
        
        with transaction.atomic():
            valid = valid and form_especificaciones.is_valid() # Se valida el primer formulario

            if(valid):
                form_especificaciones.save()
            else:
                print(form_especificaciones.errors)
            
            valid = valid and form_generador.is_valid()

            if(valid):
                form_generador.save()
            else:
                print(form_generador.errors)

            valid = valid and form_datos_corrientes.is_valid()

            if(valid):
                form_datos_corrientes.save()
            else:
                print(form_datos_corrientes.errors)

            valid = valid and forms_corrientes.is_valid()

            if(valid):
                for form in forms_corrientes:
                    valid = valid and form.is_valid()
                    
                    if(valid):
                        form.instance.datos_corriente = form_datos_corrientes.instance
                        form.save()
                    else:
                        print(form.errors)
            else:
                print(form_datos_corrientes.errors)

            valid = valid and form_turbina.is_valid()

            if(valid):
                
                form_turbina.instance.generador_electrico = form_generador.instance
                form_turbina.instance.especificaciones = form_especificaciones.instance
                form_turbina.instance.datos_corrientes = form_datos_corrientes.instance

                if(form_turbina.instance.pk):
                    form_turbina.instance.editado_por = self.request.user
                    form_turbina.instance.editado_al = datetime.datetime.now()
                else:
                    form_turbina.instance.creado_por = self.request.user

                form_turbina.save()
            else:
                print(form_turbina.errors)
                
            if(valid): # Si todos los formularios son válidos, se almacena la turbina

                messages.success(self.request, self.success_message)
                return redirect(f'/turbinas/vapor/')
    
    def post(self, request):
        form_turbina = TurbinaVaporForm(request.POST)
        form_especificaciones = EspecificacionesTurbinaVaporForm(request.POST)
        form_generador = GeneradorElectricoForm(request.POST)
        form_datos_corrientes = DatosCorrientesForm(request.POST)
        forms_corrientes = corrientes_formset(request.POST)

        try:
            return self.almacenar_datos(form_turbina, form_especificaciones, form_generador,
                                        form_datos_corrientes, forms_corrientes)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name, context={
                'form_turbina': TurbinaVaporForm(request.POST), 
                'form_especificaciones': EspecificacionesTurbinaVaporForm(request.POST), 
                'form_generador': GeneradorElectricoForm(request.POST), 
                'form_datos_corrientes': DatosCorrientesForm(request.POST),
                'forms_corrientes': corrientes_formset(request.POST),
            })

class EdicionTurbinaVapor(CreacionTurbinaVapor, ObtenerTurbinVaporMixin):
    titulo = "Edición de Turbina de Vapor"
    success_message = "La turbina ha sido editada exitosamente."

    def get_context(self):
        turbina = self.get_turbina()
        return {
            'form_turbina': TurbinaVaporForm(instance=turbina), 
            'form_especificaciones': EspecificacionesTurbinaVaporForm(instance=turbina.especificaciones), 
            'form_generador': GeneradorElectricoForm(instance=turbina.generador_electrico), 
            'form_datos_corrientes': DatosCorrientesForm(instance=turbina.datos_corrientes),
            'forms_corrientes': corrientes_formset(queryset=turbina.datos_corrientes.corrientes.all()),
            'titulo': self.titulo
        }

    def post(self, request, pk):
        turbina = self.get_turbina()

        form_turbina = TurbinaVaporForm(request.POST, instance=turbina)
        form_especificaciones = EspecificacionesTurbinaVaporForm(request.POST, instance=turbina.especificaciones)
        form_generador = GeneradorElectricoForm(request.POST, instance=turbina.generador_electrico)
        form_datos_corrientes = DatosCorrientesForm(request.POST, instance=turbina.datos_corrientes)
        forms_corrientes = corrientes_formset(request.POST, queryset=turbina.datos_corrientes.corrientes.all())

        try:
            return self.almacenar_datos(form_turbina, form_especificaciones, form_generador,
                                        form_datos_corrientes, forms_corrientes)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name, context={
                'form_turbina': form_turbina, 
                'form_especificaciones': form_especificaciones, 
                'form_generador': form_generador, 
                'form_datos_corrientes': form_datos_corrientes,
                'forms_corrientes': forms_corrientes
            })

class ConsultaEvaluacionTurbinaVapor(ConsultaEvaluacion, ObtenerTurbinVaporMixin, ReportesFichasTurbinasMixin):
    """
    Resumen:
        Vista para la consulta de evaluaciones de Consulta de Evaluaciones de una Turbina de Vapor.
        Hereda de ConsultaEvaluacion para el ahorro de trabajo en términos de consulta.
        Utiliza los Mixin para obtener ventiladores y de generación de reportes de fichas de ventiladores.

    Atributos:
        model: EvaluacionBomba -> Modelo de la vista
        model_equipment -> Modelo del equipo
        clase_equipo -> Complemento del título de la vista
        tipo -> Tipo de equipo. Necesario para la renderización correcta de nombres y links.
    
    Métodos:
        get_context_data(self) -> dict
            Añade al contexto original el equipo.

        get_queryset(self) -> QuerySet
            Hace el prefetching correspondiente al queryset de las evaluaciones.

        post(self) -> HttpResponse
            Contiene la lógica de eliminación (ocultación) de una evaluación y de generación de reportes.
    """
    model = Evaluacion
    model_equipment = TurbinaVapor
    clase_equipo = " la Turbina de Vapor"
    tipo = 'turbina_vapor'

    def post(self, request, **kwargs):
        reporte_ficha = self.reporte_ficha(request)
        if(reporte_ficha):
            return reporte_ficha
            
        if(request.user.is_superuser and request.POST.get('evaluacion')): # Lógica de "Eliminación"
            evaluacion = self.model.objects.get(pk=request.POST['evaluacion'])
            evaluacion.activo = False
            evaluacion.save()
            messages.success(request, "Evaluación eliminada exitosamente.")
        elif(request.POST.get('evaluacion') and not request.user.is_superuser):
            messages.warning(request, "Usted no tiene permiso para eliminar evaluaciones.")

        if(request.POST.get('tipo') == 'pdf'):
            return generar_pdf(request, self.get_queryset(), f"Evaluaciones de la Turbina de Vapor {self.get_turbina().tag}", "reporte_evaluaciones_turbina_vapor")
        elif(request.POST.get('tipo') == 'xlsx'):
            return historico_evaluaciones_turbinas(self.get_queryset(), request)

        if(request.POST.get('detalle')):
            return generar_pdf(request, self.model.objects.get(pk=request.POST.get('detalle')), "Detalle de Evaluación de Turbina de Vapor", "detalle_evaluacion_turbina_vapor")

        return self.get(request, **kwargs)
    
    def get_queryset(self):
        new_context = super().get_queryset()

        new_context = new_context.select_related(
            'creado_por', 'entrada', 'salida',
            'entrada__flujo_entrada_unidad', 'entrada__potencia_real_unidad',
            'entrada__presion_unidad', 'entrada__temperatura_unidad',
        )

        new_context = new_context.prefetch_related(
            "entrada__entradas_corrientes", "salida__salidas_corrientes"
        )

        return new_context

    def get_context_data(self, **kwargs: Any) -> "dict[str, Any]":
        context = super().get_context_data(**kwargs)
        context['equipo'] = self.get_turbina()
        context['tipo'] = self.tipo

        return context
