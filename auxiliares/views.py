from typing import Any

from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages

from usuarios.views import SuperUserRequiredMixin
from auxiliares.models import *
from auxiliares.forms import *
from intercambiadores.models import Complejo, Planta
from calculos.termodinamicos import calcular_densidad, calcular_presion_vapor, calcular_viscosidad, calcular_densidad_relativa
from calculos.unidades import transformar_unidades_presion, transformar_unidades_flujo_volumetrico, transformar_unidades_potencia, transformar_unidades_longitud, transformar_unidades_temperatura, transformar_unidades_densidad, transformar_unidades_viscosidad
from calculos.utils import fluido_existe, registrar_fluido
from .evaluacion import evaluacion_bomba

# Create your views here.

class SeleccionEquipo(LoginRequiredMixin, View):
    """
    Resumen:
        Vista de consulta de los equipos auxiliares planteados en el proyecto.

    Atributos:
        context: dict
            Contexto de la vista. Actualmente solo incluye el título predeterminado.
    
    Métodos:
        get(self, request)
            Renderiza la plantilla de selección de equipos.
    """
    context = {
        'titulo': "SIEVEP - Selección de Equipo Auxiliar"
    }

    def get(self, request):
        return render(request, 'seleccion_equipo.html', context=self.context)

class CargarFluidoNuevo(View, SuperUserRequiredMixin):

    def get(self, request):
        return JsonResponse(fluido_existe(request.GET.get('cas')))

class RegistrarFluidoCAS(View, SuperUserRequiredMixin):
    
    def get(self, request):
        return JsonResponse(registrar_fluido(request.GET.get('cas'), request.GET.get('nombre')))
    
class ConsultaEvaluacion(ListView, LoginRequiredMixin):
    model = None
    model_equipment = None
    clase_equipo = ""
    template_name = 'consulta_evaluaciones.html'
    paginate_by = 10
    titulo = "SIEVEP - Consulta de Evaluaciones"

    def get_context_data(self, **kwargs: Any) -> "dict[str, Any]":
        context = super().get_context_data(**kwargs)
        context["titulo"] = "SIEVEP - Consulta de Evaluaciones"
        equipo = self.model_equipment.objects.filter(pk=self.kwargs['pk'])
        
        context['equipo'] = equipo

        context['nombre'] = self.request.GET.get('nombre', '')
        context['desde'] = self.request.GET.get('desde', '')
        context['hasta'] = self.request.GET.get('hasta')
        context['usuario'] = self.request.GET.get('usuario','')

        context['clase_equipo'] = self.clase_equipo

        return context
    
    def get_queryset(self):
        new_context = self.model.objects.filter(equipo__pk=self.kwargs['pk'], activo=True)
        desde = self.request.GET.get('desde', '')
        hasta = self.request.GET.get('hasta', '')
        usuario = self.request.GET.get('usuario', '')
        nombre = self.request.GET.get('nombre', '')

        if(desde != ''):
            new_context = new_context.filter(
                fecha__gte = desde
            )

        if(hasta != ''):
            new_context = new_context.filter(
                fecha__lte=hasta
            )

        if(usuario != ''):
            new_context = new_context.filter(
                usuario__first_name__icontains = usuario
            )

        if(nombre != ''):
            new_context = new_context.filter(
                nombre__icontains = nombre
            )

        return new_context
    
# VISTAS DE BOMBAS

class CargarBombaMixin():
    def get_bomba(self):
        return Bombas.objects.get(pk = self.kwargs['pk'])

