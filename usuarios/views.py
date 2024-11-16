from django.db.models.query import QuerySet, Q, Prefetch
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from usuarios.forms import RespuestaForm
from django.http import JsonResponse
from usuarios.models import *
from intercambiadores.models import Complejo

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

class EditorRequiredMixin(UserPassesTestMixin):
    """
    Resumen:
        Mixin para verificar que un usuario pertenezca a un grupo, para permitir o denegar su acceso.
    
    Métodos:
        test_func(self, request)
            Función heredada de UserPassesTestMixin, verifica si el usuario pertenece al grupo o no.
    """
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='editor').exists()

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
        'titulo': "Registro de Nuevo Usuario",
        'complejos': Complejo.objects.prefetch_related('plantas').all()
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
                usuario = self.modelo.objects.create(
                    email = request.POST['correo'].lower(),
                    username = request.POST['correo'].lower(),
                    first_name = request.POST['nombre'].title(),
                    password = make_password(request.POST['password']),
                    is_superuser = 'superusuario' in request.POST.keys()
                )

                # Delete all current plants for this user
                usuario.usuario_planta.all().delete()

                # Assign plants according to the marked checkboxes
                ids = []
                for key in request.POST.keys():
                    if key.startswith('planta-'):
                        print(key)
                        planta_id = key.split('-')[1]
                        ids.append(planta_id)
                
                plantas = Planta.objects.filter(pk__in = ids)

                for planta in plantas:
                    planta_accesible = PlantaAccesible.objects.create(planta=planta, usuario=usuario)
                    planta_accesible.crear = f"crear-{planta.pk}" in request.POST.keys()
                    planta_accesible.edicion = f"editar-{planta.pk}" in request.POST.keys()
                    planta_accesible.edicion_instalacion = f"instalacion-{planta.pk}" in request.POST.keys()
                    planta_accesible.duplicacion = f"duplicacion-{planta.pk}" in request.POST.keys()
                    planta_accesible.ver_evaluaciones = f"evaluaciones-{planta.pk}" in request.POST.keys()
                    planta_accesible.crear_evaluaciones = f"crearevals-{planta.pk}" in request.POST.keys()
                    planta_accesible.eliminar_evaluaciones = f"delevals-{planta.pk}" in request.POST.keys()
                    planta_accesible.save()
                
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
                usuario.username = request.POST['correo'].lower() if '@' in usuario.username else usuario.username
                usuario.first_name =  request.POST['nombre'].title()
                usuario.is_active = 'activo' in request.POST.keys()
                usuario.is_superuser = 'superusuario' in request.POST.keys()

                usuario.usuario_planta.all().delete()

                # Assign plants according to the marked checkboxes
                ids = []
                for key in request.POST.keys():
                    if key.startswith('planta-'):
                        planta_id = key.split('-')[1]
                        ids.append(planta_id)

                plantas = Planta.objects.filter(pk__in = ids)

                for planta in plantas:
                    planta_accesible = PlantaAccesible.objects.create(planta=planta, usuario=usuario)
                    planta_accesible.crear = f"crear-{planta.pk}" in request.POST.keys()
                    planta_accesible.edicion = f"editar-{planta.pk}" in request.POST.keys()
                    planta_accesible.edicion_instalacion = f"instalacion-{planta.pk}" in request.POST.keys()
                    planta_accesible.duplicacion = f"duplicacion-{planta.pk}" in request.POST.keys()
                    planta_accesible.ver_evaluaciones = f"evaluaciones-{planta.pk}" in request.POST.keys()
                    planta_accesible.crear_evaluaciones = f"crearevals-{planta.pk}" in request.POST.keys()
                    planta_accesible.eliminar_evaluaciones = f"delevals-{planta.pk}" in request.POST.keys()
                    planta_accesible.save()

                usuario.save()

                messages.success(request, "Se han registrado los cambios.")

                return redirect("/usuarios/")
        else:
            return render(request, 'usuarios/creacion.html', {'errores': errores, 'previo': request.POST, 'edicion': True, **self.context})
    
    def get(self, request, pk):
        usuario = self.modelo.objects.get(pk=pk)
        plantas = usuario.usuario_planta.all()
        previo = {
            'nombre': usuario.first_name,
            'correo': usuario.email,
            'superusuario': usuario.is_superuser,
            'activo': usuario.is_active,
            'plantas': [planta.planta.pk for planta in plantas],
            'creaciones': [planta.planta.pk for planta in plantas.filter(crear = True)],
            'ediciones': [planta.planta.pk for planta in plantas.filter(edicion = True)],
            'ediciones_instalacion': [planta.planta.pk for planta in plantas.filter(edicion_instalacion = True)],
            'duplicaciones': [planta.planta.pk for planta in plantas.filter(duplicacion = True)],
            'evaluaciones': [planta.planta.pk for planta in plantas.filter(ver_evaluaciones = True)],
            'crear_evaluaciones': [planta.planta.pk for planta in plantas.filter(crear_evaluaciones = True)],
            'eliminar_evaluaciones': [planta.planta.pk for planta in plantas.filter(eliminar_evaluaciones = True)],
        }

        return render(request, 'usuarios/creacion.html', context={'previo': previo, 'edicion': True, 'complejos': Complejo.objects.prefetch_related('plantas').all(), **self.context})

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
        if(Envio.objects.filter(encuesta=Encuesta.objects.first(), usuario=request.user).exists()):
            return redirect("/usuarios/encuesta/resultados/")
        
        return render(request, 'form_encuesta.html', self.get_context_data())

