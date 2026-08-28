from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from criancas.models import Crianca
from sessoes.models import SessaoModelo, SessaoRealizada, Tema


class SessoesModelAndViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="terapeuta", password="password123")
        self.crianca = Crianca.objects.create(
            nome="Criança Teste",
            data_nascimento=date(2018, 5, 10),
            terapeuta=self.user
        )
        self.tema = Tema.objects.create(
            nome="Alfabetização Lúdica",
            descricao="Exercícios focados em sons e palavras",
            cor="#3B82F6",
            icone="bi-fonts"
        )
        self.sessao_modelo = SessaoModelo.objects.create(
            numero=1,
            titulo="Sons e Primeiras Palavras",
            objetivo="Desenvolver consciência fonológica e síntese silábica",
            descricao="Sessão introdutória com 9 exercícios",
            faixa_etaria="6 a 10 anos",
            tema=self.tema
        )

    def test_tema_creation(self):
        self.assertEqual(str(self.tema), "Alfabetização Lúdica")
        self.assertEqual(self.tema.cor, "#3B82F6")

    def test_sessao_modelo_with_tema_and_objetivo(self):
        self.assertEqual(str(self.sessao_modelo), "Sessão 1 - Sons e Primeiras Palavras")
        self.assertEqual(self.sessao_modelo.tema, self.tema)
        self.assertEqual(self.sessao_modelo.objetivo, "Desenvolver consciência fonológica e síntese silábica")
        self.assertEqual(self.sessao_modelo.faixa_etaria, "6 a 10 anos")

    def test_escolher_sessao_view_authenticated(self):
        from django.urls import reverse
        self.client.login(username="terapeuta", password="password123")
        url = reverse('sessoes:escolher_sessao', kwargs={'crianca_id': self.crianca.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alfabetização Lúdica")
        self.assertContains(response, "Sons e Primeiras Palavras")
        self.assertContains(response, "Desenvolver consciência fonológica")
