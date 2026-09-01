import json
from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from criancas.models import Crianca
from exercicios.models import ExercicioModelo, ExercicioResultado
from sessoes.models import SessaoModelo, SessaoRealizada


class EnviarSessaoTests(TestCase):
    def setUp(self):
        self.terapeuta = User.objects.create_user(username='terapeuta', password='senha123')
        self.crianca = Crianca.objects.create(
            terapeuta=self.terapeuta, nome='Criança Teste', data_nascimento=date(2018, 1, 1)
        )
        self.sessao_modelo = SessaoModelo.objects.create(numero=1, titulo='Sessão 1')
        self.ex_multipla = ExercicioModelo.objects.create(
            sessao_modelo=self.sessao_modelo,
            numero=1,
            tipo='multipla_escolha',
            enunciado='Qual a capital?',
            configuracao={'perguntas': [{'texto': 'Capital do Brasil?', 'opcoes': ['Brasília', 'Rio'], 'correta': 0}]},
        )
        self.ex_aberta = ExercicioModelo.objects.create(
            sessao_modelo=self.sessao_modelo,
            numero=2,
            tipo='pergunta_aberta',
            enunciado='Escreva algo',
            configuracao={'itens': [{'texto': 'O que você fez hoje?'}]},
        )
        self.sessao_realizada = SessaoRealizada.objects.create(
            crianca=self.crianca,
            sessao_modelo=self.sessao_modelo,
            terapeuta=self.terapeuta,
            data=timezone.now(),
            status='em_andamento',
        )
        self.client.force_login(self.terapeuta)
        self.url = reverse('sessoes:enviar_sessao', args=[self.sessao_realizada.id])

    def _payload(self, resultados):
        return json.dumps({'resultados': resultados})

    def test_tudo_certo_marca_sessao_como_concluida(self):
        resultados = [
            {'exercicio_id': self.ex_multipla.id, 'percentual_acerto': 100, 'pontuacao': 100,
             'tempo_segundos': 5, 'tentativas': 1, 'respostas': {'opcoes_selecionadas': [0]}},
            {'exercicio_id': self.ex_aberta.id, 'percentual_acerto': 100, 'pontuacao': 100,
             'tempo_segundos': 5, 'tentativas': 1, 'respostas': {'textos': ['Fui ao parque']}},
        ]
        resp = self.client.post(self.url, data=self._payload(resultados), content_type='application/json')

        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['concluida'])
        self.assertIsNone(data['primeiro_erro_exercicio_id'])

        self.sessao_realizada.refresh_from_db()
        self.assertEqual(self.sessao_realizada.status, 'concluida')

    def test_exercicio_errado_nao_conclui_e_aponta_primeiro_erro(self):
        resultados = [
            {'exercicio_id': self.ex_multipla.id, 'percentual_acerto': 0, 'pontuacao': 0,
             'tempo_segundos': 5, 'tentativas': 1, 'respostas': {'opcoes_selecionadas': [1]}},
            {'exercicio_id': self.ex_aberta.id, 'percentual_acerto': 100, 'pontuacao': 100,
             'tempo_segundos': 5, 'tentativas': 1, 'respostas': {'textos': ['Fui ao parque']}},
        ]
        resp = self.client.post(self.url, data=self._payload(resultados), content_type='application/json')

        data = resp.json()
        self.assertFalse(data['concluida'])
        self.assertEqual(data['primeiro_erro_exercicio_id'], self.ex_multipla.id)

        self.sessao_realizada.refresh_from_db()
        self.assertEqual(self.sessao_realizada.status, 'em_andamento')

    def test_exercicio_nao_respondido_conta_como_erro(self):
        resultados = [
            {'exercicio_id': self.ex_multipla.id, 'percentual_acerto': 100, 'pontuacao': 100,
             'tempo_segundos': 5, 'tentativas': 1, 'respostas': {'opcoes_selecionadas': [0]}},
        ]
        resp = self.client.post(self.url, data=self._payload(resultados), content_type='application/json')

        data = resp.json()
        self.assertFalse(data['concluida'])
        self.assertEqual(data['primeiro_erro_exercicio_id'], self.ex_aberta.id)

    def test_persiste_respostas_e_tentativas(self):
        resultados = [
            {'exercicio_id': self.ex_multipla.id, 'percentual_acerto': 0, 'pontuacao': 0,
             'tempo_segundos': 5, 'tentativas': 2, 'respostas': {'opcoes_selecionadas': [1]}},
            {'exercicio_id': self.ex_aberta.id, 'percentual_acerto': 100, 'pontuacao': 100,
             'tempo_segundos': 5, 'tentativas': 1, 'respostas': {'textos': ['Fui ao parque']}},
        ]
        self.client.post(self.url, data=self._payload(resultados), content_type='application/json')

        resultado = ExercicioResultado.objects.get(
            sessao_realizada=self.sessao_realizada, exercicio_modelo=self.ex_multipla
        )
        self.assertEqual(resultado.tentativas, 2)
        self.assertEqual(resultado.respostas, {'opcoes_selecionadas': [1]})
        self.assertFalse(resultado.correto)

    def test_reenvio_atualiza_resultado_existente_sem_duplicar(self):
        resultados_errado = [
            {'exercicio_id': self.ex_multipla.id, 'percentual_acerto': 0, 'pontuacao': 0,
             'tempo_segundos': 5, 'tentativas': 1, 'respostas': {'opcoes_selecionadas': [1]}},
            {'exercicio_id': self.ex_aberta.id, 'percentual_acerto': 100, 'pontuacao': 100,
             'tempo_segundos': 5, 'tentativas': 1, 'respostas': {'textos': ['Fui ao parque']}},
        ]
        self.client.post(self.url, data=self._payload(resultados_errado), content_type='application/json')

        resultados_corrigido = [
            {'exercicio_id': self.ex_multipla.id, 'percentual_acerto': 100, 'pontuacao': 100,
             'tempo_segundos': 8, 'tentativas': 2, 'respostas': {'opcoes_selecionadas': [0]}},
            {'exercicio_id': self.ex_aberta.id, 'percentual_acerto': 100, 'pontuacao': 100,
             'tempo_segundos': 5, 'tentativas': 1, 'respostas': {'textos': ['Fui ao parque']}},
        ]
        resp = self.client.post(self.url, data=self._payload(resultados_corrigido), content_type='application/json')

        self.assertTrue(resp.json()['concluida'])
        self.assertEqual(
            ExercicioResultado.objects.filter(sessao_realizada=self.sessao_realizada).count(), 2
        )

    def test_outro_terapeuta_nao_acessa_sessao(self):
        outro = User.objects.create_user(username='outro', password='senha123')
        self.client.force_login(outro)
        resp = self.client.post(self.url, data=self._payload([]), content_type='application/json')
        self.assertEqual(resp.status_code, 404)
