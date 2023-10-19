from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import *
from django.views.generic.list import ListView
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from thermo.chemical import search_chemical
from calculos.termodinamicos import calcular_cp
from calculos.evaluaciones import evaluacion_tubo_carcasa
from reportes.pdfs import generar_pdf
from calculos.unidades import transformar_unidades_temperatura, transformar_unidades_cp

# VISTAS PARA LOS INTERCAMBIADORES TUBO/CARCASA

class CrearIntercambiadorTuboCarcasa(LoginRequiredMixin, View):
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

            fluido_tubo = request.POST['fluido_tubo']
            fluido_carcasa = request.POST['fluido_carcasa']

            if(fluido_tubo.find('*') != -1):
                fluido_tubo = fluido_tubo.split('*')
                if(fluido_tubo[1].find('-') != -1):
                    quimico = search_chemical(fluido_tubo[1], cache=True)
                    fluido_tubo = Fluido.objects.create(nombre = fluido_tubo[0].upper(), cas = fluido_tubo[1], peso_molecular = quimico.MW)
            else:
                fluido_tubo = Fluido.objects.get(pk=fluido_tubo)

            if(fluido_carcasa.find('*') != -1):
                fluido_carcasa = fluido_carcasa.split('*')
                if(fluido_carcasa[1].find('-') != -1):
                    quimico = search_chemical(fluido_carcasa[1], cache=True)
                    fluido_carcasa = Fluido.objects.create(nombre = fluido_carcasa[0].upper(), cas = fluido_carcasa[1], peso_molecular = quimico.MW)
            else:
                fluido_carcasa = Fluido.objects.get(pk=fluido_carcasa)

            propiedades = PropiedadesTuboCarcasa.objects.create(
                intercambiador = intercambiador,
                area = float(request.POST['area']),
                area_unidad = Unidades.objects.get(pk=request.POST['unidad_area']),
                numero_tubos = float(request.POST['no_tubos']),
                longitud_tubos = float(request.POST['longitud_tubos']),
                longitud_tubos_unidad = Unidades.objects.get(pk=request.POST['longitud_tubos_unidad']),
                diametro_externo_tubos = float(request.POST['od_tubos']),
                diametro_interno_tubos = float(request.POST['id_carcasa']),
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

                pitch_tubos = float(request.POST['pitch']),
                unidades_pitch = Unidades.objects.get(pk=request.POST['unidades_pitch']),

                criticidad = request.POST['criticidad'],

                arreglo_serie = request.POST['arreglo_serie'],
                arreglo_paralelo = request.POST['arreglo_paralelo'],
                numero_pasos_tubo = request.POST['numero_pasos_tubo'],
                numero_pasos_carcasa = request.POST['numero_pasos_carcasa'],
                q =  float(request.POST['calor']),
                q_unidad = Unidades.objects.get(pk=request.POST['unidad_calor']),
                u =  float(request.POST['u']),
                u_unidad = Unidades.objects.get(pk=request.POST['unidad_u']),
                ensuciamiento = float(request.POST['ensuciamiento']),
                ensuciamiento_unidad = Unidades.objects.get(pk=request.POST['unidad_fouling'])
            )

            condiciones_diseno_tubo = CondicionesTuboCarcasa.objects.create(
                intercambiador = propiedades,
                lado = 'T',
                temp_entrada = request.POST['temp_in_tubo'],
                temp_salida = request.POST['temp_out_tubo'],
                temperaturas_unidad = Unidades.objects.get(pk=request.POST['unidad_temperaturas']),

                cambio_de_fase = request.POST['cambio_fase_tubo'],
                
                flujo_masico = float(request.POST['flujo_vapor_in_tubo']) + float(request.POST['flujo_liquido_in_tubo']),
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
                fluido_cp = request.POST['cp_tubo']
            )

            condiciones_diseno_carcasa = CondicionesTuboCarcasa.objects.create(
                intercambiador = propiedades,
                lado = 'C',
                temp_entrada = request.POST['temp_in_carcasa'],
                temp_salida = request.POST['temp_out_carcasa'],
                temperaturas_unidad =Unidades.objects.get(pk=request.POST['unidad_temperaturas']),

                cambio_de_fase = request.POST['cambio_fase_carcasa'],
                
                flujo_masico = float(request.POST['flujo_vapor_in_carcasa']) + float(request.POST['flujo_liquido_in_carcasa']),
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
                fluido_cp = request.POST['cp_carcasa']
            )

            messages.success(request, "El nuevo intercambiador ha sido registrado exitosamente.")

            return redirect(f"/intercambiadores/tubo_carcasa/{propiedades.pk}/")
    
    def get(self, request):
        self.context['complejos'] = Complejo.objects.all()
        self.context['plantas'] = Planta.objects.filter(complejo__pk=1)
        self.context['tipos'] = TiposDeTubo.objects.all()
        self.context['temas'] = Tema.objects.all()
        self.context['fluidos'] = Fluido.objects.all()
        self.context['unidades_temperaturas'] = Unidades.objects.filter(tipo = 'T')
        self.context['unidades_longitud'] = Unidades.objects.filter(tipo = 'L')
        self.context['unidades_area'] = Unidades.objects.filter(tipo = 'A')
        self.context['unidades_flujo'] = Unidades.objects.filter(tipo = 'f')
        self.context['unidades_presion'] = Unidades.objects.filter(tipo = 'P')
        self.context['unidades_ensuciamiento'] = Unidades.objects.filter(tipo = 'E')
        self.context['unidades_q'] = Unidades.objects.filter(tipo = 'Q').order_by('-simbolo')
        self.context['unidades_cp'] = Unidades.objects.filter(tipo = 'C')
        self.context['unidades_u'] = Unidades.objects.filter(tipo = 'u').order_by('-simbolo')

        if(self.context.get('error')):
            del(self.context['error'])
            
        if(self.context.get('previo')):
            del(self.context['previo'])            

        return render(request, 'tubo_carcasa/creacion.html', context=self.context)

