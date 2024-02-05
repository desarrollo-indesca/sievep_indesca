from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.

class SeleccionTipo(LoginRequiredMixin, View):
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