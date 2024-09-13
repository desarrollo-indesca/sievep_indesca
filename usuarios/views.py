from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from usuarios.forms import RespuestaForm
from usuarios.models import *

# Create your views here.

class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Resumen:
        Mixin para verificar que un usuario sea superusuario, para permitir o denegar su acceso.
    
    Métodos:
        test_func(self, request)
            Función heredada de UserPassesTestMixin, verifica si el usuario es un superusuario o no.
    """
    def test_func(self):
        return self.request.user.is_superuser

class ConsultaUsuarios(SuperUserRequiredMixin, ListView):
    """
    Resumen:
        Vista de consulta de usuarios. Contiene la lógica de filtrado y paginación
        para los usuarios del sistema. Únicamente pueden acceder superusuarios.

    Atributos:
        model: Model
            Modelo (User) de la consulta.

        template_name: str
            Nombre de la plantilla a renderizar.

        paginate_by: int
            Número de registros de usuarios que se pueden ver por página.
    
    Métodos:
        get_context_data(self, **kwargs)
            Rellena los datos contextuales de la vista para el filtrado.

        def get_queryset(self)
            Filtra los usuarios de acuerdo a los datos de filtrado proporcionados.
    """

    model = get_user_model()
    template_name = 'usuarios/consulta.html'
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

class CrearNuevoUsuario(SuperUserRequiredMixin, View):
    """
    Resumen:
        Vista de creación de un nuevo usuario. 
        Únicamente pueden acceder superusuarios.

    Atributos:
        modelo: Model
            Modelo (User) de la creación.

        context: dict
            Diccionario que contiene la data contextual de la vista.
            Incluye inicialmente el título.
    
    Métodos:
        validar(self, data)
            Contiene la lógica de validación para la creación de un usuario.

        def post(self, request)
            Contiene la lógica de almacenamiento de un nuevo usuario.

        def get(self, request)
            Contiene la lógica de renderizado del formulario.
    """

    context = {
        'titulo': "Registro de Nuevo Usuario"
    }

    modelo = get_user_model()

    def validar(self, data):
        errores = []
        if(self.modelo.objects.filter(email = data['correo'].lower()).exists()):
            errores.append("Ya existe un usuario con ese correo registrado.")

        if(self.modelo.objects.filter(first_name = data['nombre'].title()).exists()):
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
                    username = request.POST['correo'].lower(),
                    first_name = request.POST['nombre'].title(),
                    password = make_password(request.POST['password']),
                    is_superuser = 'superusuario' in request.POST.keys()
                )

                messages.success(request, "Se ha registrado al nuevo usuario correctamente.")

                return redirect("/usuarios/")
        else:
            return render(request, 'usuarios/creacion.html', {'errores': errores, 'previo': request.POST, **self.context})
    
    def get(self, request):
        return render(request, 'usuarios/creacion.html', self.context)

class EditarUsuario(SuperUserRequiredMixin, View):
    """
    Resumen:
        Vista de edición un usuario existente.
        Los usuarios pueden activarse y desactivarse por esta vía.
        Únicamente pueden acceder superusuarios.

    Atributos:
        modelo: Model
            Modelo (User) de la creación.

        context: dict
            Diccionario que contiene la data contextual de la vista.
            Incluye inicialmente el título.
    
    Métodos:
        validar(self, data)
            Contiene la lógica de validación para la edición de un usuario.

        def post(self, request)
            Contiene la lógica de actualización de un usuario editado.

        def get(self, request)
            Contiene la lógica de renderizado del formulario.
    """

    context = {
        'titulo': "Editar Usuario"
    }

    modelo = get_user_model()

    def validar(self, data):
        errores = []
        if(self.modelo.objects.filter(email = data['correo'].lower()).exclude(pk=self.kwargs['pk']).exists()):
            errores.append("Ya existe un usuario con ese correo registrado.")

        if(self.modelo.objects.filter(first_name = data['nombre'].title()).exclude(pk=self.kwargs['pk']).exists()):
            errores.append("Ya existe un usuario con ese nombre registrado. Añada una característica diferenciadora.")

        return errores

    def post(self, request, pk): # Envío de Formulario de Creación
        errores = self.validar(request.POST)
        if(len(errores) == 0):
            with transaction.atomic():
                usuario = self.modelo.objects.get(pk=pk)
                usuario.email = request.POST['correo'].lower()
                usuario.username = request.POST['correo'].lower()
                usuario.first_name =  request.POST['nombre'].title()
                usuario.is_active = 'activo' in request.POST.keys()
                usuario.is_superuser = 'superusuario' in request.POST.keys()
                usuario.save()

                messages.success(request, "Se han registrado los cambios.")

                return redirect("/usuarios/")
        else:
            return render(request, 'usuarios/creacion.html', {'errores': errores, 'previo': request.POST, 'edicion': True, **self.context})
    
    def get(self, request, pk):
        usuario = self.modelo.objects.get(pk=pk)
        previo = {
            'nombre': usuario.first_name,
            'correo': usuario.email,
            'superusuario': usuario.is_superuser,
            'activo': usuario.is_active
        }

        return render(request, 'usuarios/creacion.html', context={'previo': previo, 'edicion': True, **self.context})

class CambiarContrasena(SuperUserRequiredMixin, View):
    """
    Resumen:
        Vista del formulario de cambio de contraseña de un usuario existente. 
        Únicamente pueden acceder superusuarios.

    Atributos:
        modelo: Model
            Modelo (User) de la creación.

        context: dict
            Diccionario que contiene la data contextual de la vista.
            Incluye inicialmente el título.
    
    Métodos:
        validar(self, data)
            Contiene la lógica de validación para el cambio de contraseña.

        def post(self, request)
            Contiene la lógica de actualización de contraseña para el usuario.

        def get(self, request)
            Contiene la lógica de renderizado del formulario.
    """

    context = {
        'titulo': "Cambiar Contraseña"
    }

    modelo = get_user_model()

    def validar(self, data):
        errores = []

        if(len(data['password']) < 8):
            errores.append("La contraseña debe contar con al menos 8 caracteres.")

        return errores

    def post(self, request, pk): # Envío de Formulario de Creación
        errores = self.validar(request.POST)
        if(len(errores) == 0):
            with transaction.atomic():
                usuario = self.modelo.objects.get(pk=pk)
                usuario.password = make_password(request.POST['password'])
                usuario.save()

                messages.success(request, "Se han registrado los cambios correctamente.")

                return redirect("/usuarios/")
        else:
            return render(request, 'cambiar_contrasena.html', {'errores': errores, **self.context})
    
    def get(self, request, pk):
        usuario = self.modelo.objects.get(pk=pk)

        return render(request, 'cambiar_contrasena.html', context={'usuario': usuario, 'edicion': True, **self.context})

class EncuestaSatisfaccion(LoginRequiredMixin, View):
    """
    Resumen:
        Vista del formulario de encuesta de satisfacción.

    Método:
        get_context_data(self, **kwargs)
            Contiene la lógica de renderizado del formulario.

        get(self, request)
            Contiene la lógica de renderizado del formulario.
    """
    def get_context_data(self, **kwargs):
        encuesta = Encuesta.objects.first()
        forms = []

        request = self.request.POST

        for seccion in encuesta.secciones.all():
            forms.append({
                'seccion': seccion,
                'preguntas': [
                    {
                        'pregunta': pregunta,
                        'form': RespuestaForm(request if len(request) else None, prefix=f"pregunta-{pregunta.id}", initial={'pregunta': pregunta})
                    } for pregunta in seccion.preguntas.all()
                ]
            })

        return {
            'forms': forms,
            'encuesta': encuesta,
            'titulo': 'Encuesta de Satisfacción del SIEVEP'
        }

    def post(self, request):
        with transaction.atomic():
            encuesta = Encuesta.objects.first()
            envio = Envio.objects.create(encuesta=encuesta, usuario=request.user)

            for seccion in encuesta.secciones.all():
                for pregunta in seccion.preguntas.all():
                    form = RespuestaForm(request.POST, prefix=f"pregunta-{pregunta.id}")
                    if(form.is_valid()):
                        form.instance.envio = envio
                        form.save()
                    else:
                        print(form.errors)
                    
                    return render(request, 'form_encuesta.html', self.get_context_data())

        return redirect("/")

    def get(self, request):
        return render(request, 'form_encuesta.html', self.get_context_data())