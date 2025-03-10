# contador_sistema/formulario/forms.py
from django import forms
from .models import Formulario, Pergunta, Resposta

class SWOTForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ['titulo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'})
        }

class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = ['texto', 'tipo', 'categoria_swot']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'categoria_swot': forms.Select(attrs={'class': 'form-select'})
        }

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }