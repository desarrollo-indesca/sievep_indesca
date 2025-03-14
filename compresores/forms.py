from django import forms
from django.core.validators import MinValueValidator
from intercambiadores.models import Complejo
from .models import *

class CompresorForm(forms.ModelForm):    
    complejo = forms.ModelChoiceField(queryset=Complejo.objects.all(), empty_label=None)
    numero_etapas = forms.IntegerField(required=True, validators=[MinValueValidator(1)])

    class Meta:
        model = Compresor
        exclude = ['id', 'creado_al', 'creado_por', 'editado_al', 'editado_por', 'copia']

class PropiedadesCompresorForm(forms.ModelForm):    
    class Meta:
        model = PropiedadesCompresor
        exclude = ['id', 'compresor']

class EtapaCompresorForm(forms.ModelForm):    
    class Meta:
        model = EtapaCompresor
        exclude = ['id', 'compresor', 'numero']

class LadoEtapaCompresorForm(forms.ModelForm):    
    class Meta:
        model = LadoEtapaCompresor
        exclude = ['id', 'etapa', 'lado']

class ComposicionGasForm(forms.ModelForm):    
    class Meta:
        model = ComposicionGases
        exclude = ['id', 'etapa']
        widgets = {'etapa': forms.HiddenInput(), 'compuesto': forms.HiddenInput()}

class EntradaEtapaEvaluacionForm(forms.ModelForm):    
    class Meta:
        model = EntradaEtapaEvaluacion
        exclude = ['id', 'etapa', 'evaluacion']

class EvaluacionCompresorForm(forms.ModelForm):    
    class Meta:
        model = Evaluacion
        exclude = ['id', 'evaluacion', 'compresor', 'creado_al', 'creado_por']

class ComposicionEvaluacionForm(forms.ModelForm):
    class Meta:
        model = ComposicionEvaluacion
        exclude = ['id',]