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
from calculos.unidades import transformar_unidades_presion, transformar_unidades_temperatura, transformar_unidades_densidad, transformar_unidades_viscosidad
from calculos.utils import fluido_existe, registrar_fluido

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

# VISTAS DE BOMBAS

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
        temp_presion_vapor = transformar_unidades_temperatura([temp_presion_vapor], unidad_temperatura)[0]
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
        fluido = int(request.GET.get('fluido'))

        unidad_temperatura = int(request.GET.get('temperatura_unidad'))

        unidad_viscosidad = int(request.GET.get('viscosidad_unidad'))
        unidad_densidad = request.GET.get('densidad_unidad')

        unidad_presion_vapor = int(request.GET.get('presion_vapor_unidad'))
        unidad_presion = int(request.GET.get('presion_unidad'))

        temp = float(request.GET.get('temperatura_operacion'))
        temp_presion_vapor = float(request.GET.get('temperatura_presion_vapor'))
        presion_succion = float(request.GET.get('presion_succion'))

        if(unidad_densidad):
            unidad_densidad = int(unidad_densidad)

        propiedades = self.calcular_propiedades(fluido, temp, temp_presion_vapor, 
                                                presion_succion, unidad_presion_vapor, 
                                                unidad_viscosidad, unidad_densidad, 
                                                unidad_presion, unidad_temperatura)

        return render(request, 'bombas/partials/fluido_bomba.html', propiedades)

class EdicionBomba(CreacionBomba):
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
    
    def get_bomba(self):
        return Bombas.objects.get(pk = self.kwargs['pk'])
    
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
        
class CreacionInstalacionBomba(View, SuperUserRequiredMixin):
    PREFIJO_INSTALACIONES = "formset-instalaciones"
    PREFIJO_TUBERIAS_SUCCION = "formset-succion"
    PREFIJO_TUBERIAS_DESCARGA = "formset-descarga"

    def get_bomba(self):
        return Bombas.objects.get(pk = self.kwargs['pk'])

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

class ConsultaEvaluacionBomba(ConsultaEvaluacion):
    model = EvaluacionBomba
    model_equipment = Bombas
    clase_equipo = " la Bomba"
    
    def get_queryset(self):
        new_context = super().get_queryset()

        new_context = new_context.select_related('instalacion_succion', 'instalacion_descarga', 'usuario')
        new_context = new_context.prefetch_related('instalacion_succion__tuberias', 'instalacion_succion__tuberias__diametro_tuberia_unidad',
                                                   'instalacion_succion__tuberias__longitud_tuberia_unidad', 'instalacion_succion__tuberias__material_tuberia',
                                                   'entrada_evaluacion_evaluacionbomba', 'entrada_evaluacion_evaluacionbomba__presion_unidad', 'entrada_evaluacion_evaluacionbomba__altura_unidad',
                                                   'entrada_evaluacion_evaluacionbomba__diametro_unidad', 'entrada_evaluacion_evaluacionbomba__flujo_unidad', 
                                                   'entrada_evaluacion_evaluacionbomba__temperatura_unidad', 'entrada_evaluacion_evaluacionbomba__potencia_unidad',
                                                   'entrada_evaluacion_evaluacionbomba__npshr_unidad', 'entrada_evaluacion_evaluacionbomba__densidad_unidad',
                                                   'entrada_evaluacion_evaluacionbomba__viscosidad_unidad', 'entrada_evaluacion_evaluacionbomba_presion_vapor_unidad',
                                                   'salida_general_evaluacionbomba', 'salida_secciones_evaluacionbomba')

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