class ConsultaBombas(LoginRequiredMixin, ListView):
    """
    Resumen:
        Vista para la consulta general de las bombas centrífugas (primer equipo auxiliar)

    Atributos:
        context: dict
            Contexto de la vista. Actualmente solo incluye el título predeterminado.
    
    Métodos:
        get(self, request)
            Renderiza la plantilla de selección de equipos.
    """

    model = Bombas
    template_name = 'bombas/consulta.html'
    paginate_by = 10

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
        context["titulo"] = "SIEVEP - Consulta de Bombas Centrífugas"
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

        context['link_creacion'] = 'creacion_bomba'

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

        new_context = new_context.select_related('instalacion_succion', 'instalacion_descarga', 'creado_por','editado_por','planta','tipo_bomba','detalles_motor','especificaciones_bomba','detalles_construccion','condiciones_diseno')
        new_context = new_context.prefetch_related(
            'instalacion_succion__elevacion_unidad', 'condiciones_diseno__capacidad_unidad', 
            'instalacion_succion__tuberias', 'instalacion_succion__tuberias__diametro_tuberia_unidad',

            'condiciones_diseno__presion_unidad', 'condiciones_diseno__npsha_unidad', 
            
            'condiciones_diseno__condiciones_fluido', 'condiciones_diseno__condiciones_fluido__temperatura_unidad',
            'condiciones_diseno__condiciones_fluido__presion_vapor_unidad', 'condiciones_diseno__condiciones_fluido__viscosidad_unidad',
            'condiciones_diseno__condiciones_fluido__concentracion_unidad', 'condiciones_diseno__condiciones_fluido__fluido',

            'especificaciones_bomba__velocidad_unidad', 'especificaciones_bomba__potencia_unidad',
            'especificaciones_bomba__npshr_unidad', 'especificaciones_bomba__cabezal_unidad',
            'especificaciones_bomba__id_unidad',

            'detalles_construccion__tipo_carcasa1', 'detalles_construccion__tipo_carcasa2',
            'detalles_construccion__tipo',

            'detalles_motor__potencia_motor_unidad','detalles_motor__velocidad_motor_unidad',
            'detalles_motor__voltaje_unidad', 'detalles_motor__velocidad_motor_unidad',

            'planta__complejo',
        )

        return new_context

class CreacionBomba(View, SuperUserRequiredMixin):
    success_message = "La nueva bomba ha sido registrada exitosamente. Los datos de instalación ya pueden ser cargados."

    def get_context(self):
        return {
            'form_bomba': BombaForm(), 
            'form_especificaciones': EspecificacionesBombaForm(), 
            'form_detalles_construccion': DetallesConstruccionBombaForm(), 
            'form_detalles_motor': DetallesMotorBombaForm(),
            'form_condiciones_diseno': CondicionesDisenoBombaForm(),
            'form_condiciones_fluido': CondicionFluidoBombaForm(),
            'titulo': 'SIEVEP - Creación de Bomba Centrífuga'
        }

    def get(self, request, **kwargs):
        return render(request, 'bombas/creacion_bomba.html', self.get_context())
    
    def almacenar_datos(self, form_bomba, form_detalles_motor, form_condiciones_fluido,
                            form_detalles_construccion, form_condiciones_diseno, 
                            form_especificaciones):
        
        valid = True
        
        with transaction.atomic():
                valid = valid and form_especificaciones.is_valid()

                if(form_especificaciones.is_valid()):
                    especificaciones = form_especificaciones.save()

                valid = valid and form_detalles_motor.is_valid()
                
                if(form_detalles_motor.is_valid()):
                    detalles_motor = form_detalles_motor.save()

                valid = valid and form_condiciones_fluido.is_valid() and form_detalles_construccion.is_valid()

                if(form_detalles_construccion.is_valid()):
                    detalles_construccion = form_detalles_construccion.save()

                valid = valid and form_condiciones_diseno.is_valid()

                if(valid):
                    if(form_condiciones_fluido.instance.calculo_propiedades == 'A'):
                        instancia = form_condiciones_fluido.instance

                        propiedades = ObtencionDatosFluidosBomba.calcular_propiedades(None, 
                            instancia.fluido.pk, instancia.temperatura_operacion, instancia.temperatura_presion_vapor, 
                            form_condiciones_diseno.instance.presion_succion, instancia.presion_vapor_unidad.pk, 
                            instancia.viscosidad_unidad.pk, instancia.densidad_unidad.pk if instancia.densidad_unidad else None, 
                            form_condiciones_diseno.instance.presion_unidad.pk, instancia.temperatura_unidad.pk
                        )

                        form_condiciones_fluido.instance.densidad = propiedades['densidad']
                        form_condiciones_fluido.instance.viscosidad = propiedades['viscosidad']
                        form_condiciones_fluido.instance.presion_vapor = propiedades['presion_vapor']

                    condiciones_fluido = form_condiciones_fluido.save()
                    form_condiciones_diseno.instance.condiciones_fluido = condiciones_fluido

                    if(form_condiciones_diseno.is_valid()):
                        condiciones_diseno = form_condiciones_diseno.save()

                valid = valid and form_bomba.is_valid()
                
                if(valid):
                    form_bomba.instance.creado_por = self.request.user
                    form_bomba.instance.detalles_motor = detalles_motor
                    form_bomba.instance.especificaciones_bomba = especificaciones
                    form_bomba.instance.condiciones_diseno = condiciones_diseno
                    form_bomba.instance.detalles_motor = detalles_motor
                    form_bomba.instance.detalles_construccion = detalles_construccion
                    form_bomba.instance.condiciones_fluido = condiciones_fluido

                    instalacion_succion = EspecificacionesInstalacion.objects.create()
                    instalacion_descarga = EspecificacionesInstalacion.objects.create()

                    form_bomba.instance.instalacion_succion = instalacion_succion
                    form_bomba.instance.instalacion_descarga = instalacion_descarga

                    form_bomba.save()

                    messages.success(self.request, self.success_message)
                    return redirect(f'/auxiliares/bombas/')
                else:
                    raise Exception("Ocurrió un error")
    
    def post(self, request):
        form_bomba = BombaForm(request.POST, request.FILES)
        form_especificaciones = EspecificacionesBombaForm(request.POST)
        form_detalles_motor = DetallesMotorBombaForm(request.POST)
        form_detalles_construccion = DetallesConstruccionBombaForm(request.POST)

        form_condiciones_diseno = CondicionesDisenoBombaForm(request.POST)
        form_condiciones_fluido = CondicionFluidoBombaForm(request.POST)

        try:
            return self.almacenar_datos(form_bomba, form_detalles_motor, form_condiciones_fluido,
                                form_detalles_construccion, form_condiciones_diseno, form_especificaciones)
        except Exception as e:
            return render(request, 'bombas/creacion_bomba.html', context={
                'form_bomba': form_bomba, 
                'form_especificaciones': form_especificaciones,
                'form_detalles_construccion': form_detalles_construccion, 
                'form_detalles_motor': form_detalles_motor,
                'form_condiciones_diseno': form_condiciones_diseno,
                'form_condiciones_fluido': form_condiciones_fluido,
                'edicion': True,
                'titulo': self.get_context()['titulo']
            })
        
