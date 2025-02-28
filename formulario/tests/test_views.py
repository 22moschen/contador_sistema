'''
from django.test import TestCase
from django.urls import reverse
from .models import Empresa, SWOT

class SWOTViewTests(TestCase):



    def setUp(self):
        # Configurar um objeto Empresa para os testes
        self.empresa = Empresa.objects.create(
            nome="Empresa Teste",
            cnpj="12.345.678/0001-90",
            endereco="Endereço Teste",
            telefone="123456789",
            email="teste@empresa.com"
        )

    def test_exibir_swot_form(self):


        response = self.client.get(reverse('exibir_swot_formulario'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'formulario/swot_form.html')

    def test_submeter_swot_formulario(self):


        response = self.client.post(reverse('submeter_swot_formulario'), {


            'cnpj': self.empresa.cnpj,
            'forcas': 'Força 1',
            'fraquezas': 'Fraqueza 1',
            'oportunidades': 'Oportunidade 1',
            'ameacas': 'Ameaça 1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Análise SWOT submetida com sucesso!')

        # Verificar se os dados foram salvos no banco de dados
        swot = SWOT.objects.get(cnpj=self.empresa.cnpj)
        self.assertEqual(swot.forcas, 'Força 1')
        self.assertEqual(swot.fraquezas, 'Fraqueza 1')
        self.assertEqual(swot.oportunidades, 'Oportunidade 1')
        self.assertEqual(swot.ameacas, 'Ameaça 1')
'''