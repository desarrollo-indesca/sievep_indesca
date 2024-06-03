from typing import Any
import logging
import datetime
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib import messages
from simulaciones_pequiven.views import FiltradoSimpleMixin, ConsultaEvaluacion, ReportesFichasMixin, FiltrarEvaluacionesMixin

from usuarios.views import SuperUserRequiredMixin
from calculos.unidades import *
from .evaluacion import evaluar_turbina
from reportes.pdfs import generar_pdf
from reportes.xlsx import reporte_equipos, historico_evaluaciones_turbinas_vapor, ficha_tecnica_turbina_vapor
from .models import *
from .forms import *

logger = logging.getLogger('django')

# Create your views here.
class ObtenerTurbinaVaporMixin():
    '''
    Resumen:
        Mixin para ejecutar la consulta de turbinas completa.
    '''
    def get_turbina(self, turbina_q = None):
        if(not turbina_q):
            if(self.kwargs.get('pk')):
                turbina = TurbinaVapor.objects.filter(pk=self.kwargs['pk'])
            else:
                turbina = TurbinaVapor.objects.none()
        else:
            turbina = turbina_q

        turbina = turbina.select_related(
            'generador_electrico', 
            'generador_electrico__ciclos_unidad',
            'generador_electrico__potencia_real_unidad',
            'generador_electrico__potencia_aparente_unidad',
            'generador_electrico__velocidad_unidad',
            'generador_electrico__corriente_electrica_unidad',
            'generador_electrico__voltaje_unidad',
            
            'planta', 'planta__complejo',
            'creado_por', 'editado_por',
            
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

        if(turbina.count()):
            return turbina[0] if not turbina_q else turbina
        else:
            return turbina

class ReportesFichasTurbinasVaporMixin(ReportesFichasMixin):
    '''
    Resumen:
        Mixin para que los reportes de ficha técnica estén disponibles en todas las vistas donde esté disponible para así evitar repetir código.
    '''
    model_ficha = TurbinaVapor
    reporte_ficha_xlsx = ficha_tecnica_turbina_vapor
    titulo_reporte_ficha = "Ficha Técnica de la Turbina de Vapor"
    codigo_reporte_ficha = "ficha_tecnica_turbina_vapor"

class ConsultaTurbinasVapor(FiltradoSimpleMixin, ObtenerTurbinaVaporMixin, LoginRequiredMixin, ListView, ReportesFichasTurbinasVaporMixin):
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
        titulo: str -> Título de la vista

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
    titulo = "SIEVEP - Consulta de Turbinas de Vapor"

    def post(self, request, *args, **kwargs):
        reporte_ficha = self.reporte_ficha(request)
        if(reporte_ficha): # Si se está deseando generar un reporte de ficha, se genera
            return reporte_ficha

        if(request.POST.get('tipo') == 'pdf'): # Reporte de turbinas de vapor en PDF
            return generar_pdf(request, self.get_queryset(), 'Reporte de Turbinas de Vapor', 'turbinas_vapor')
        
        if(request.POST.get('tipo') == 'xlsx'): # reporte de turbinas de vapor en XLSX
            return reporte_equipos(request, self.get_queryset(), 'Listado de Turbinas de Vapor', 'listado_turbinas_vapor')
    
    def get_queryset(self):
        new_context = self.get_turbina(self.filtrar_equipos())

        return new_context
    
class CreacionTurbinaVapor(SuperUserRequiredMixin, View):
    """
    Resumen:
        Vista para la creación o registro de nuevas turbinas de vapor.
        Solo puede ser accedido por superusuarios.

    Atributos:
        success_message: str -> Mensaje a ser enviado al usuario al registrar exitosamente una turbina.
        titulo: str -> Título de la vista.
        template_name: str -> Plantilla a renderizar.
    
    Métodos:
        get_context(self) -> dict
            Crea instancias de los formularios a ser utilizados y define el título de la vista.

        get(self, request, **kwargs) -> HttpResponse
            Renderiza el formulario con la plantilla y contexto correspondiente.

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
            
            valid = valid and form_generador.is_valid() # Segundo formulario

            if(valid):
                form_generador.save()
            else:
                print(form_generador.errors)

            valid = valid and form_datos_corrientes.is_valid() # Tercer formulario

            if(valid):
                form_datos_corrientes.instance.id = None
                form_datos_corrientes.save()
            else:
                print(form_datos_corrientes.errors)

            valid = valid and forms_corrientes.is_valid() # Formset de corrientes

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

            valid = valid and form_turbina.is_valid() # Form de turbinas

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

                flujo_unidad = form_datos_corrientes.instance.flujo_unidad.pk
                flujo_entrada = transformar_unidades_flujo([form_datos_corrientes.instance.corrientes.first().flujo], flujo_unidad)[0]
                potencia_real = transformar_unidades_potencia([form_generador.instance.potencia_real], form_generador.instance.potencia_real_unidad.pk)[0]
                corrientes = form_datos_corrientes.instance.corrientes.all().values('presion','temperatura','flujo','entrada')

                presiones_corrientes = transformar_unidades_presion([x['presion'] for x in corrientes], form_datos_corrientes.instance.presion_unidad.pk)
                temperaturas_corrientes = transformar_unidades_temperatura([x['temperatura'] for x in corrientes], form_datos_corrientes.instance.temperatura_unidad.pk)
                
                flujos_corrientes = transformar_unidades_flujo([x['flujo'] for x in corrientes], flujo_unidad)

                for i in range(len(corrientes)):
                    corrientes[i]['presion'] = presiones_corrientes[i]
                    corrientes[i]['temperatura'] = temperaturas_corrientes[i]
                    corrientes[i]['flujo'] = flujos_corrientes[i]                    

                res = evaluar_turbina(flujo_entrada, potencia_real, corrientes, corrientes)

                form_especificaciones.instance.eficiencia = res['eficiencia']
                form_especificaciones.save()
                
            else:
                print(form_turbina.errors)
                
            if(valid): # Si todos los formularios son válidos, se almacena la turbina

                messages.success(self.request, self.success_message)
                return redirect(f'/turbinas/vapor/')
            else:
                raise Exception("Ocurrió un error de validación.")
    
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
                'form_turbina': form_turbina, 
                'form_especificaciones': form_especificaciones,
                'form_generador': form_generador, 
                'form_datos_corrientes': form_datos_corrientes,
                'forms_corrientes': forms_corrientes,
                'error': "Ocurrió un error desconocido al momento de almacenar la turbina de vapor. Revise los datos e intente de nuevo."
            })

class EdicionTurbinaVapor(CreacionTurbinaVapor, ObtenerTurbinaVaporMixin):
    """
    Resumen:
        Vista para la edición de turbinas de vapor.
        Solo puede ser accedido por superusuarios.

    Atributos:
        success_message: str -> Mensaje a ser enviado al usuario al editar exitosamente una turbina.
        titulo: str -> Título de la vista.
    
    Métodos:
        get_context(self) -> dict
            Crea instancias de los formularios a ser utilizados y define el título de la vista.

        post(self) -> HttpResponse
            Envía el request a los formularios y envía la respuesta al cliente.
    """
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
        form_datos_corrientes = DatosCorrientesForm(request.POST)
        forms_corrientes = corrientes_formset(request.POST)

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
                'forms_corrientes': forms_corrientes,
                'titulo': self.titulo,
                'error': "Ocurrió un error desconocido al momento de almacenar la turbina de vapor. Revise los datos e intente de nuevo."
            })
        
class ConsultaEvaluacionTurbinaVapor(ConsultaEvaluacion, ObtenerTurbinaVaporMixin, ReportesFichasTurbinasVaporMixin):
    """
    Resumen:
        Vista para la Consulta de Evaluaciones de una Turbina de Vapor.
        Hereda de ConsultaEvaluacion para el ahorro de trabajo en repetición de código.
        Utiliza los Mixin para obtener turbinas y de generación de reportes de fichas de turbinas.

    Atributos:
        model: EvaluacionBomba -> Modelo de la vista
        model_equipment -> Modelo del equipo
        clase_equipo -> Complemento del título de la vista
        tipo -> Tipo de equipo. Necesario para la renderización correcta de nombres y links.
        template_name: str -> Plantilla a renderizar en la vista.
    
    Métodos:
        get_context_data(self) -> dict
            Añade al contexto original el equipo y su tipo.

        get_queryset(self) -> QuerySet
            Hace el prefetching correspondiente al queryset de las evaluaciones para optimización de consultas.

        post(self) -> HttpResponse
            Contiene la lógica de eliminación (ocultación) de una evaluación y de generación de reportes.
    """
    model = Evaluacion
    model_equipment = TurbinaVapor
    clase_equipo = " la Turbina de Vapor"
    tipo = 'turbina_vapor'
    template_name = 'turbinas_vapor/consulta_evaluaciones.html'

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
            return generar_pdf(request, self.get_queryset(), f"Evaluaciones de la Turbina de Vapor {self.get_turbina().tag}", "reporte_evaluaciones_turbinas_vapor")
        elif(request.POST.get('tipo') == 'xlsx'):
            return historico_evaluaciones_turbinas_vapor(self.get_queryset(), request)

        if(request.POST.get('detalle')):
            return generar_pdf(request, self.model.objects.get(pk=request.POST.get('detalle')), "Detalle de Evaluación de Turbina de Vapor", "detalle_evaluacion_turbina_vapor")

        return self.get(request, **kwargs)
    
    def get_queryset(self):
        new_context = super().get_queryset()

        new_context = new_context.select_related(
            'creado_por', 'entrada', 'salida',
            'entrada__flujo_entrada_unidad', 'entrada__potencia_real_unidad',
            'entrada__presion_unidad', 'entrada__temperatura_unidad',
            'salida__entalpia_unidad'
        )

        new_context = new_context.prefetch_related(
            Prefetch('corrientes_evaluacion', queryset=CorrienteEvaluacion.objects.select_related(
                'entrada', 'salida', 'corriente'
            ))
        )

        return new_context

    def get_context_data(self, **kwargs: Any) -> "dict[str, Any]":
        context = super().get_context_data(**kwargs)
        context['equipo'] = self.get_turbina()
        context['tipo'] = self.tipo

        return context

class CreacionEvaluacionTurbinaVapor(LoginRequiredMixin, View, ReportesFichasTurbinasVaporMixin, ObtenerTurbinaVaporMixin):
    """
    Resumen:
        Vista de la creación de una evaluación de una turbina de vapor.
    
    Métodos:        
        get(self, request) -> HttpResponse
            Renderiza la plantilla de la vista cuando se recibe una solicitud HTTP GET con su respectivo contexto.

        post(self, request, **kwargs) -> HttpResponse
            Genera el reporte de ficha (único disponible).

        get_context_data(self) -> dict
            Inicializa los formularios respectivos con los datos precargados correspondientes.

        def generar_formset_entrada_corrientes(self, turbina) -> dict
            Genera el formset de datos de entrada de corrientes de acuerdo a las corrientes existentes en la base de datos.
    """

    def post(self, request, **kwargs):
        reporte_ficha = self.reporte_ficha(request)
        if(reporte_ficha):
            return reporte_ficha
    
    def get_context_data(self):
        turbina = self.get_turbina()       

        context = {
            'turbina': turbina,
            'form_evaluacion': EvaluacionesForm(),
            'form_entrada_evaluacion': EntradaEvaluacionForm({
                'potencia_real': turbina.generador_electrico.potencia_real if turbina.generador_electrico.potencia_real else None,
                'potencia_real_unidad': turbina.generador_electrico.potencia_real_unidad,
                'flujo_entrada_unidad': turbina.datos_corrientes.flujo_unidad if turbina.datos_corrientes.flujo_unidad else turbina.datos_corrientes.flujo_unidad,
                'presion_unidad': turbina.datos_corrientes.presion_unidad,
                'temperatura_unidad': turbina.datos_corrientes.temperatura_unidad
            }),
            'formset_entrada_corriente': self.generar_formset_entrada_corrientes(turbina),
            'titulo': "Evaluación de Turbina de Vapor"
        }

        return context
    
    def generar_formset_entrada_corrientes(self, turbina):
        formset = forms.modelformset_factory(EntradaCorriente, fields="__all__", max_num=turbina.datos_corrientes.corrientes.count(), min_num=turbina.datos_corrientes.corrientes.count())
        lista = []
        corrientes = turbina.datos_corrientes.corrientes.all()

        for x in range(corrientes.count()):
            lista.append({
                'form': EntradaCorrienteForm(prefix=f"form-{x}"),
                'corriente': corrientes[x]
            })
        
        return {
            'formset': formset(queryset=EntradaCorriente.objects.none()),
            'form_list': lista
        } 
    
    def get(self, request, pk):
        return render(request, 'turbinas_vapor/evaluacion.html', self.get_context_data())
    
class CalcularResultadosturbinaVapor(LoginRequiredMixin, View, ObtenerTurbinaVaporMixin):
    """
    Resumen:
        Vista para el cálculo de resultados de evaluaciones de Turbinas de Vapor y su almacenamiento.
        Utiliza los Mixin para obtener ventiladores y de acceso por autenticación.
    
    Métodos:
        calcular(self, request) -> HttpResponse
            Obtiene los resultados y renderiza la plantilla de resultados.

        obtener_resultados(self) -> HttpResponse
            Contiene la lógica de obtención de data, transformación de unidades, cálculo de resultados y reconversión a unidades de salida.
        
        almacenar(self) -> QuerySet
            Contiene la lógica de almacenamiento y transformación de unidades para el almacenamiento de la evaluación y sus resultados.

        post(self) -> HttpResponse
            Contiene la lógica para redirigir a almacenar o calcular los resultados de acuerdo al request.
    """
    def calcular(self, request):
        res = self.obtener_resultados(request)
        return render(request, 'turbinas_vapor/partials/resultados.html', context={'res': res})

    def obtener_resultados(self, request):
        turbina = self.get_turbina()
        datos_corrientes = turbina.datos_corrientes
        corrientes_diseno =  datos_corrientes.corrientes.all()

        # Obtener data del request
        flujo_entrada, flujo_entrada_unidad = float(request.POST.get('flujo_entrada')), int(request.POST.get('flujo_entrada_unidad'))
        potencia_real, potencia_real_unidad = float(request.POST.get('potencia_real')), int(request.POST.get('potencia_real_unidad'))
        temperatura_unidad, presion_unidad = int(request.POST.get('temperatura_unidad')),int(request.POST.get('presion_unidad'))
        temperaturas = [float(request.POST.get(f'form-{i}-temperatura')) for i in range(datos_corrientes.corrientes.count())]
        presiones = [float(request.POST.get(f'form-{i}-presion')) for i in range(datos_corrientes.corrientes.count() - 1)]

        # Transformar unidades a internacional
        presiones = transformar_unidades_presion(presiones, presion_unidad)
        temperaturas = transformar_unidades_temperatura(temperaturas, temperatura_unidad)
        potencia_real = transformar_unidades_potencia([potencia_real], potencia_real_unidad)[0]

        flujo_entrada = transformar_unidades_flujo([flujo_entrada], flujo_entrada_unidad)[0]        

        # Calcular Resultados
        corrientes = []
        for x in range(len(temperaturas)):
            corrientes.append({
                'presion': presiones[x] if x < len(temperaturas) - 1 else None,
                'temperatura': temperaturas[x],
                'entrada': corrientes_diseno[x].entrada
            })

        res = evaluar_turbina(flujo_entrada, potencia_real, corrientes, corrientes_diseno.values())

        # Transformar unidades de internacional a salida (ficha)
        res['potencia_calculada'] = transformar_unidades_potencia([res['potencia_calculada']], 49, potencia_real_unidad)[0]

        for i in range(len(res['corrientes'])):
            res['corrientes'][i]['entalpia'] = transformar_unidades_entalpia_masica([res['corrientes'][i]['entalpia']], 60, turbina.datos_corrientes.entalpia_unidad.pk)[0]
            
            if(flujo_entrada_unidad in PK_UNIDADES_FLUJO_MASICO):
                res['corrientes'][i]['flujo'] = transformar_unidades_flujo([res['corrientes'][i]['flujo']], 10, flujo_entrada_unidad)[0]
            else:
                res['corrientes'][i]['flujo'] = transformar_unidades_flujo_volumetrico([res['corrientes'][i]['flujo']], 42, flujo_entrada_unidad)[0]

        res['potencia_unidad'] = Unidades.objects.get(pk =  potencia_real_unidad)

        return res

    def almacenar(self, request):
        try:
            res = self.obtener_resultados(request)
            valid = True
            turbina = self.get_turbina()
            corrientes_diseno = turbina.datos_corrientes.corrientes.all()

            form_evaluacion = EvaluacionesForm(request.POST)
            form_entrada = EntradaEvaluacionForm(request.POST)
            formset_corrientes = forms.modelformset_factory(EntradaCorriente, form=EntradaCorrienteForm, extra=0, max_num = turbina.datos_corrientes.corrientes.count())
            formset_corrientes = formset_corrientes(request.POST)
            entradas_corrientes = []

            with transaction.atomic():
                valid = valid and form_entrada.is_valid() # Primer form validado

                if(valid):
                    form_entrada.save()
                else:
                    print(form_entrada.errors)

                valid = valid and formset_corrientes.is_valid() # Formset de datos de entrada de corrientes

                if(valid):
                    for i,form in enumerate(formset_corrientes): # Iterar por cada uno
                        form.save() # Almacenarlo
                        entradas_corrientes.append(form.instance) # Guardar la instancia en una lista temporal
                else:
                    print(formset_corrientes.errors)

                valid = valid and form_evaluacion.is_valid() # Segundo form validado

                if(valid):
                    # Añadido de datos faltantes a la instancia de evaluación
                    form_evaluacion.instance.equipo = turbina 
                    form_evaluacion.instance.creado_por = request.user
                    form_evaluacion.instance.entrada = form_entrada.instance

                    form_evaluacion.instance.salida = SalidaEvaluacion.objects.create(
                        eficiencia = res['eficiencia'],
                        potencia_calculada = res['potencia_calculada'],
                        entalpia_unidad = turbina.datos_corrientes.entalpia_unidad
                    )                      

                    form_evaluacion.save() # Almacenamiento de la evaluación

                    salidas_corrientes = []
                    for corriente in res['corrientes']: # Almacenamiento de los datos de cada salida de cada corriente
                        salidas_corrientes.append(SalidaCorriente(
                            flujo = corriente['flujo'],
                            entalpia = corriente['entalpia'],
                            fase = corriente['fase'][0] # 0 = clave
                        ))
                    
                    salidas_corrientes = SalidaCorriente.objects.bulk_create(salidas_corrientes)
                    corrientes = []

                    for i in range(len(salidas_corrientes)): # Almacenamiento de los datos de cada corriente
                        corrientes.append(CorrienteEvaluacion(
                            corriente = corrientes_diseno[i],
                            entrada = entradas_corrientes[i],
                            salida = salidas_corrientes[i],
                            evaluacion = form_evaluacion.instance                            
                        ))

                    CorrienteEvaluacion.objects.bulk_create(corrientes)
                    
                else:
                    print(form_evaluacion.errors)
                    return render(request, 'turbinas_vapor/partials/carga_fallida.html', {'turbina': turbina})

                return render(request, 'turbinas_vapor/partials/carga_lograda.html', {'turbina': turbina})

        except Exception as e:
            print(str(e))
            return render(request, 'turbinas_vapor/partials/carga_fallida.html', {'turbina': turbina})

    def post(self, request, pk):
        if(request.POST['submit'] == 'almacenar'):
            return self.almacenar(request)
        else:
            return self.calcular(request)

class GenerarGraficaTurbina(LoginRequiredMixin, View, FiltrarEvaluacionesMixin):
    """
    Resumen:
        Vista AJAX que envía los datos necesarios para la gráfica histórica de evaluaciones de turbinas de vapor.
        Transforma a las unidades en el diseño.
    
    Métodos:
        get(self, request, pk) -> JsonResponse
            Obtiene los datos y envía el Json correspondiente de respuesta
    """

    def get(self, request, pk):
        turbina = TurbinaVapor.objects.get(pk=pk)
        evaluaciones = Evaluacion.objects.filter(activo = True, equipo = turbina).order_by('fecha')

        evaluaciones = self.filtrar(request, evaluaciones)
        potencia_unidad = turbina.generador_electrico.potencia_real_unidad.pk
        
        res = []

        for evaluacion in evaluaciones:
            salida = evaluacion.salida
            entrada = evaluacion.entrada
            res.append({
                'fecha': evaluacion.fecha.__str__(),
                'salida__eficiencia': salida.eficiencia,
                'salida__potencia_calculada': transformar_unidades_potencia([salida.potencia_calculada], evaluacion.entrada.potencia_real_unidad.pk, potencia_unidad)[0],
                'salida__potencia': transformar_unidades_potencia([entrada.potencia_real], evaluacion.entrada.potencia_real_unidad.pk, potencia_unidad)[0],
            })

        return JsonResponse(res[:15], safe=False)