class ObtencionDatosFluidosBomba(View, SuperUserRequiredMixin):
    def calcular_propiedades(self, fluido, temp, temp_presion_vapor, presion_succion, 
                              unidad_presion_vapor, unidad_viscosidad, unidad_densidad,
                              unidad_presion, unidad_temperatura) -> dict:
        
        temp = transformar_unidades_temperatura([temp], unidad_temperatura)[0]
        temp_presion_vapor = transformar_unidades_temperatura([temp_presion_vapor], unidad_temperatura)[0] if temp_presion_vapor else temp
        presion_succion = transformar_unidades_presion([presion_succion], unidad_presion)[0]

        cas = Fluido.objects.get(pk = fluido).cas
        viscosidad, bandera = calcular_viscosidad(cas, temp, presion_succion)
        propiedades = {
            'viscosidad': round(transformar_unidades_viscosidad([viscosidad], 44, unidad_viscosidad)[0], 6),
            'densidad': round(transformar_unidades_densidad([calcular_densidad(cas, temp, presion_succion)[0]], 43, unidad_densidad)[0] if unidad_densidad else calcular_densidad_relativa(cas, temp, presion_succion), 4),
            'presion_vapor': round(transformar_unidades_presion([calcular_presion_vapor(cas, temp_presion_vapor, presion_succion)], 33, unidad_presion_vapor)[0], 4),
            'bandera': bandera
        }

        return propiedades

    def get(self, request):
        tipo = request.GET.get('calculo_propiedades', 'A')

        unidad_temperatura = int(request.GET.get('temperatura_unidad'))
        unidad_viscosidad = int(request.GET.get('viscosidad_unidad'))
        unidad_densidad = request.GET.get('densidad_unidad')
        unidad_presion_vapor = int(request.GET.get('presion_vapor_unidad'))
        unidad_presion = int(request.GET.get('presion_unidad'))

        if(tipo == 'A'):
            fluido = int(request.GET.get('fluido'))

            temp = float(request.GET.get('temperatura_operacion')) 
            temp_presion_vapor = float(request.GET.get('temperatura_presion_vapor', temp))
            presion_succion = float(request.GET.get('presion_succion'))

            if(unidad_densidad):
                unidad_densidad = int(unidad_densidad)

            propiedades = self.calcular_propiedades(fluido, temp, temp_presion_vapor, 
                                                    presion_succion, unidad_presion_vapor, 
                                                    unidad_viscosidad, unidad_densidad, 
                                                    unidad_presion, unidad_temperatura)
        else:
            bomba = Bombas.objects.get(pk = request.GET.get('bomba'))
            diseno = bomba.condiciones_diseno
            fluido = diseno.condiciones_fluido
    
            propiedades = {
                'viscosidad':fluido.viscosidad,
                'viscosidad_unidad': fluido.viscosidad_unidad.pk,
                'densidad': fluido.densidad,
                'densidad_unidad': fluido.densidad_unidad.pk if fluido.densidad_unidad else None,
                'presion_vapor': fluido.presion_vapor,
                'presion_vapor_unidad': fluido.presion_vapor_unidad.pk,
                'presion_succion': diseno.presion_succion,
                'presion_unidad': diseno.presion_unidad.pk,
                'temperatura_operacion': fluido.temperatura_operacion,
                'temperatura_unidad': fluido.temperatura_unidad.pk,
                'ficha': True
            }

        return render(request, 'bombas/partials/fluido_bomba.html', propiedades)

