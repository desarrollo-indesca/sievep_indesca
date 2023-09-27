from typing import Any
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.db import transaction
import numpy

# VISTAS PARA LOS INTERCAMBIADORES TUBO/CARCASA

class CrearIntercambiadorTuboCarcasa(View):
    context = {
        'titulo': "Creación de Intercambiador Tubo Carcasa"
    }

    def post(self, request): # Envío de Formulario de Creación
        print(request.POST)

        if(Intercambiador.objects.filter(tag = request.POST['tag']).exists()):
            copia_context = self.context
            copia_context['previo'] = request.POST
            copia_context['error'] = f'El tag {request.POST["tag"]} ya está registrado en el sistema.' 

            return render(request, 'tubo_carcasa/creacion.html', context=self.context)
        
        with transaction.atomic():
            intercambiador = Intercambiador.objects.create(
                tag = request.POST['tag'],
                tipo = TipoIntercambiador.objects.get(pk=1),
                fabricante = request.POST['fabricante'],
                planta = Planta.objects.get(pk=request.POST['planta']),
                tema = Tema.objects.get(pk=request.POST['tema']),
                servicio = request.POST['servicio'],
                arreglo_flujo = request.POST['flujo']
            )

            propiedades = PropiedadesTuboCarcasa.objects.create(
                intercambiador = intercambiador,
                area = request.POST['area'],
                area_unidad = Unidades.objects.get(pk=request.POST['unidad_area']),
                numero_tubos = request.POST['no_tubos'],
                longitud_tubos = request.POST['longitud_tubos'],
                longitud_tubos_unidad = Unidades.objects.get(pk=request.POST['longitud_tubos_unidad']),
                diametro_externo_tubos = request.POST['od_tubos'],
                diametro_interno_tubos = request.POST['id_carcasa'],
                diametro_tubos_unidad = Unidades.objects.get(pk=request.POST['unidad_diametros']),

                fluido_carcasa = Fluido.objects.get(pk=request.POST['fluido_carcasa']),
                material_carcasa = request.POST['material_carcasa'],
                conexiones_entrada_carcasa = request.POST['conexiones_entrada_carcasa'],
                conexiones_salida_carcasa = request.POST['conexiones_salida_carcasa'],
                
                fluido_tubo = Fluido.objects.get(pk=request.POST['fluido_tubo']),
                material_tubo = request.POST['material_tubo'],
                conexiones_entrada_tubos = request.POST['conexiones_entrada_tubo'],
                conexiones_salida_tubos = request.POST['conexiones_salida_tubo'],
                tipo_tubo = TiposDeTubo.objects.get(pk=request.POST['tipo_tubo']),

                pitch_tubos = request.POST['pitch'],
                unidades_pitch = Unidades.objects.get(pk=request.POST['unidades_pitch']),

                criticidad = request.POST['criticidad'],

                arreglo_serie = request.POST['arreglo_serie'],
                arreglo_paralelo = request.POST['arreglo_paralelo'],
                numero_pasos_tubo = request.POST['numero_pasos_tubo'],
                numero_pasos_carcasa = request.POST['numero_pasos_carcasa'],
                q =  request.POST['calor'],
                u =  request.POST['u'],
                ensuciamiento =  request.POST['ensuciamiento']
            )

            condiciones_diseno_tubo = CondicionesTuboCarcasa.objects.create(
                intercambiador = propiedades,
                lado = 'T',
                temp_entrada = request.POST['temp_in_tubo'],
                temp_salida = request.POST['temp_out_tubo'],
                temperaturas_unidad = Unidades.objects.get(pk=request.POST['unidad_temperaturas']),

                cambio_de_fase = request.POST['cambio_fase_tubo'],
                
                flujo_masico = request.POST['flujo_tubo'],
                flujo_vapor_entrada = request.POST['flujo_vapor_in_tubo'],
                flujo_vapor_salida = request.POST['flujo_vapor_out_tubo'],
                flujo_liquido_entrada = request.POST['flujo_liquido_in_tubo'],
                flujo_liquido_salida = request.POST['flujo_liquido_out_tubo'],
                caida_presion_max = request.POST['caida_presion_max_tubo'],
                caida_presion_min = request.POST['caida_presion_min_tubo'],
                presion_entrada = request.POST['presion_entrada_tubo'],
                unidad_presion = Unidades.objects.get(pk=request.POST['unidad_presiones']),

                fouling = request.POST['fouling_tubo']
            )

            condiciones_diseno_carcasa = CondicionesTuboCarcasa.objects.create(
                intercambiador = propiedades,
                lado = 'C',
                temp_entrada = request.POST['temp_in_carcasa'],
                temp_salida = request.POST['temp_out_carcasa'],
                temperaturas_unidad =Unidades.objects.get(pk=request.POST['unidad_temperaturas']),

                cambio_de_fase = request.POST['cambio_fase_carcasa'],
                
                flujo_masico = request.POST['flujo_carcasa'],
                flujo_vapor_entrada = request.POST['flujo_vapor_in_carcasa'],
                flujo_vapor_salida = request.POST['flujo_vapor_out_carcasa'],
                flujo_liquido_entrada = request.POST['flujo_liquido_in_carcasa'],
                flujo_liquido_salida = request.POST['flujo_liquido_out_carcasa'],
                flujos_unidad = Unidades.objects.get(pk=request.POST['unidad_flujos']),
                
                presion_entrada = request.POST['presion_entrada_carcasa'],
                caida_presion_max = request.POST['caida_presion_max_carcasa'],
                caida_presion_min = request.POST['caida_presion_min_carcasa'],
                unidad_presion = Unidades.objects.get(pk=request.POST['unidad_presiones']),

                fouling = request.POST['fouling_carcasa']
            )

            request.session['mensaje'] = "El nuevo intercambiador ha sido registrado exitosamente."

            return redirect('/intercambiadores/tubo_carcasa/')
    
    def get(self, request):
        self.context['complejos'] = Complejo.objects.all()
        self.context['plantas'] = Planta.objects.filter(complejo__pk=1)
        self.context['tipos'] = TiposDeTubo.objects.all()
        self.context['temas'] = Tema.objects.all()
        self.context['fluidos'] = Fluido.objects.all()

        if(self.context.get('error')):
            del(self.context['error'])
            
        if(self.context.get('previo')):
            del(self.context['previo'])            

        return render(request, 'tubo_carcasa/creacion.html', context=self.context)

