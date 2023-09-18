from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, get_user_model


class Bienvenida(View):
    context = {
        'titulo': "PEQUIVEN - Simulaciones"
    }
    
    def get(self, request):
        print(request.user)
        if(request.user.is_authenticated):
            return render(request, 'bienvenida.html', context=self.context)
        else:
            return render(request, 'usuarios/login.html', context=self.context)
        
    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                user = user
            else:
                user = None
            
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            self.context['errores'] = 'Datos Incorrectos.'
            return redirect('/')
        
class CerrarSesion(View):
    def get(self, request):
        logout(request)
        return redirect('/')