class EdicionBomba(CreacionBomba, CargarBombaMixin):
    success_message = "Se han guardado los cambios exitosamente."
    def get_context(self):
        bomba = self.get_bomba()
        return {
            'form_bomba': BombaForm(instance = bomba), 
            'form_especificaciones': EspecificacionesBombaForm(instance = bomba.especificaciones_bomba), 
            'form_detalles_construccion': DetallesConstruccionBombaForm(instance = bomba.detalles_construccion), 
            'form_detalles_motor': DetallesMotorBombaForm(instance = bomba.detalles_motor),
            'form_condiciones_diseno': CondicionesDisenoBombaForm(instance = bomba.condiciones_diseno),
            'form_condiciones_fluido': CondicionFluidoBombaForm(instance = bomba.condiciones_diseno.condiciones_fluido),
            'titulo': f'SIEVEP - Edición de la Bomba {bomba.tag}',
            'edicion': True
        }
    
    def post(self, request, pk):
        bomba = self.get_bomba()

        form_bomba = BombaForm(request.POST, request.FILES ,instance=bomba)
        form_especificaciones = EspecificacionesBombaForm(request.POST, instance = bomba.especificaciones_bomba)
        form_detalles_motor = DetallesMotorBombaForm(request.POST, instance = bomba.detalles_motor)
        form_detalles_construccion = DetallesConstruccionBombaForm(request.POST, instance = bomba.detalles_construccion)

        form_condiciones_diseno = CondicionesDisenoBombaForm(request.POST, instance = bomba.condiciones_diseno)
        form_condiciones_fluido = CondicionFluidoBombaForm(request.POST, instance = bomba.condiciones_diseno.condiciones_fluido)

        try:
            return self.almacenar_datos(form_bomba, form_detalles_motor, form_condiciones_fluido,
                                form_detalles_construccion, form_condiciones_diseno, form_especificaciones)
        except Exception as e:
            return render(request, 'bombas/creacion_bomba.html', context={
                'form_bomba': form_bomba, 
                'form_especificaciones': form_especificaciones,
                'form_detalles_construccion': form_detalles_construccion, 
                'form_detalles_motor': form_detalles_motor,
                'form_condiciones_diseno': form_condiciones_diseno,
                'form_condiciones_fluido': form_condiciones_fluido,
                'edicion': True,
                'titulo': self.get_context()['titulo']
            })
        