class CrearEvaluacionTuboCarcasa(LoginRequiredMixin, View):
    context = {
        'titulo': "Evaluación Tubo Carcasa"
    }

    def post(self, request, pk):
        intercambiador = PropiedadesTuboCarcasa.objects.get(pk=pk)

        with transaction.atomic():
            print(request.POST)
            ti = (float(request.POST['temp_in_carcasa']))
            ts = (float(request.POST['temp_out_carcasa']))
            Ti = (float(request.POST['temp_in_tubo']))
            Ts = (float(request.POST['temp_out_tubo']))
            ft = (float(request.POST['flujo_tubo']))
            fc = (float(request.POST['flujo_carcasa']))
            nt = (float(request.POST['no_tubos']))
            cp_tubo =  transformar_unidades_cp([float(request.POST['cp_tubo'].replace(',','.'))], unidad=request.POST['unidad_cp'])[0]
            cp_carcasa =  transformar_unidades_cp([float(request.POST['cp_carcasa'].replace(',','.'))], unidad=request.POST['unidad_cp'])[0]
            unidad = int(request.POST['unidad_temperaturas'])
            unidad_flujo = int(request.POST['unidad_flujo'])

            resultados = evaluacion_tubo_carcasa(intercambiador, Ti, Ts, ti, ts, ft, fc, nt, cp_tubo, cp_carcasa, unidad_temp=unidad, unidad_flujo = unidad_flujo)

            print(resultados)

            EvaluacionesIntercambiador.objects.create(
                creado_por = request.user,
                intercambiador = intercambiador.intercambiador,
                condiciones = intercambiador.condicion_tubo(),
                metodo = request.POST['metodo'],
                nombre = request.POST['nombre'],

                # DATOS TEMPERATURAS
                temp_ex_entrada = request.POST['temp_in_carcasa'],
                temp_ex_salida = request.POST['temp_out_carcasa'],
                temp_in_entrada = request.POST['temp_in_tubo'],
                temp_in_salida = request.POST['temp_out_tubo'],
                temperaturas_unidad = Unidades.objects.get(pk=unidad),

                # DATOS FLUJOS
                flujo_masico_ex = request.POST['flujo_carcasa'],
                flujo_masico_in = request.POST['flujo_tubo'],
                unidad_flujo = Unidades.objects.get(pk=request.POST['unidad_flujo']),

                # DATOS PRESIONES
                caida_presion_in = request.POST['caida_tubo'],
                caida_presion_ex = request.POST['caida_carcasa'],
                unidad_presion = Unidades.objects.get(pk=request.POST['unidad_presion']),

                # DATOS DE SALIDA
                lmtd = resultados['lmtd'],
                area_transferencia = resultados['area'],
                u = round(resultados['u'], 4),
                ua = resultados['ua'],
                ntu = resultados['ntu'],
                efectividad = resultados['efectividad'],
                eficiencia = resultados['eficiencia'],
                ensuciamiento = resultados['factor_ensuciamiento'],
                q = resultados['q'],
                numero_tubos = request.POST['no_tubos'],

                # CP
                cp_tubo = request.POST['cp_tubo'],
                cp_carcasa = request.POST['cp_carcasa'],
                cp_unidad = Unidades.objects.get(pk=request.POST['unidad_cp'])
            )

        messages.success(request, "La nueva evaluación ha sido registrada exitosamente.")

        return redirect(f'/intercambiadores/tubo_carcasa/{intercambiador.pk}/')        

    def get(self, request, pk):
        context = self.context
        context['intercambiador'] = PropiedadesTuboCarcasa.objects.get(pk=pk)
        context['unidades_temperaturas'] = Unidades.objects.filter(tipo = 'T')
        context['unidades_flujo'] = Unidades.objects.filter(tipo = 'f')
        context['unidades_presion'] = Unidades.objects.filter(tipo = 'P')
        context['unidades_cp'] = Unidades.objects.filter(tipo = 'C')

        return render(request, 'tubo_carcasa/evaluaciones/creacion.html', context=context)

