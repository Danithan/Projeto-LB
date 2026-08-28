from datetime import date
from django.db import models
from django.contrib.auth.models import User

class Crianca(models.Model):
    terapeuta = models.ForeignKey(User, on_delete=models.CASCADE, related_name="criancas", null=True, blank=True)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='perfil_crianca')
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    criada_em = models.DateTimeField(auto_now_add=True)
    @property
    def idade(self):
        hoje = date.today()

        anos = hoje.year - self.data_nascimento.year
        anos -= (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)

        meses = (hoje.month - self.data_nascimento.month) % 12
        if hoje.day < self.data_nascimento.day:
            meses -= 1
            meses %= 12

        return f"{anos} anos e {meses} meses"

    def __str__(self):
        return self.nome