class ConsultaEncuestas(LoginRequiredMixin, ListView):
    """
    Resumen:
        Vista de la lista de encuestas existentes. 
        Únicamente pueden acceder superusuarios.

    Atributos:
        modelo: Model
            modelos (User) de la creación.

        context: dict
            Diccionario que contiene la data contextual de la vista.
            Incluye inicialmente el título.
    
    Métodos:
        get_context_data(self, **kwargs)
            Contiene la lógica de renderizado del formulario.
    """
    model = Envio
    paginate_by = 10
    template_name = 'consulta_encuesta.html'

    def filtrar(self, queryset):
        desde = self.request.GET.get('desde', '')
        hasta = self.request.GET.get('hasta', '')
        usuario = self.request.GET.get('usuario', '')

        # Lógica de filtrado según valor del parámetro
        if(desde != ''):
            queryset = queryset.filter(
                fecha__gte = desde
            )

        if(hasta != ''):
            queryset = queryset.filter(
                fecha__lte=hasta
            )

        if(usuario != ''):
            queryset = queryset.filter(
                Q(usuario__first_name__icontains = usuario) |
                Q(usuario__last_name__icontains = usuario)
            )

        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Encuestas de Satisfacción'

        return ctx

    def get_queryset(self) -> QuerySet:
        return self.filtrar(self.model.objects.filter(
            encuesta=Encuesta.objects.first()
        ).select_related(
            'usuario', 'encuesta',
        ).prefetch_related(
            Prefetch('encuesta__secciones', Seccion.objects.prefetch_related('preguntas')),
            Prefetch('respuestas', Respuesta.objects.select_related('pregunta', 'pregunta__seccion'))
        ))
    
def graficas_encuestas(request):
    respuestas = Respuesta.objects.all().select_related('pregunta')
    questions = {}
    for respuesta in respuestas:
        if respuesta.pregunta.tipo != "3":
            if respuesta.pregunta.pk not in questions:
                questions[respuesta.pregunta.pk] = {}
            if respuesta.respuesta not in questions[respuesta.pregunta.pk]:
                questions[respuesta.pregunta.pk][respuesta.respuesta] = 1
            else:
                questions[respuesta.pregunta.pk][respuesta.respuesta] += 1

    for question, keys in questions.items():
        if 'Sí' in keys or 'No' in keys:
            for key in ['Sí','No']:
                if key not in keys:
                    questions[question][key] = 0
        else:
            for j in range(1, 6):
                if str(j) not in keys:
                    questions[question][str(j)] = 0

    return JsonResponse(questions)

class PuedeCrear(LoginRequiredMixin):
    def test_func(self):
        return self.request.user.usuario_planta.filter(crear = True).exists()