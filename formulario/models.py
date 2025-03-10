from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class Formulario(models.Model):
    contador = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)
            self.slug = base_slug
            counter = 1
            while Formulario.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Pergunta(models.Model):
    TIPO_CHOICES = [
        ('texto', 'Resposta Textual'),
        ('multipla', 'Múltipla Escolha'),
        ('swot', 'Classificação SWOT')
    ]
    
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    texto = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    categoria_swot = models.CharField(max_length=15, blank=True, null=True)

    def clean(self):
        if self.tipo == 'swot' and not self.categoria_swot:
            raise ValidationError("Perguntas SWOT devem ter uma categoria definida")
        super().clean()

class Resposta(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_resposta = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('formulario', 'pergunta')

class SWOTResponse(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    resposta = models.TextField()
    data_resposta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resposta SWOT - {self.formulario.titulo}"

class RespostaFormulario(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_resposta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resposta - {self.formulario.titulo}"

class AnaliseSWOT(models.Model):

    formulario = models.OneToOneField(Formulario, on_delete=models.CASCADE)
    strengths = models.TextField()
    weaknesses = models.TextField()
    opportunities = models.TextField()
    threats = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Análise SWOT - {self.formulario.titulo}"
