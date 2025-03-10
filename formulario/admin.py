from django.contrib import admin
from .models import Formulario, Pergunta, Resposta, AnaliseSWOT, SWOTResponse, RespostaFormulario


@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'contador', 'data_criacao', 'slug')
    search_fields = ('titulo', 'contador__username')
    readonly_fields = ('slug',)

@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'formulario', 'tipo', 'categoria_swot')
    list_filter = ('tipo', 'formulario')
    search_fields = ('texto',)

@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('formulario', 'pergunta', 'data_resposta')
    raw_id_fields = ('formulario', 'pergunta')

@admin.register(AnaliseSWOT)
class AnaliseSWOTAdmin(admin.ModelAdmin):
    list_display = ('formulario', 'data_criacao')
    readonly_fields = ('data_criacao',)
