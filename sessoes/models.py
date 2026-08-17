from django.db import models


class SessaoModelo(models.Model):
    numero = models.IntegerField(unique=True)
    titulo = models.CharField(max_length=50)
    descricao = models.TextField(blank=True)