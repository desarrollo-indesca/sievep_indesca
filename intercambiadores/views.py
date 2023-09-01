from django.shortcuts import render
from django.views import View
from .models import *
from django.http import JsonResponse
import numpy

# Create your views here.

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
        pass

class Areas(View): # Esta vista se utiliza al seleccionar planta en el formulario
    def get(self, request, pk):
        return JsonResponse({'areas': Area.objects.filter(planta__pk = pk)})
    
class Intercambiadores(View): # Esta vista se utiliza al seleccionar área en el formulario
    def get(self, request, pk):
        return JsonResponse({'intercambiadores': list(Intercambiador.objects.filter(area__pk = pk).values('id','codigo','diametro_ex_carcasa','diametro_ex_tubos', 'longitud_tubo'))})
    
class Fluidos(View):
    def get(self, request, pk): # La PK corresponde al intercambiador
        intercambiador = Intercambiador.objects.get(pk = pk)
        return JsonResponse({'fluidos_servicio': list(Fluido.objects.filter(pk__in = intercambiador.condiciones.values('fluido_servicio')).values('id','nombre')), 
                             'fluidos_interno': list(Fluido.objects.filter(pk__in = intercambiador.condiciones.values('fluido_interno')).values('id','nombre'))})