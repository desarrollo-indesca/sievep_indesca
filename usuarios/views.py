from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model

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

        print(new_context)

        return new_context
