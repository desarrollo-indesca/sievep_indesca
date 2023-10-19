from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.hashers import make_password

# Create your views here.

class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class ConsultaUsuarios(SuperUserRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'consulta.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "SIEVEP - Consulta de Usuarios"

        context['nombre'] = self.request.GET.get('nombre', '')
        context['correo'] = self.request.GET.get('correo', '')
        context['superusuario'] = self.request.GET.get('superusuario')
        context['activo'] = self.request.GET.get('activo','')

        return context
    
    def get_queryset(self):
        new_context = self.model.objects.all()
        nombre = self.request.GET.get('nombre', '')
        correo = self.request.GET.get('correo', '')
        superusuario = self.request.GET.get('superusuario', '')
        activo = self.request.GET.get('activo', '')

        if(nombre != ''):
            new_context = new_context.filter(
                first_name__icontains = nombre
            )

        if(correo != ''):
            new_context = new_context.filter(
                email__icontains=correo
            )

        if(superusuario != ''):
            new_context = new_context.filter(
                is_superuser = int(superusuario)
            )

        if(activo != ''):
            new_context = new_context.filter(
                is_active = activo
            )

        return new_context.order_by('first_name','last_name')

class CrearNuevoUsuario(LoginRequiredMixin, View):
    context = {
        'titulo': "Registro de Nuevo Usuario"
    }

    modelo = get_user_model()

    def validar(self, data):
        errores = []
        if(self.modelo.objects.filter(email = data['correo'].lower()).exists()):
            errores.append("Ya existe un usuario con ese correo registrado.")

        if(self.modelo.objects.filter(username = data['nombre'].title()).exists()):
            errores.append("Ya existe un usuario con ese nombre registrado. Añada una característica diferenciadora.")

        if(len(data['password']) < 8):
            errores.append("La contraseña debe tener 8 caracteres.")

        return errores

    def post(self, request): # Envío de Formulario de Creación
        errores = self.validar(request.POST)
        if(len(errores) == 0):
            with transaction.atomic():
                self.modelo.objects.create(
                    email = request.POST['correo'].lower(),
                    username = request.POST['nombre'].title(),
                    password = make_password(request.POST['password']),
                    is_superuser = 'superusuario' in request.POST.keys()
                )

                request.session['mensaje'] = "Se ha registrado al nuevo usuario correctamente."

                return redirect("/usuarios/")
        else:
            return render(request, 'creacion.html', {'errores': errores, 'previo': request.POST})
    
    def get(self, request):
        return render(request, 'creacion.html')

class EditarUsuario(LoginRequiredMixin, View):
    context = {
        'titulo': "Editar Usuario"
    }

    modelo = get_user_model()

    def validar(self, data):
        errores = []
        if(self.modelo.objects.filter(email = data['correo'].lower()).exclude(pk=self.kwargs['pk']).exists()):
            errores.append("Ya existe un usuario con ese correo registrado.")

        if(self.modelo.objects.filter(username = data['nombre'].title()).exclude(pk=self.kwargs['pk']).exists()):
            errores.append("Ya existe un usuario con ese nombre registrado. Añada una característica diferenciadora.")

        return errores

    def post(self, request, pk): # Envío de Formulario de Creación
        errores = self.validar(request.POST)
        if(len(errores) == 0):
            with transaction.atomic():
                usuario = self.modelo.objects.get(pk=pk)
                usuario.email = request.POST['correo'].lower()
                usuario.username =  request.POST['nombre'].title()
                usuario.is_active = 'activo' in request.POST.keys()
                usuario.is_superuser = 'superusuario' in request.POST.keys()
                usuario.save()

                request.session['mensaje'] = "Se han registrado los cambios."

                return redirect("/usuarios/")
        else:
            return render(request, 'creacion.html', {'errores': errores, 'previo': request.POST, 'edicion': True})
    
    def get(self, request, pk):
        usuario = self.modelo.objects.get(pk=pk)
        previo = {
            'nombre': usuario.get_username(),
            'correo': usuario.email,
            'superusuario': usuario.is_superuser,
            'activo': usuario.is_active
        }

        return render(request, 'creacion.html', context={'previo': previo, 'edicion': True})
