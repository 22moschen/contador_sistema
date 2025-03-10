from django.test import TestCase
from .models import Formulario, Pergunta, RespostaFormulario
from django.contrib.auth.models import User

class RespostaFormularioTestCase(TestCase):
    def setUp(self):
        self.usuario = User.objects.create(username='contador_teste')
        self.formulario = Formulario.objects.create(nome='Formulario Teste', usuario=self.usuario)
        self.pergunta = Pergunta.objects.create(texto='Pergunta Teste', formulario=self.formulario)

    def test_resposta_notificacao(self):
        resposta = RespostaFormulario.objects.create(pergunta=self.pergunta, resposta='Resposta Teste')
        self.assertIsNotNone(resposta)  # Verifica se a resposta foi criada
        # Aqui você pode adicionar mais verificações para garantir que a notificação foi enviada
