# pyrefly: ignore [missing-import]
from django.db import models
from sessoes.models import SessaoModelo, SessaoRealizada


class ExercicioModelo(models.Model):
    TIPO_CHOICES = [
        ('pergunta_aberta', 'Pergunta Aberta'),
        ('jogo_palavras', 'Jogo de Palavras'),
        ('multipla_escolha', 'Múltipla Escolha'),
        ('verdadeiro_falso', 'Verdadeiro ou Falso'),
        ('caca_palavras', 'Caça-Palavras'),
        ('cruzadinha', 'Cruzadinha'),
        ('ordena_letras', 'Ordene as Letras'),
        ('preenche_lacunas_letras', 'Lacunas com Letras'),
    ]

    sessao_modelo = models.ForeignKey(SessaoModelo, on_delete=models.PROTECT)
    numero = models.IntegerField()
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    enunciado = models.TextField()
    configuracao = models.JSONField(blank=True, default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sessao_modelo', 'numero'], name='numero_unico_por_sessao')
        ]

    def __str__(self):
        return f"{self.sessao_modelo} - Exercício {self.numero} ({self.get_tipo_display()})"

class ExercicioResultado(models.Model):
    sessao_realizada = models.ForeignKey(SessaoRealizada, on_delete=models.CASCADE)
    exercicio_modelo = models.ForeignKey(ExercicioModelo, on_delete=models.PROTECT)
    ordem_execucao = models.IntegerField()
    percentual_acerto = models.DecimalField(max_digits=5, decimal_places=2)
    tentativas = models.IntegerField()
    tempo_segundos = models.IntegerField()
    pontuacao = models.IntegerField()
    respostas = models.JSONField(blank=True, default=dict)
    respondido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sessao_realizada', 'exercicio_modelo'],
                name='resultado_unico_por_exercicio_sessao',
            )
        ]

    @property
    def correto(self):
        return self.percentual_acerto == 100

    def __str__(self):
        return f"{self.exercicio_modelo} - {self.percentual_acerto}%"