class CrearEvaluacionTuboCarcasa(View):
    context = {
        'titulo': "Evaluación Tubo Carcasa"
    }

    def get(self, request, pk):
        context = self.context
        context['intercambiador'] = PropiedadesTuboCarcasa.objects.get(pk=pk)

        return render(request, 'tubo_carcasa/evaluaciones/creacion.html', context=context)

class EditarIntercambiadorTuboCarcasa(View):
    context = {
        'titulo': "Edición de Intercambiador Tubo Carcasa"
    }

    def post(self, request, pk):
        print(request.POST)
        with transaction.atomic():
            propiedades = PropiedadesTuboCarcasa.objects.get(pk=pk)
            propiedades.area = request.POST['area']
            propiedades.numero_tubos = request.POST['no_tubos']
            propiedades.longitud_tubos = request.POST['longitud_tubos']
            propiedades.diametro_externo_tubos = request.POST['od_tubos']
            propiedades.diametro_interno_tubos = request.POST['id_carcasa']
            propiedades.tipo_tubo = TiposDeTubo.objects.get(pk=request.POST['tipo_tubo'])
            propiedades.pitch_tubos = request.POST['pitch']
            propiedades.material_carcasa = request.POST['material_carcasa']
            propiedades.material_tubo = request.POST['material_tubo']
            propiedades.q = request.POST['calor']
            propiedades.ensuciamiento = request.POST['ensuciamiento']
            propiedades.u = request.POST['u']
            propiedades.conexiones_entrada_carcasa = request.POST['conexiones_entrada_carcasa']
            propiedades.conexiones_salida_carcasa = request.POST['conexiones_salida_carcasa']
            propiedades.conexiones_entrada_tubos = request.POST['conexiones_entrada_tubo']
            propiedades.conexiones_salida_tubos = request.POST['conexiones_salida_tubo']
            propiedades.numero_pasos_carcasa = request.POST['numero_pasos_carcasa']
            propiedades.numero_pasos_tubo = request.POST['numero_pasos_tubo']
            propiedades.numero_pasos_carcasa = request.POST['numero_pasos_carcasa']
            propiedades.fluido_tubo = Fluido.objects.get(pk=request.POST['fluido_tubo'])
            propiedades.fluido_carcasa = Fluido.objects.get(pk=request.POST['fluido_carcasa'])
            propiedades.save()

            condiciones_tubo = propiedades.condicion_tubo()
            condiciones_tubo.temp_entrada = request.POST['temp_in_tubo']
            condiciones_tubo.temp_salida = request.POST['temp_out_tubo']
            condiciones_tubo.flujo_vapor_entrada = request.POST['flujo_vapor_in_tubo']
            condiciones_tubo.flujo_liquido_salida = request.POST['flujo_vapor_out_tubo']
            condiciones_tubo.flujo_liquido_entrada = request.POST['flujo_liquido_in_tubo']
            condiciones_tubo.cambio_de_fase = request.POST['cambio_fase_tubo']
            condiciones_tubo.flujo_masico = request.POST['flujo_tubo']
            condiciones_tubo.presion_entrada = request.POST['presion_entrada_tubo']
            condiciones_tubo.caida_presion_max = request.POST['caida_presion_max_tubo']
            condiciones_tubo.caida_presion_min = request.POST['caida_presion_min_tubo']
            condiciones_tubo.fouling = request.POST['fouling_tubo']
            condiciones_tubo.save()

            condiciones_carcasa = propiedades.condicion_carcasa()
            condiciones_carcasa.temp_entrada = request.POST['temp_in_carcasa']
            condiciones_carcasa.temp_salida = request.POST['temp_out_carcasa']
            condiciones_carcasa.flujo_vapor_entrada = request.POST['flujo_vapor_in_carcasa']
            condiciones_carcasa.flujo_liquido_salida = request.POST['flujo_vapor_out_carcasa']
            condiciones_carcasa.flujo_liquido_entrada = request.POST['flujo_liquido_in_carcasa']
            condiciones_carcasa.cambio_de_fase = request.POST['cambio_fase_carcasa']
            condiciones_carcasa.flujo_masico = request.POST['flujo_carcasa']
            condiciones_carcasa.presion_entrada = request.POST['presion_entrada_carcasa']
            condiciones_carcasa.caida_presion_max = request.POST['caida_presion_max_carcasa']
            condiciones_carcasa.caida_presion_min = request.POST['caida_presion_min_carcasa']
            condiciones_carcasa.fouling = request.POST['fouling_carcasa']
            condiciones_carcasa.save()

            intercambiador = Intercambiador.objects.get(pk=propiedades.intercambiador.pk)
            intercambiador.tag = request.POST['tag']
            intercambiador.fabricante = request.POST['fabricante']
            intercambiador.servicio = request.POST['servicio']
            intercambiador.arreglo_flujo = request.POST['flujo']
            intercambiador.save()



        return redirect("/intercambiadores/tubo_carcasa/")
    
    def get(self, request, pk):
        self.context['intercambiador'] = PropiedadesTuboCarcasa.objects.get(pk=pk)
        self.context['complejos'] = Complejo.objects.all()
        self.context['temas'] = Tema.objects.all()
        self.context['tipos'] = TiposDeTubo.objects.all()
        self.context['plantas'] = Planta.objects.filter(complejo__pk=1)
        self.context['fluidos'] = Fluido.objects.all()

        return render(request, 'tubo_carcasa/edicion.html', context=self.context)

