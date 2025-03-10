# formulario/apps.py
from django.apps import AppConfig

class FormularioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'formulario'

    def ready(self):
        if not hasattr(self, 'already_loaded'):
            from . import signals  # Garantir carga única
            self.already_loaded = True