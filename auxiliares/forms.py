from django import forms
from intercambiadores.models import Complejo
from auxiliares.models import *

class BombaForm(forms.ModelForm):
    complejo = forms.ModelChoiceField(queryset=Complejo.objects.all(), initial=1)
    class Meta:
        model = Bombas
        fields = [
            "tag", "descripcion", "fabricante", "modelo",
            "planta", "grafica", "tipo_bomba"
        ]

class EspecificacionesBombaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['velocidad_unidad'].empty_label = None
        self.fields['velocidad_unidad'].queryset = Unidades.objects.filter(simbolo = 'RPM')

    class Meta:
        model = EspecificacionesBomba
        exclude = [
            "id"
        ]

# class DetallesConstruccionBombaForm(forms.ModelForm):
#     model = DetallesConstruccionBomba

# class DetallesMotorBombaForm(forms.ModelForm):
#     model = DetallesMotorBomba

# class CondicionesDisenoBombaForm(forms.ModelForm):
#     model = CondicionesDisenoBomba

# class CondicionFluidoBombaForm(forms.ModelForm):
#     model = CondicionFluidoBomba