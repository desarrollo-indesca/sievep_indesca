from django.shortcuts import render
from django.views import View
from .models import *
from django.http import JsonResponse
import numpy

# VISTAS PARA LOS INTERCAMBIADORES TUBO/CARCASA

class CrearSimulacionTuboCarcasa(View):
    context = {
        'titulo': "Simulación Tubo Carcasa"
    }
    def get(self, request, pk):
        return render(request, 'tubo_carcasa/simulaciones/creacion.html', context=self.context)

class ConsultaSimulacionesTuboCarcasa(View):
    context = {
        'titulo': "PEQUIVEN - Intercambiadores de Tubo/Carcasa",
        'numeros': [1,2,3,4,5,6,7,8,9,10]
    }

    def get(self, request, pk):
        return render(request, 'tubo_carcasa/simulaciones/consulta.html', context=self.context)

class ConsultaTuboCarcasa(View):
    context = {
        'titulo': "PEQUIVEN - Intercambiadores de Tubo/Carcasa",
        'numeros': [1,2,3,4,5,6,7,8,9,10]
    }

    def get(self, request):
        return render(request, 'tubo_carcasa/consulta.html', context=self.context)

# VISTAS GENERALES PARA LOS INTERCAMBIADORES DE CALOR

class SeleccionTipo(View):
    context = {
        'titulo': "PEQUIVEN - Selección de Tipo de Intercambiador"
    }

    def get(self, request):
        return render(request, 'seleccion_tipo.html', context=self.context)

# ESTAS YA NO SE USARÁN

class Simulaciones(View):
    context = {
        'titulo': "PEQUIVEN - Simulaciones de Intercambiadores"
    }

    def get(self, request):
        return render(request, 'simulaciones.html', context=self.context)
    
class FormularioSimulaciones(View):
    context = {
        'titulo': "PEQUIVEN - Simulaciones de Intercambiadores"
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