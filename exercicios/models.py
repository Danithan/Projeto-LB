from django.db import models
from sessoes.models import SessaoModelo


class ExercicioModelo(models.Model):
    TIPO_CHOICES = [
        ('pergunta_aberta', 'Pergunta Aberta'),
        ('jogo_palavras', 'Jogo de Palavras'),
    ]

    sessao_modelo = models.ForeignKey(SessaoModelo, on_delete=models.PROTECT)
    numero = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    enunciado = models.TextField()
    configuracao = models.JSONField(blank=True, default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sessao_modelo', 'numero'], name='numero_unico_por_sessao')
        ]