class ConsultaEvaluacionesTuboCarcasa(View):
    context = {
        'titulo': "SIEVEP - Intercambiadores de Tubo/Carcasa",
        'numeros': [1,2,3,4,5,6,7,8,9,10]
    }

    def get(self, request, pk):
        context = self.context
        context['intercambiador'] = PropiedadesTuboCarcasa.objects.get(pk=pk)

        return render(request, 'tubo_carcasa/evaluaciones/consulta.html', context=context)

class ConsultaTuboCarcasa(ListView):
    model = PropiedadesTuboCarcasa
    template_name = 'tubo_carcasa/consulta.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "SIEVEP - Consulta de Intercambiadores de Tubo/Carcasa"
        context['complejos'] = Complejo.objects.all()

        if(self.request.GET.get('complejo')):
            context['plantas'] = Planta.objects.filter(complejo__pk = self.request.GET.get('complejo'))

        context['tag'] = self.request.GET.get('tag', '')
        context['servicio'] = self.request.GET.get('servicio', '')
        context['complejox'] = self.request.GET.get('complejo')
        context['plantax'] = self.request.GET.get('planta')

        if(context['complejox']):
            context['complejox'] = int(context['complejox'])
        
        if(context['plantax']):
            context['plantax'] = int(context['plantax'])

        print(context)

        return context
    
    def get_queryset(self):
        tag = self.request.GET.get('tag', '')
        servicio = self.request.GET.get('servicio', '')
        complejo = self.request.GET.get('complejo', '')
        planta = self.request.GET.get('planta', '')

        new_context = None

        if(planta != '' and complejo != ''):
            new_context = self.model.objects.filter(
                intercambiador__planta__pk=planta
            )
        elif(complejo != ''):
            new_context = new_context.filter(
                intercambiador__planta__complejo__pk=complejo
            ) if new_context else self.model.objects.filter(
                intercambiador__planta__complejo__pk=complejo
            )

        if(not(new_context is None)):
            new_context = new_context.filter(
                intercambiador__servicio__icontains = servicio,
                intercambiador__tag__icontains = tag
            )
        else:
            new_context = self.model.objects.filter(
                intercambiador__servicio__icontains = servicio,
                intercambiador__tag__icontains = tag
            )

        return new_context

