from django.test import TestCase
from formulario.models import Empresa, Formulario, RespostaFormulario, SWOT

from django.contrib.auth.models import User  # Adicione esta linha


class EmpresaModelTest(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nome="Empresa Teste",
            cnpj="12.345.678/0001-90",
            endereco="Rua Teste, 123",
            telefone="123456789",
            email="teste@empresa.com"
        )

    def test_empresa_str(self):
        self.assertEqual(str(self.empresa), "Empresa Teste")

class FormularioModelTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.formulario = Formulario.objects.create(
            nome="Formulario Teste",
            usuario=self.usuario  # Supondo que você tenha um usuário criado
        )

    def test_formulario_str(self):
        self.assertEqual(str(self.formulario), "Formulario Teste")

class RespostaFormularioModelTest(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nome="Empresa Teste",
            cnpj="12.345.678/0001-90",
            endereco="Rua Teste, 123",
            telefone="123456789",
            email="teste@empresa.com"
        )

        self.usuario = User.objects.create_user ( # criando um usuario.
            username="testuser",
            password="testpass123"
        )

        self.formulario = Formulario.objects.create(
            nome="Formulario Teste",
            usuario=self.usuario  # Usando o usuario criado.
        )

        self.resposta = RespostaFormulario.objects.create(
            formulario=self.formulario,
            resposta="Esta é uma resposta de teste."
        )

    def test_resposta_str(self):
        self.assertEqual(str(self.resposta), f'Resposta para {self.formulario.nome}')

class SWOTModelTest(TestCase):
    def setUp(self):
        self.swot = SWOT.objects.create(
            cnpj="12.345.678/0001-90",
            forcas="Força Teste",
            fraquezas="Fraqueza Teste",
            oportunidades="Oportunidade Teste",
            ameacas="Ameaça Teste"
        )

    def test_swot_str(self):
        self.assertEqual(str(self.swot), "Análise SWOT para 12.345.678/0001-90")