from django.contrib import admin
from .models import Empresa, RespostaFormulario, Relatorio

# Register your models here.

admin.site.register(Empresa)
admin.site.register(RespostaFormulario)
admin.site.register(Relatorio)

