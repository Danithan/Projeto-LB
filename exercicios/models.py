# pyrefly: ignore [missing-import]
from django.db import models
from sessoes.models import SessaoModelo, SessaoRealizada


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

class ExercicioResultado(models.Model):
    sessao_realizada = models.ForeignKey(SessaoRealizada, on_delete=models.CASCADE)
    exercicio_modelo = models.ForeignKey(ExercicioModelo, on_delete=models.PROTECT)
    ordem_execucao = models.IntegerField()
    percentual_acerto = models.DecimalField(max_digits=5, decimal_places=2)
    tentativas = models.IntegerField()
    tempo_segundos = models.IntegerField()
    pontuacao = models.IntegerField()
    respondido_em = models.DateTimeField(auto_now_add=True)