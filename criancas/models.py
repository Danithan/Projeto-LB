from django.db import models

class Crianca(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    criada_em = models.DateTimeField(auto_now_add=True)
    