class CreacionInstalacionBomba(View, CargarBombaMixin, SuperUserRequiredMixin):
    PREFIJO_INSTALACIONES = "formset-instalaciones"
    PREFIJO_TUBERIAS_SUCCION = "formset-succion"
    PREFIJO_TUBERIAS_DESCARGA = "formset-descarga"

    def get_context(self):
        bomba = self.get_bomba()
        instalacion_succion = bomba.instalacion_succion
        instalacion_descarga = bomba.instalacion_descarga

        context = {
            'bomba': bomba,
            'forms_instalacion': EspecificacionesInstalacionFormSet(queryset=EspecificacionesInstalacion.objects.filter(pk__in = [instalacion_succion.pk, instalacion_descarga.pk]), prefix = self.PREFIJO_INSTALACIONES),
            'forms_tuberia_succion': TuberiaFormSet(queryset=instalacion_succion.tuberias.all(), prefix=self.PREFIJO_TUBERIAS_SUCCION),
            'forms_tuberia_descarga': TuberiaFormSet(queryset=instalacion_descarga.tuberias.all(), prefix=self.PREFIJO_TUBERIAS_DESCARGA),
            'titulo': "Especificaciones de Instalación"
        }

        return context
    
    def post(self, request, **kwargs):
        bomba = self.get_bomba()

        try:
            with transaction.atomic():
                formset_instalacion = EspecificacionesInstalacionFormSet(request.POST or None, prefix=self.PREFIJO_INSTALACIONES)
                formset_tuberias_succion = TuberiaFormSet(request.POST or None, prefix=self.PREFIJO_TUBERIAS_SUCCION)
                formset_tuberias_descarga = TuberiaFormSet(request.POST or None, prefix=self.PREFIJO_TUBERIAS_DESCARGA)

                formset_instalacion.is_valid()
                formset_tuberias_succion.is_valid()
                formset_tuberias_descarga.is_valid()

                if(formset_instalacion.is_valid()):
                    succion = formset_instalacion.forms[0]
                    succion.instance.usuario = request.user
                    succion.instance.pk = None
                    descarga = formset_instalacion.forms[1]
                    descarga.instance.usuario = request.user
                    descarga.instance.pk = None

                    succion = succion.save()
                    descarga = descarga.save()

                    bomba.instalacion_succion = succion
                    bomba.instalacion_descarga = descarga
                    bomba.save()
                else:
                    raise Exception("Ocurrió un error al validar los datos de instalación.")
                
                if(formset_tuberias_succion.is_valid()):
                    for form in formset_tuberias_succion:
                        if(form.is_valid()):
                            form.instance.pk = None
                            form.instance.instalacion = succion
                            form.save()
                elif(int(request.POST.get('formset-succion-TOTAL_FORMS')) > 1):
                    print(formset_tuberias_succion.errors)
                    raise Exception("Ocurrió un error al validar los datos de tuberías de la succión.")

                if(formset_tuberias_descarga.is_valid()):
                    for form in formset_tuberias_descarga:
                        if(form.is_valid()):
                            form.instance.pk = None
                            form.instance.instalacion = descarga
                            form.save()
                elif(int(request.POST.get('formset-descarga-TOTAL_FORMS')) > 1):
                    raise Exception("Ocurrió un error al validar los datos de tuberías de la descarga.")

                messages.success(request, "Se han actualizado los datos de instalación exitosamente.")
                return redirect('/auxiliares/bombas/')    
                      
        except Exception as e:
            print(str(e))        
            return render(request, 'bombas/creacion_instalacion.html', context={'forms_instalacion': formset_instalacion, 'forms_tuberia_succion': formset_tuberias_succion, 'forms_tuberia_descarga': formset_tuberias_descarga}) 

    def get(self, request, **kwargs):
        return render(request, 'bombas/creacion_instalacion.html', context=self.get_context())

