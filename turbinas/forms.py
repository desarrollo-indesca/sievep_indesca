from django import forms
from intercambiadores.models import Complejo
from simulaciones_pequiven.unidades import *
from .models import *
from auxiliares.forms import FormConUnidades

class TurbinaVaporForm(forms.ModelForm):
    complejo = forms.ModelChoiceField(queryset=Complejo.objects.all(), initial=1)

    def clean_tag(self):
        return self.data['tag'].upper().strip()
    
    class Meta:
        model = TurbinaVapor
        exclude = (
            'id', 'generador_electrico', 'especificaciones',
            'datos_corrientes', 'creado_por', 'creado_al',
            'editado_por', 'editado_al'
        )

class EspecificacionesTurbinaVaporForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['potencia_unidad'].empty_label = None
        self.fields['potencia_unidad'].queryset = UNIDADES_POTENCIA

        self.fields['velocidad_unidad'].empty_label = None
        self.fields['velocidad_unidad'].queryset = UNIDADES_VELOCIDAD_ANGULAR

        self.fields['presion_entrada_unidad'].empty_label = None
        self.fields['presion_entrada_unidad'].queryset = UNIDADES_PRESION

        self.fields['temperatura_entrada_unidad'].empty_label = None
        self.fields['temperatura_entrada_unidad'].queryset = UNIDADES_TEMPERATURA

        self.fields['contra_presion_unidad'].empty_label = None
        self.fields['contra_presion_unidad'].queryset = UNIDADES_TEMPERATURA

    class Meta:
        model = EspecificacionesTurbinaVapor
        exclude = ('id', 'eficiencia')

class GeneradorElectricoForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['ciclos_unidad'].empty_label = None
        self.fields['ciclos_unidad'].queryset = UNIDADES_FRECUENCIA

        self.fields['potencia_real_unidad'].empty_label = None
        self.fields['potencia_real_unidad'].queryset = UNIDADES_POTENCIA
        
        self.fields['potencia_aparente_unidad'].empty_label = None
        self.fields['potencia_aparente_unidad'].queryset = UNIDADES_POTENCIA_APARENTE

        self.fields['velocidad_unidad'].empty_label = None
        self.fields['velocidad_unidad'].queryset = UNIDADES_VELOCIDAD_ANGULAR

        self.fields['corriente_electrica_unidad'].empty_label = None
        self.fields['corriente_electrica_unidad'].queryset = UNIDADES_CORRIENTE

        self.fields['voltaje_unidad'].empty_label = None
        self.fields['voltaje_unidad'].queryset = UNIDADES_VOLTAJE

    class Meta:
        model = GeneradorElectrico
        exclude = ('id',)

class CorrienteForm(forms.ModelForm):
    def clean_presion(self):
        if(self.cleaned_data.get('presion') == '' and self.data['entrada'] == 'checked'):
            return forms.ValidationError("La corriente en entrada debe llevar presión.")
        
        return self.cleaned_data.get('presion')

    class Meta:
        model = Corriente
        exclude = ('id', 'datos_corriente')

class DatosCorrientesForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['flujo_unidad'].empty_label = None
        self.fields['flujo_unidad'].queryset = UNIDADES_FLUJOS
        
        self.fields['presion_unidad'].empty_label = None
        self.fields['presion_unidad'].queryset = UNIDADES_PRESION

        self.fields['entalpia_unidad'].empty_label = None
        self.fields['entalpia_unidad'].queryset = UNIDADES_ENTALPIA

        self.fields['temperatura_unidad'].empty_label = None
        self.fields['temperatura_unidad'].queryset = UNIDADES_TEMPERATURA

    class Meta:
        model = DatosCorrientes
        exclude = ('id',)
    
corrientes_formset = forms.modelformset_factory(
    Corriente, form=CorrienteForm, extra=0, can_delete=True, min_num=2, exclude=('id','datos_corriente')
)