class EditarIntercambiadorTuboCarcasa(LoginRequiredMixin, View):
    context = {
        'titulo': "Edición de Intercambiador Tubo Carcasa"
    }

    def post(self, request, pk):
        print(request.POST)
        with transaction.atomic():
            fluido_tubo = request.POST['fluido_tubo']
            fluido_carcasa = request.POST['fluido_carcasa']

            if(fluido_tubo.find('*') != -1):
                fluido_tubo = fluido_tubo.split('*')
                if(fluido_tubo[1].find('-') != -1):
                    quimico = search_chemical(fluido_tubo[1], cache=True)
                    fluido_tubo = Fluido.objects.create(nombre = fluido_tubo[0].upper(), cas = fluido_tubo[1], peso_molecular = quimico.MW)
            elif fluido_tubo != '':
                fluido_tubo = Fluido.objects.get(pk=fluido_tubo)

            if(fluido_carcasa.find('*') != -1):
                fluido_carcasa = fluido_carcasa.split('*')
                if(fluido_carcasa[1].find('-') != -1):
                    quimico = search_chemical(fluido_carcasa[1], cache=True)
                    fluido_carcasa = Fluido.objects.create(nombre = fluido_carcasa[0].upper(), cas = fluido_carcasa[1], peso_molecular = quimico.MW)
            elif fluido_carcasa != '':
                fluido_carcasa = Fluido.objects.get(pk=fluido_carcasa)

            propiedades = PropiedadesTuboCarcasa.objects.get(pk=pk)
            propiedades.area = request.POST['area']
            propiedades.numero_tubos = request.POST['no_tubos']
            propiedades.longitud_tubos = float(request.POST['longitud_tubos'])
            propiedades.diametro_externo_tubos = request.POST['od_tubos']
            propiedades.diametro_interno_tubos = request.POST['id_carcasa']
            propiedades.tipo_tubo = TiposDeTubo.objects.get(pk=request.POST['tipo_tubo'])
            propiedades.pitch_tubos = request.POST['pitch']
            propiedades.unidades_pitch = Unidades.objects.get(pk=request.POST['unidades_pitch'])
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
            propiedades.fluido_tubo =  Fluido.objects.get(pk=request.POST['fluido_tubo']) if type(fluido_tubo) == str and fluido_tubo else fluido_tubo if type(fluido_tubo) == Fluido else None
            propiedades.fluido_carcasa = Fluido.objects.get(pk=request.POST['fluido_carcasa']) if type(fluido_carcasa) == str and fluido_carcasa else fluido_carcasa if type(fluido_carcasa) == Fluido else None
            propiedades.area_unidad = Unidades.objects.get(pk=request.POST['unidad_area'])
            propiedades.longitud_tubos_unidad = Unidades.objects.get(pk=request.POST['longitud_tubos_unidad'])
            propiedades.diametro_tubos_unidad = Unidades.objects.get(pk=request.POST['unidad_diametros'])
            propiedades.q_unidad = Unidades.objects.get(pk=request.POST['unidad_q'])
            propiedades.u_unidad = Unidades.objects.get(pk=request.POST['unidad_u'])
            propiedades.ensuciamiento_unidad = Unidades.objects.get(pk=request.POST['unidad_fouling'])

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
            condiciones_tubo.fluido_cp = request.POST['cp_tubo']
            condiciones_tubo.unidad_cp = Unidades.objects.get(pk=request.POST['unidad_cp'])
            condiciones_tubo.temperaturas_unidad = Unidades.objects.get(pk=request.POST['unidad_temperaturas'])
            condiciones_tubo.unidad_presion = Unidades.objects.get(pk=request.POST['unidad_presiones'])
            condiciones_tubo.flujos_unidad = Unidades.objects.get(pk=request.POST['unidad_flujos'])

            if(fluido_tubo != ''):
                condiciones_tubo.fluido_etiqueta = fluido_tubo[0] if type(fluido_tubo) != Fluido else None

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
            condiciones_carcasa.fluido_cp = request.POST['cp_carcasa']
            condiciones_carcasa.unidad_cp = Unidades.objects.get(pk=request.POST['unidad_cp'])
            condiciones_carcasa.temperaturas_unidad = Unidades.objects.get(pk=request.POST['unidad_temperaturas'])
            condiciones_carcasa.unidad_presion = Unidades.objects.get(pk=request.POST['unidad_presiones'])
            condiciones_carcasa.flujos_unidad = Unidades.objects.get(pk=request.POST['unidad_flujos'])
            
            if(fluido_carcasa != ''):
                print(fluido_carcasa)
                condiciones_carcasa.fluido_etiqueta = fluido_carcasa[0] if type(fluido_carcasa) != Fluido else None

            condiciones_carcasa.save()

            intercambiador = Intercambiador.objects.get(pk=propiedades.intercambiador.pk)
            intercambiador.tag = request.POST['tag']
            intercambiador.fabricante = request.POST['fabricante']
            intercambiador.servicio = request.POST['servicio']
            intercambiador.arreglo_flujo = request.POST['flujo']
            intercambiador.save()

        messages.success(request, "Se han editado las características del intercambiador exitosamente.")

        return redirect(f"/intercambiadores/tubo_carcasa/{propiedades.pk}/")
    
    def get(self, request, pk):
        self.context['intercambiador'] = PropiedadesTuboCarcasa.objects.get(pk=pk)
        self.context['complejos'] = Complejo.objects.all()
        self.context['tipos'] = TiposDeTubo.objects.all()
        self.context['plantas'] = Planta.objects.filter(complejo__pk=1)
        self.context['tipos'] = TiposDeTubo.objects.all()
        self.context['temas'] = Tema.objects.all()
        self.context['fluidos'] = Fluido.objects.all()
        self.context['unidades_temperaturas'] = Unidades.objects.filter(tipo = 'T')
        self.context['unidades_longitud'] = Unidades.objects.filter(tipo = 'L')
        self.context['unidades_area'] = Unidades.objects.filter(tipo = 'A')
        self.context['unidades_flujo'] = Unidades.objects.filter(tipo = 'f')
        self.context['unidades_presion'] = Unidades.objects.filter(tipo = 'P')
        self.context['unidades_ensuciamiento'] = Unidades.objects.filter(tipo = 'E')
        self.context['unidades_q'] = Unidades.objects.filter(tipo = 'Q')
        self.context['unidades_cp'] = Unidades.objects.filter(tipo = 'C')
        self.context['unidades_u'] = Unidades.objects.filter(tipo = 'u')

        return render(request, 'tubo_carcasa/edicion.html', context=self.context)

