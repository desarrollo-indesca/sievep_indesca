from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.

class FormularioSimulacion(View):
    context = {
        'titulo': "PEQUIVEN - Simulaciones de Intercambiadores"
    }

    def get(self, request):
        return render(request, 'simulaciones.html', context=self.context)