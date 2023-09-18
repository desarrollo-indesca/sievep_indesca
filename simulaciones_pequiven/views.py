from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login

class Bienvenida(View):
    context = {
        'titulo': "PEQUIVEN - Simulaciones"
    }
    
    def get(self, request):
        if(request.user.is_authenticated):
            return render(request, 'bienvenida.html', context=self.context)
        else:
            return render(request, 'usuarios/login.html', context=self.context)
        
    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            pass