class ConsultaEvaluacionesTuboCarcasa(LoginRequiredMixin, ListView):
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
        new_context = EvaluacionesIntercambiador.objects.filter(intercambiador=PropiedadesTuboCarcasa.objects.get(pk=self.kwargs['pk']).intercambiador)
        desde = self.request.GET.get('desde', '')
        hasta = self.request.GET.get('hasta', '')
        condiciones = self.request.GET.get('condiciones', '')
        metodo = self.request.GET.get('metodo', '')
        nombre = self.request.GET.get('nombre', '')

        if(desde != ''):
            new_context = new_context.filter(
                fecha__gte = desde
            )

        if(hasta != ''):
            new_context = new_context.filter(
                fecha__lte=hasta
            )

        if(metodo != ''):
            new_context = new_context.filter(
                metodo = metodo
            )

        if(nombre != ''):
            new_context = new_context.filter(
                nombre__icontains = nombre
            )

        return new_context

class ConsultaTuboCarcasa(LoginRequiredMixin, ListView):
    model = PropiedadesTuboCarcasa
    template_name = 'tubo_carcasa/consulta.html'
    paginate_by = 10

    def post(self, request, **kwargs):
        if(request.POST['tipo'] == 'pdf'):
            return generar_pdf(request, self.get_queryset(),"Reporte de Intercambiadores Tubo/Carcasa", "intercambiadores_tubo_carcasa")
        else:
            from reportes.xlsx import reporte_tubo_carcasa
            response = reporte_tubo_carcasa(self.get_queryset(), request)
            response['Content-Disposition'] = 'attachment; filename="reporte_tubo_carcasa.xlsx"'
            return response
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "SIEVEP - Consulta de Intercambiadores de Tubo/Carcasa"
        context['complejos'] = Complejo.objects.all()

        if(self.request.GET.get('complejo')):
            context['plantas'] = Planta.objects.filter(complejo= self.request.GET.get('complejo'))

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

