from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from criancas.models import Crianca
from exercicios.models import ExercicioModelo, ExercicioResultado
from sessoes.models import SessaoModelo, SessaoRealizada


class ExercicioResultadoCorretoTests(TestCase):
    def setUp(self):
        terapeuta = User.objects.create_user(username='terapeuta', password='senha123')
        crianca = Crianca.objects.create(
            terapeuta=terapeuta, nome='Criança Teste', data_nascimento=date(2018, 1, 1)
        )
        sessao_modelo = SessaoModelo.objects.create(numero=1, titulo='Sessão 1')
        self.exercicio = ExercicioModelo.objects.create(
            sessao_modelo=sessao_modelo, numero=1, tipo='ordena_letras', enunciado='Ordene',
        )
        self.sessao_realizada = SessaoRealizada.objects.create(
            crianca=crianca, sessao_modelo=sessao_modelo, terapeuta=terapeuta,
            data=timezone.now(), status='em_andamento',
        )

    def _resultado(self, percentual):
        return ExercicioResultado.objects.create(
            sessao_realizada=self.sessao_realizada,
            exercicio_modelo=self.exercicio,
            ordem_execucao=1,
            percentual_acerto=Decimal(str(percentual)),
            tentativas=1,
            tempo_segundos=10,
            pontuacao=int(percentual),
        )

    def test_correto_quando_percentual_e_cem(self):
        self.assertTrue(self._resultado(100).correto)

    def test_incorreto_quando_percentual_menor_que_cem(self):
        resultado = self._resultado(99.99)
        self.assertFalse(resultado.correto)
        resultado.percentual_acerto = Decimal('0')
        self.assertFalse(resultado.correto)

    def test_respostas_default_e_dict_vazio(self):
        resultado = self._resultado(100)
        self.assertEqual(resultado.respostas, {})
