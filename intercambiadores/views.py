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
        return render(request, 'formulario.html', context=self.context)
    
    def post(self, request):
        pass

class Areas(View): # Esta vista se utiliza al seleccionar planta en el formulario
    def get(self, request, pk):
        return JsonResponse({'areas': Area.objects.filter(planta__pk = pk)})
    
class Intercambiadores(View): # Esta vista se utiliza al seleccionar área en el formulario
    def get(self, request, pk):
        return JsonResponse({'intercambiadores': Intercambiador.objects.filter(area__pk = pk)})