class ConsultaEvaluacionBomba(ConsultaEvaluacion):
    model = EvaluacionBomba
    model_equipment = Bombas
    clase_equipo = " la Bomba"
    
    def get_queryset(self):
        new_context = super().get_queryset()

        new_context = new_context.select_related('instalacion_succion', 'instalacion_descarga', 'creado_por', 'entrada', 'salida')
        new_context = new_context.prefetch_related('instalacion_succion__tuberias', 'instalacion_succion__tuberias__diametro_tuberia_unidad',
                                                   'instalacion_succion__tuberias__longitud_tuberia_unidad', 'instalacion_succion__tuberias__material_tuberia',
                                                   'entrada__presion_unidad', 'entrada__altura_unidad',
                                                   'entrada__flujo_unidad', 'salida_secciones_evaluacionbomba__datos_tramos_seccion',
                                                   'entrada__temperatura_unidad', 'entrada__potencia_unidad', 'salida__velocidad_unidad',
                                                   'entrada__npshr_unidad', 'entrada__densidad_unidad', 'salida__potencia_unidad',
                                                   'entrada__viscosidad_unidad', 'entrada__presion_vapor_unidad', 'salida_secciones_evaluacionbomba',
                                                   'salida__cabezal_total_unidad', 'salida_secciones_evaluacionbomba__datos_tramos_seccion', 'salida_secciones_evaluacionbomba__datos_tramos_seccion__tramo',
                                                   'salida_secciones_evaluacionbomba__datos_tramos_seccion__tramo__diametro_tuberia_unidad', 'salida_secciones_evaluacionbomba__datos_tramos_seccion__tramo__longitud_tuberia_unidad',
                                                   'salida_secciones_evaluacionbomba__datos_tramos_seccion__tramo__material_tuberia')

        return new_context

    def get_context_data(self, **kwargs: Any) -> "dict[str, Any]":
        context = super().get_context_data(**kwargs)
        context['equipo'] = context['equipo']
        context['equipo'] = context['equipo'].select_related('instalacion_succion', 'instalacion_descarga', 'creado_por','editado_por','planta','tipo_bomba','detalles_motor','especificaciones_bomba','detalles_construccion','condiciones_diseno')
        context['equipo'] = context['equipo'].prefetch_related(
            'instalacion_succion__elevacion_unidad', 'condiciones_diseno__capacidad_unidad', 
            'instalacion_succion__tuberias', 'instalacion_succion__tuberias__diametro_tuberia_unidad',

            'condiciones_diseno__presion_unidad', 'condiciones_diseno__npsha_unidad', 
            
            'condiciones_diseno__condiciones_fluido', 'condiciones_diseno__condiciones_fluido__temperatura_unidad',
            'condiciones_diseno__condiciones_fluido__presion_vapor_unidad', 'condiciones_diseno__condiciones_fluido__viscosidad_unidad',
            'condiciones_diseno__condiciones_fluido__concentracion_unidad', 'condiciones_diseno__condiciones_fluido__fluido',

            'especificaciones_bomba__velocidad_unidad', 'especificaciones_bomba__potencia_unidad',
            'especificaciones_bomba__npshr_unidad', 'especificaciones_bomba__cabezal_unidad',
            'especificaciones_bomba__id_unidad',

            'detalles_construccion__tipo_carcasa1', 'detalles_construccion__tipo_carcasa2',
            'detalles_construccion__tipo',

            'detalles_motor__potencia_motor_unidad','detalles_motor__velocidad_motor_unidad',
            'detalles_motor__voltaje_unidad', 'detalles_motor__velocidad_motor_unidad',

            'planta__complejo',
        )

        context['equipo'] = context['equipo'][0]

        return context

