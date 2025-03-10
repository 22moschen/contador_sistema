from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Resposta, RespostaFormulario


@receiver(post_save, sender=Resposta)
def handle_resposta(sender, instance, **kwargs):
    if instance.resposta:  # Verifica se a resposta foi preenchida
        # Lógica para enviar e-mail ou notificação
        print(f"Notificar contador sobre a resposta: {instance.resposta}")