# VISTAS GENERALES PARA LOS INTERCAMBIADORES DE CALOR

class SeleccionTipo(View):
    context = {
        'titulo': "SIEVEP - Selección de Tipo de Intercambiador"
    }

    def get(self, request):
        return render(request, 'seleccion_tipo.html', context=self.context)

# ESTAS YA NO SE USARÁN

class Simulaciones(View):
    context = {
        'titulo': "SIEVEP - Evaluaciones de Intercambiadores"
    }

    def get(self, request):
        return render(request, 'simulaciones.html', context=self.context)
    
class FormularioSimulaciones(View):
    context = {
        'titulo': "SIEVEP - Evaluaciones de Intercambiadores"
    }

    def get(self, request):
        self.context['plantas'] = Planta.objects.all().order_by('codigo')
        self.context['areas'] = Area.objects.filter(planta = self.context['plantas'].first()).order_by('nombre')
        self.context['intercambiadores'] = Intercambiador.objects.filter(area = self.context['areas'].first()).order_by('codigo')
        
        print(self.context)

        intercambiador = self.context['intercambiadores'].first()
        self.context['diametro_ex_carcasa'] =  intercambiador.diametro_ex_carcasa
        self.context['diametro_ex_tubos'] =  intercambiador.diametro_ex_tubos
        self.context['longitud_tubo'] =  intercambiador.longitud_tubo

        self.context['fluidos_servicio'] = Fluido.objects.filter(pk__in = intercambiador.condiciones.values('fluido_servicio'))
        self.context['fluidos_interno'] = Fluido.objects.filter(pk__in = intercambiador.condiciones.values('fluido_interno'))
        
        return render(request, 'formulario.html', context=self.context)
    
    def post(self, request):
        # CARGA DEL REQUEST.POST
        t1_serv = float(request.POST['temp_in_serv'])
        t2_serv = float(request.POST['temp_out_serv'])
        t1_proc = float(request.POST['temp_in_proceso'])
        t2_proc = float(request.POST['temp_out_proceso'])

        w_serv = float(request.POST['flujo_externo'])
        w_proc = float(request.POST['flujo_interno'])

        intercambiador = Intercambiador.objects.get(pk = request.POST['intercambiador'])
        condiciones = CondicionesSimulacionTubos.objects.get(intercambiador = intercambiador, tipo = request.POST['condiciones'],
            fluido_servicio = int(request.POST['fluido_externo']), fluido_interno = int(request.POST['fluido_interno']))

        # CÁLCULO DE DATOS

        # Promedio de las temperaturas
        tprom_serv = numpy.mean([t1_serv, t2_serv]) # REVISADO
        tprom_proc = numpy.mean([t1_proc, t2_proc]) # REVISADO

        # Cálculo de las capacidades caloríficas y promedio
        q_serv = w_serv*float(condiciones.cp_tubo)*(t2_serv-t1_serv)
        q_proc = w_proc*float(condiciones.cp_tubo)*(t2_proc-t1_proc)

        qprom = numpy.mean([q_proc, q_serv])

        # Cálculo de la diferencia de temperatura media logarítmica
        flujo_contracorriente = ((t1_proc-t2_serv)-(t2_proc-t1_serv))/numpy.log(abs((t1_proc-t2_serv)/(t2_proc-t1_serv)))
        flujo_cocorriente = ((t1_proc-t1_serv)-(t2_proc-t2_serv))/numpy.log(abs((t1_proc-t1_serv)/(t2_proc-t2_serv)))

        # Cálculo del coeficiente global de transferencia de calor
        ua = qprom/flujo_contracorriente

        #Cálculo de la efectividad del intercambio de calor
        efectividad = (ua*flujo_contracorriente)/(float(condiciones.cp_tubo)*(t1_proc-t1_serv))
        
        # Cálculo de las unidades térmicas transferidas por unidad de área
        ntu = ua/float(condiciones.cp_tubo)

        # Cálculo del área de transferencia de calor 
        at = numpy.pi*float(intercambiador.diametro_ex_carcasa)*float(intercambiador.longitud_tubo)

        # Cálculo de la eficiencia del intercambiador de calor
        eficiencia = efectividad/ntu*100

        # Cálculo del porcentaje de ensuciamiento
        
        resultados = {
            'tprom_proc': tprom_proc,
            'tprom_serv': tprom_serv,
            'ntu': ntu,
            'ua': ua,
            'area_transferencia': at,
            'eficiencia': eficiencia,
            'efectividad': efectividad,
            'lmtd': flujo_contracorriente,
            'u': ua/at,
            'ensuciamiento': 'N/A'
        }

        return render(request, 'resultados_ntu.html', context={'resultados': resultados})

class ConsultaIntercambiadores(View):
    def get(self, request):
        return render(request, 'intercambiadores.html')

class Areas(View): # Esta vista se utiliza al seleccionar planta en el formulario
    def get(self, request, pk):
        return JsonResponse({'areas': Planta.objects.filter(planta__pk = pk)})
    
class Intercambiadores(View): # Esta vista se utiliza al seleccionar área en el formulario
    def get(self, request, pk):
        return JsonResponse({'intercambiadores': list(Intercambiador.objects.filter(area__pk = pk))})
    
class Fluidos(View):
    def get(self, request, pk): # La PK corresponde al intercambiador
        intercambiador = Intercambiador.objects.get(pk = pk)
        return JsonResponse({'interno': intercambiador.fluido_interno, 'externo': intercambiador.fluido_externo})