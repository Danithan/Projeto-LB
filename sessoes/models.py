from django.db import models
from django.contrib.auth.models import User
from criancas.models import Crianca


class Tema(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    cor = models.CharField(max_length=20, default="#4F46E5", blank=True, help_text="Código de cor (HEX) para identificação visual")
    icone = models.CharField(max_length=50, blank=True, default="bi-stars", help_text="Classe de ícone Bootstrap")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tema"
        verbose_name_plural = "Temas"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class SessaoModelo(models.Model):
    numero = models.IntegerField(unique=True)
    titulo = models.CharField(max_length=100, help_text="Nomenclatura da sessão")
    objetivo = models.TextField(blank=True, help_text="Objetivo pedagógico e terapêutico da sessão")
    descricao = models.TextField(blank=True)
    faixa_etaria = models.CharField(max_length=50, blank=True, default="Geral", help_text="Faixa etária recomendada (ex: 3 a 5 anos, 6 a 10 anos, 11+ anos)")
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessoes_modelo")

    class Meta:
        verbose_name = "Sessão Modelo"
        verbose_name_plural = "Sessões Modelo"
        ordering = ['numero']

    def __str__(self):
        return f"Sessão {self.numero} - {self.titulo}"

class SessaoRealizada(models.Model):
    STATUS_CHOICES = [
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
    ]

    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE)
    sessao_modelo = models.ForeignKey(SessaoModelo, on_delete=models.PROTECT)
    terapeuta = models.ForeignKey(User, on_delete=models.PROTECT)
    data = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    observacoes = models.TextField(blank=True)
    exercicios_selecionados = models.ManyToManyField('exercicios.ExercicioModelo', blank=True)

    def __str__(self):
        return f"{self.crianca.nome} - {self.sessao_modelo.titulo} ({self.data:%d/%m/%Y})"