class CalcularResultados(View, LoginRequiredMixin):
    bomba = None

    def evaluar(self, request):
        tipo_propiedades = request.POST.get('calculo_propiedades', 'A')
        
        velocidad = self.bomba.especificaciones_bomba.velocidad
        temp_operacion = float(request.POST.get('temperatura_operacion')) if tipo_propiedades != 'F' else self.bomba.condiciones_diseno.condiciones_fluido.temperatura_operacion
        presion_succion = float(request.POST.get('presion_succion')) if tipo_propiedades != 'F' else self.bomba.condiciones_diseno.presion_succion
        presion_descarga = float(request.POST.get('presion_descarga'))
        altura_succion = float(request.POST.get('altura_succion', 0))
        altura_descarga = float(request.POST.get('altura_descarga', 0))
        presion_descarga = float(request.POST.get('presion_descarga'))
        diametro_interno_succion = self.bomba.especificaciones_bomba.succion_id
        diametro_interno_descarga = self.bomba.especificaciones_bomba.descarga_id
        flujo = float(request.POST.get('flujo'))
        potencia = float(request.POST.get('potencia'))
        npshr = float(request.POST.get('npshr')) if request.POST.get('npshr') else None

        # Conversión de Parámetros a SI
        temp_operacion = transformar_unidades_temperatura([temp_operacion], int(request.POST.get('temperatura_unidad', self.bomba.condiciones_diseno.condiciones_fluido.temperatura_unidad.pk)))[0]
        presion_descarga, presion_succion = transformar_unidades_presion([presion_descarga, presion_succion], int(request.POST.get('presion_unidad', self.bomba.condiciones_diseno.presion_unidad.pk)))
        altura_descarga, altura_succion = transformar_unidades_longitud([altura_descarga, altura_succion], int(request.POST.get('altura_unidad')))
        diametro_interno_succion, diametro_interno_descarga = transformar_unidades_longitud([diametro_interno_succion, diametro_interno_descarga], self.bomba.especificaciones_bomba.id_unidad.pk)
        potencia = transformar_unidades_potencia([potencia], int(request.POST.get('potencia_unidad')))[0]
        flujo = transformar_unidades_flujo_volumetrico([flujo], int(request.POST.get('flujo_unidad')))[0]
        npshr = transformar_unidades_longitud([npshr], int(request.POST.get('npshr_unidad')))[0]

        res = evaluacion_bomba(
            self.bomba, velocidad, temp_operacion,
            presion_succion, presion_descarga,
            altura_succion, altura_descarga,
            diametro_interno_succion, diametro_interno_descarga,
            flujo, potencia, npshr, tipo_propiedades, 
            [request.POST.get('viscosidad'), request.POST.get('densidad'), request.POST.get('presion_vapor')],
            [request.POST.get('viscosidad_unidad'), request.POST.get('densidad_unidad'), request.POST.get('presion_vapor_unidad')]
        )

        res['cabezal_total'] = transformar_unidades_longitud([res['cabezal_total']], self.bomba.especificaciones_bomba.cabezal_unidad.pk)
        res['potencia_calculada'] = transformar_unidades_longitud([res['potencia_calculada']], self.bomba.especificaciones_bomba.potencia_unidad.pk)
        res['npsha'] = transformar_unidades_longitud([res['npsha']], int(request.POST.get('npshr_unidad')))
        res['npshr'] = npshr
        res['npshr_unidad'] = Unidades.objects.get(pk = int(request.POST.get('npshr_unidad'))) 
        return res
    
    def calcular(self, request):
        res = self.evaluar(request)
        print(res)
        return render(request, 'bombas/partials/resultado_evaluacion.html', context={'res': res, 'bomba': self.bomba})

    def parse_entrada(self, request, specs, res):
        condiciones_diseno = self.bomba.condiciones_diseno
        condiciones_fluido = condiciones_diseno.condiciones_fluido
        return {
            'presion_succion': request.POST.get('presion_succion', condiciones_diseno.presion_succion),
            'presion_descarga': request.POST.get('presion_descarga'),
            'presion_unidad': request.POST.get('presion_unidad', condiciones_diseno.presion_unidad.pk),

            'altura_succion': request.POST.get('altura_succion'),
            'altura_descarga': request.POST.get('altura_descarga'),
            'altura_unidad': request.POST.get('altura_unidad'),

            'velocidad': specs.velocidad,

            'flujo': request.POST.get('flujo'),
            'flujo_unidad': request.POST.get('flujo_unidad'),

            'temperatura_operacion': request.POST.get('temperatura_operacion', condiciones_fluido.temperatura_operacion),
            'temperatura_unidad': request.POST.get('temperatura_unidad', condiciones_fluido.temperatura_unidad.pk),

            'potencia': request.POST.get('potencia'),
            'potencia_unidad': request.POST.get('potencia_unidad'),

            'npshr': request.POST.get('npshr'),
            'npshr_unidad': request.POST.get('npshr_unidad'),

            'densidad': res['propiedades']['densidad'],
            'densidad_unidad': request.POST.get('densidad_unidad', condiciones_fluido.densidad_unidad.pk if condiciones_fluido.densidad_unidad else None),

            'viscosidad': res['propiedades']['viscosidad'],
            'viscosidad_unidad': request.POST.get('viscosidad_unidad', condiciones_fluido.viscosidad_unidad.pk),

            'presion_vapor': res['propiedades']['presion_vapor'],
            'presion_vapor_unidad': request.POST.get('presion_vapor_unidad', condiciones_fluido.presion_vapor_unidad.pk),

            'calculo_propiedades': request.POST.get('calculo_propiedades'),
        }

    def almacenar_bdd(self, form_entrada, form_evaluacion):
        res = self.evaluar(self.request)

        try:
            with transaction.atomic():
                form_entrada.instance.velocidad = self.bomba.especificaciones_bomba.velocidad
                form_entrada.instance.velocidad_unidad = self.bomba.especificaciones_bomba.velocidad_unidad
                form_entrada.save()

                especificaciones = self.bomba.especificaciones_bomba

                salida = SalidaEvaluacionBombaGeneral.objects.create(
                    cabezal_total = res['cabezal_total'][0],
                    cabezal_total_unidad = especificaciones.cabezal_unidad,
                    potencia = res['potencia_calculada'][0],
                    potencia_unidad = especificaciones.potencia_unidad,
                    eficiencia = res['eficiencia'],
                    velocidad = res['velocidad_especifica'],
                    velocidad_unidad = especificaciones.velocidad_unidad,
                    npsha = res['npsha'][0],
                    cavita = None if res['cavita'] == 'D' else res['cavita'] == 'S'
                )

                form_evaluacion.instance.equipo = self.bomba
                form_evaluacion.instance.creado_por = self.request.user
                form_evaluacion.instance.instalacion_succion = self.bomba.instalacion_succion
                form_evaluacion.instance.instalacion_descarga = self.bomba.instalacion_descarga
                form_evaluacion.instance.entrada = form_entrada.instance
                form_evaluacion.instance.salida = salida

                evaluacion = form_evaluacion.save()

                salida_succion = SalidaSeccionesEvaluacionBomba.objects.create(
                    lado = 'S',
                    perdida_carga_tuberia = res['perdidas']['s']['tuberia'],
                    perdida_carga_accesorios = res['perdidas']['s']['accesorio'],
                    perdida_carga_total = res['perdidas']['s']['total'],
                    evaluacion = evaluacion
                )

                salida_descarga = SalidaSeccionesEvaluacionBomba.objects.create(
                    lado = 'D',
                    perdida_carga_tuberia = res['perdidas']['d']['tuberia'],
                    perdida_carga_accesorios = res['perdidas']['d']['accesorio'],
                    perdida_carga_total = res['perdidas']['d']['total'],
                    evaluacion = evaluacion
                )

                for i,tramo in enumerate(self.bomba.instalacion_succion.tuberias.all().order_by('pk')):
                    EntradaTramos.objects.create(
                        tramo = tramo,
                        flujo = res['flujo']['s'][i]['tipo_flujo'],
                        velocidad = res['flujo']['s'][i]['velocidad'],
                        salida = salida_succion
                    )

                for i,tramo in enumerate(self.bomba.instalacion_descarga.tuberias.all().order_by('pk')):
                    EntradaTramos.objects.create(
                        tramo = tramo,
                        flujo = res['flujo']['d'][i]['tipo_flujo'],
                        velocidad = res['flujo']['d'][i]['velocidad'],
                        salida = salida_descarga
                    )

            messages.success(self.request, "Se almacenó la evaluación correctamente.")
            return render(self.request, 'bombas/partials/carga_lograda.html', {'bomba': self.bomba})

        except Exception as e:
            print(str(e))

            return render(self.request, 'bombas/partials/carga_fallida.html', {'bomba': self.bomba})

    def almacenar(self, request):
        res = self.evaluar(request)
        entrada = self.parse_entrada(request, self.bomba.especificaciones_bomba, res) 
        
        form_entrada = EntradaEvaluacionBombaForm(entrada)
        form_evaluacion = EvaluacionBombaForm(request.POST)

        print(form_entrada.is_valid(), form_evaluacion.is_valid())

        if(form_entrada.is_valid() and form_evaluacion.is_valid()):
            return self.almacenar_bdd(form_entrada, form_evaluacion)
        else:
            print(form_entrada.errors)
            print(form_evaluacion.errors)
            context = {
                'bomba': self.bomba,
                'form_evaluacion': form_evaluacion,
                'form_entrada_evaluacion': form_evaluacion,
                'titulo': "Evaluación de Bomba"
            }

            return render(request, 'bombas/evaluacion.html', context)

    def post(self, request, pk):
        # Obtención de Parámetros
        self.bomba = Bombas.objects.get(pk = pk)

        print(request.POST)
        
        if(request.POST.get('submit') == 'calcular'):
            res = self.calcular(request)
        elif(request.POST.get('submit') == 'almacenar'):
            res = self.almacenar(request)

        return res