class ConsultaVacia(LoginRequiredMixin, View):
    template_name = 'pantalla_vacia.html'
      
    def get(self, request, tipo):
        return render(request, self.template_name, {'tipo': tipo, 'titulo': f'Consulta de Intercambiadores de Calor {tipo}'})

class SeleccionTipo(LoginRequiredMixin, View):
    context = {
        'titulo': "SIEVEP - Selección de Tipo de Intercambiador"
    }

    def get(self, request):
        return render(request, 'seleccion_tipo.html', context=self.context)

# VISTAS AJAX

class EvaluarTuboCarcasa(LoginRequiredMixin, View):
    def get(self, request, pk):
        print(request.GET)
        intercambiador = PropiedadesTuboCarcasa.objects.get(id = pk)

        ti = (float(request.GET['temp_in_carcasa'].replace(',','.')))
        ts = (float(request.GET['temp_out_carcasa'].replace(',','.')))
        Ti = (float(request.GET['temp_in_tubo'].replace(',','.')))
        Ts = (float(request.GET['temp_out_tubo'].replace(',','.')))
        ft = (float(request.GET['flujo_tubo'].replace(',','.')))
        fc = (float(request.GET['flujo_carcasa'].replace(',','.')))
        nt = (float(request.GET['no_tubos']))
        cp_tubo = transformar_unidades_cp([float(request.GET['cp_tubo'].replace(',','.'))], unidad=request.GET['unidad_cp'])[0]
        cp_carcasa = transformar_unidades_cp([float(request.GET['cp_carcasa'].replace(',','.'))], unidad=request.GET['unidad_cp'])[0]
        unidad = int(request.GET['unidad'])
        unidad_flujo = int(request.GET['unidad_flujo'])

        print(ti, ts, Ti, Ts, ft, fc, cp_tubo, cp_carcasa)

        res = evaluacion_tubo_carcasa(intercambiador, Ti, Ts, ti, ts, ft, fc, nt, cp_tubo, cp_carcasa, unidad_temp=unidad, unidad_flujo = unidad_flujo)
        print(res)
        return JsonResponse(res)

class ConsultaCAS(LoginRequiredMixin, View):
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

class ConsultaCP(LoginRequiredMixin, View):
    def get(self, request):
        fluido = request.GET['fluido']
        t1,t2 = float(request.GET['t1']), float(request.GET['t2'])
        unidad = int(request.GET['unidad'])
        unidad_salida = int(request.GET.get('unidad_salida')) if request.GET.get('unidad_salida') else 29

        print(unidad_salida)
        print(request.GET.get('unidad_salida'))

        t1,t2 = transformar_unidades_temperatura([t1,t2], unidad=unidad)

        if(fluido != ''):
            if(fluido.find('*') != -1):
                cas = fluido.split('*')[1]

                if(cas.find('-') == -1):
                    return JsonResponse({'cp': fluido.split('*')[1]})
            else:
                cas = Fluido.objects.get(pk = fluido).cas
        
            cp = calcular_cp(cas, t1, t2, unidad_salida)

            return JsonResponse({'cp': cp})
        else:
            return JsonResponse({'cp': ''})
        
class ConsultaGraficasEvaluacion(LoginRequiredMixin, View):
    def get(self, request, pk):
        evaluaciones = EvaluacionesIntercambiador.objects.filter(intercambiador = PropiedadesTuboCarcasa.objects.get(pk=pk).intercambiador).order_by('fecha')
        
        if(request.GET.get('desde')):
            evaluaciones = evaluaciones.filter(fecha__gte = request.GET.get('desde'))

        if(request.GET.get('hasta')):
            evaluaciones = evaluaciones.filter(fecha__lte = request.GET.get('hasta'))
        
        print(evaluaciones)

        return JsonResponse(list(evaluaciones.values('fecha','efectividad', 'u', 'ensuciamiento','eficiencia', 'caida_presion_in', 'caida_presion_ex'))[:15], safe=False)
