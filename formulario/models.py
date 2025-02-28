from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nome

class Formulario(models.Model):
    nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Pergunta(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    texto = models.TextField()

    def __str__(self):
        return self.texto

class RespostaFormulario(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, default=1)  # Adicionando valor padrão
    resposta = models.CharField(max_length=255)

    def __str__(self):
        return self.resposta

class SWOT(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    forcas = models.TextField()
    fraquezas = models.TextField()
    oportunidades = models.TextField()
    ameacas = models.TextField()

    def __str__(self):
        return f"SWOT para {self.formulario.nome}"

class Relatorio(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE, default=1)  # Adicionando valor padrão
    pontos_fortes = models.TextField(default="Pontos fortes...")  # Adicionando valor padrão
    pontos_fracos = models.TextField(default="Pontos fracos...")  # Adicionando valor padrão
    recomendacoes = models.TextField(default="Recomendações...")  # Adicionando valor padrão

    def __str__(self):
        return f"Relatório para {self.formulario.nome}"