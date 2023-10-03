from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.views.generic.list import ListView
from django.db import transaction
import numpy
import os
from thermo.chemical import search_chemical
from thermo.heat_capacity import HeatCapacityLiquid, HeatCapacityGas, HeatCapacitySolid
from reportes.pdfs import generar_pdf

# VISTAS PARA LOS INTERCAMBIADORES TUBO/CARCASA

class CrearIntercambiadorTuboCarcasa(View):
    context = {
        'titulo': "Creación de Intercambiador Tubo Carcasa"
    }

    def post(self, request): # Envío de Formulario de Creación
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

            print(request.POST)

            fluido_tubo = request.POST['fluido_tubo']
            fluido_carcasa = request.POST['fluido_carcasa']

            print(fluido_carcasa)
            print(fluido_tubo)

            if(fluido_tubo.find('*') != -1):
                fluido_tubo = fluido_tubo.split('*')
                if(fluido_tubo[1].find('-') != -1):
                    quimico = search_chemical(fluido_tubo[1], cache=True)
                    fluido_tubo = Fluido.objects.create(nombre = fluido_tubo[0].upper(), cas = fluido_tubo[1], peso_molecular = quimico.MW, estado = 'L')
            else:
                fluido_tubo = Fluido.objects.get(pk=fluido_tubo)

            if(fluido_carcasa.find('*') != -1):
                fluido_carcasa = fluido_carcasa.split('*')
                if(fluido_carcasa[1].find('-') != -1):
                    quimico = search_chemical(fluido_carcasa[1], cache=True)
                    fluido_carcasa = Fluido.objects.create(nombre = fluido_carcasa[0].upper(), cas = fluido_carcasa[1], peso_molecular = quimico.MW, estado = 'L')
            else:
                fluido_carcasa = Fluido.objects.get(pk=fluido_carcasa)

            print(fluido_carcasa)
            print(fluido_tubo)

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

                fluido_carcasa = Fluido.objects.get(pk=request.POST['fluido_carcasa']) if type(fluido_carcasa) == str else fluido_carcasa if type(fluido_carcasa) == Fluido else None,
                material_carcasa = request.POST['material_carcasa'],
                conexiones_entrada_carcasa = request.POST['conexiones_entrada_carcasa'],
                conexiones_salida_carcasa = request.POST['conexiones_salida_carcasa'],
                
                fluido_tubo = Fluido.objects.get(pk=request.POST['fluido_tubo']) if type(fluido_tubo) == str else fluido_tubo if type(fluido_tubo) == Fluido else None,
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

                fouling = request.POST['fouling_tubo'],
                fluido_etiqueta = fluido_tubo[0] if type(fluido_tubo) != Fluido else None,
                fluido_cp = fluido_tubo[1] if type(fluido_tubo) != Fluido else calcular_cp(propiedades.fluido_tubo.cas, request.POST['temp_in_tubo'], request.POST['temp_out_tubo'], 'C') 
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

                fouling = request.POST['fouling_carcasa'],
                fluido_etiqueta = fluido_carcasa[0] if type(fluido_carcasa) != Fluido else None,
                fluido_cp = fluido_carcasa[1] if type(fluido_carcasa) != Fluido else None 
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
            propiedades.ensuciamiento = request.POST['ensuciamiento'] if request.POST['ensuciamiento'] != '' else None
            propiedades.u = request.POST['u'] if request.POST['u'] != '' else None
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

class ConsultaEvaluacionesTuboCarcasa(ListView):
    model = EvaluacionesIntercambiador
    template_name = 'tubo_carcasa/evaluaciones/consulta.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "SIEVEP - Consulta de Evaluaciones"
        context['intercambiador'] = PropiedadesTuboCarcasa.objects.get(pk=self.kwargs['pk'])

        context['nombre'] = self.request.GET.get('nombre', '')
        context['desde'] = self.request.GET.get('desde', '')
        context['hasta'] = self.request.GET.get('hasta')
        context['metodo'] = self.request.GET.get('metodo','')
        context['condiciones'] = self.request.GET.get('condiciones', '')

        return context
    
    def get_queryset(self):
        new_context = EvaluacionesIntercambiador.objects.filter(intercambiador__pk=PropiedadesTuboCarcasa.objects.get(pk=self.kwargs['pk']).intercambiador.pk)
        desde = self.request.GET.get('desde', '')
        hasta = self.request.GET.get('hasta', '')
        condiciones = self.request.GET.get('condiciones', '')
        metodo = self.request.GET.get('metodo', '')
        nombre = self.request.GET.get('nombre', '')

        if(desde != ''):
            new_context = self.model.objects.filter(
                fecha__gte = desde
            )

        if(hasta != ''):
            new_context = new_context.filter(
                fecha__lte=hasta
            )

        if(metodo != ''):
            new_context = self.model.objects.filter(
                metodo = metodo
            )

        if(nombre != ''):
            new_context = self.model.objects.filter(
                nombre__icontains = nombre
            )

        return new_context

class ConsultaTuboCarcasa(ListView):
    model = PropiedadesTuboCarcasa
    template_name = 'tubo_carcasa/consulta.html'
    paginate_by = 10

    def post(self, request, **kwargs):
        # TODO
        if(request.POST['tipo'] == 'pdf'):
            return generar_pdf(request, self.get_queryset(),"Reporte de Intercambiadores Tubo/Carcasa", "intercambiadores_tubo_carcasa")
        else:
            from reportes.xlsx import reporte_tubo_carcasa
            archivo = reporte_tubo_carcasa(self.get_queryset(), request)
            with open(archivo, "rb") as excel:
                data = excel.read()
            os.remove(archivo)
            response = HttpResponse(data, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="reporte_tubo_carcasa.xlsx"'
            return response
            
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

class ConsultaCAS(View):
    def get(self, request):
        cas = request.GET['cas']

        if(Fluido.objects.filter(cas = cas).exists()):
            estado = 2
            fluido = Fluido.objects.get(cas = cas).nombre
        else:
            estado = 1

        if(estado != 2):
            try:
                quimico = search_chemical(cas, cache=True)
                fluido = quimico.common_name
            except Exception as e:
                estado = 3
                fluido = ''

        return JsonResponse({'nombre': fluido, 'estado': estado})

class ConsultaCP(View):
    def get(self, request):
        fluido = request.GET['fluido']
        t1,t2 = request.GET['t1'], request.GET['t2']

        if(fluido.find('*') != -1):
            cas = fluido.split('*')[0]

            if(cas.find('-') == -1):
                return JsonResponse({'cp': ''})
        else:
            cas = Fluido.objects.get(pk = fluido).cas
        
        cp = calcular_cp(cas, t1, t2, 'C')

        print(cp)

        return JsonResponse({'cp': cp})

# Funciones Auxiliares de Cálculos

def calcular_cp(fluido, t1, t2, unidad = 'K'):
    if(unidad == 'C'):
        t1 = float(t1)
        t1 += 273.15

        t2 = float(t2)
        t2 += 273.15

    t = numpy.mean([t1, t2])
    quimico = HeatCapacityLiquid(fluido)

    if(t > quimico.Tmax):
        quimico = HeatCapacityGas(fluido)
    elif(t < quimico.Tmin):
        quimico = HeatCapacitySolid(fluido)

    cp = quimico.calculate(t, 'HEOS_FIT')

    return round(cp, 4)