class CreacionEvaluacionBomba(View, LoginRequiredMixin, CargarBombaMixin):
    PREFIJO_INSTALACIONES = "formset-instalaciones"
    PREFIJO_TUBERIAS_SUCCION = "formset-succion"
    PREFIJO_TUBERIAS_DESCARGA = "formset-descarga"

    def get_context_data(self):
        bomba = self.get_bomba()
        precargo = {
            'altura_succion': bomba.instalacion_succion.elevacion,
            'altura_descarga': bomba.instalacion_descarga.elevacion,
            'altura_unidad': bomba.instalacion_succion.elevacion_unidad.pk,
            'potencia': bomba.especificaciones_bomba.potencia_maxima,
            'potencia_unidad': bomba.especificaciones_bomba.potencia_unidad,
            'npshr': bomba.especificaciones_bomba.npshr,
            'npshr_unidad': bomba.especificaciones_bomba.npshr_unidad
        }
        context = {
            'bomba': bomba,
            'form_evaluacion': EvaluacionBombaForm(),
            'form_entrada_evaluacion': EntradaEvaluacionBombaForm(precargo),
            'titulo': "Evaluación de Bomba"
        }

        return context
    
    def get(self, request, pk):
        return render(request, 'bombas/evaluacion.html', self.get_context_data())