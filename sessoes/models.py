from django.db import models
from django.contrib.auth.models import User
from criancas.models import Crianca


class SessaoModelo(models.Model):
    numero = models.IntegerField(unique=True)
    titulo = models.CharField(max_length=50)
    descricao = models.TextField(blank=True)

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