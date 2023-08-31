from django.views import View
from django.shortcuts import render

class Bienvenida(View):
    context = {
        'titulo': "PEQUIVEN - Simulaciones"
    }
    
    def get(self, request):
        return render(request, 'bienvenida.html', context=self.context)