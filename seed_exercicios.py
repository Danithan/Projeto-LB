import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from criancas.models import Crianca
from sessoes.models import SessaoModelo, SessaoRealizada
from exercicios.models import ExercicioModelo
from django.utils import timezone

def seed():
    # Setup base entities
    user, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})
    if _: user.set_password('admin'); user.save()

    crianca, _ = Crianca.objects.get_or_create(nome='Joãozinho', data_nascimento='2015-05-10')
    
    sessao_modelo, _ = SessaoModelo.objects.get_or_create(numero=1, titulo='Sessão de Teste Cognitivo')
    
    sessao_realizada, _ = SessaoRealizada.objects.get_or_create(
        crianca=crianca,
        sessao_modelo=sessao_modelo,
        terapeuta=user,
        data=timezone.now(),
        status='em_andamento'
    )

    # 1. Preenche Lacunas Letras
    ExercicioModelo.objects.get_or_create(
        sessao_modelo=sessao_modelo,
        numero=1,
        tipo='preenche_lacunas_letras',
        defaults={
            'enunciado': 'Encontre as profissões no quadro e complete as frases.',
            'configuracao': {
                'grid': [
                    ["O", "R", "I", "E", "N", "A"],
                    ["R", "O", "R", "D", "I", "X"],
                    ["I", "E", "A", "C", "A", "I"],
                    ["E", "J", "N", "O", "R", "I"],
                    ["M", "R", "R", "F", "H", "E"],
                    ["B", "O", "E", "R", "A", "C"]
                ],
                'frases': [
                    "Paulo trabalha num hospital. Ele é {0}",
                    "Agenor troca pneus. Ele é {1}"
                ],
                'respostas': ["MÉDICO", "BORRACHEIRO"]
            }
        }
    )

    # 2. Cruzadinha
    ExercicioModelo.objects.get_or_create(
        sessao_modelo=sessao_modelo,
        numero=2,
        tipo='cruzadinha',
        defaults={
            'enunciado': 'Complete a cruzadinha com nomes de cores.',
            'configuracao': {
                'dicas': ["Cor da maçã (vertical)", "Cor do céu (horizontal)"],
                'celulas': [
                    {"x": 2, "y": 0, "letra": "V", "numero": 1, "editavel": True},
                    {"x": 2, "y": 1, "letra": "E", "editavel": True},
                    {"x": 2, "y": 2, "letra": "R", "editavel": True},
                    {"x": 2, "y": 3, "letra": "M", "numero": 2, "editavel": True},
                    {"x": 3, "y": 3, "letra": "A", "editavel": True},
                    {"x": 4, "y": 3, "letra": "R", "editavel": True},
                    {"x": 5, "y": 3, "letra": "R", "editavel": True},
                    {"x": 6, "y": 3, "letra": "O", "editavel": True},
                    {"x": 7, "y": 3, "letra": "M", "editavel": True},
                    {"x": 2, "y": 4, "letra": "E", "editavel": True},
                    {"x": 2, "y": 5, "letra": "L", "editavel": True},
                    {"x": 2, "y": 6, "letra": "H", "editavel": True},
                    {"x": 2, "y": 7, "letra": "O", "editavel": True},
                ]
            }
        }
    )

    # 3. Ordena Letras
    ExercicioModelo.objects.get_or_create(
        sessao_modelo=sessao_modelo,
        numero=3,
        tipo='ordena_letras',
        defaults={
            'enunciado': 'Ordene as letras para descobrir os animais. Use as casas sombreadas para o animal oculto.',
            'configuracao': {
                "palavras": [
                    {"embaralhada": "ENERETPS", "resposta": "SERPENTE", "sombreadas": [2, 5]},
                    {"embaralhada": "OFHINGOL", "resposta": "GOLFINHO", "sombreadas": [1, 6]}
                ],
                "palavra_final": "TIGRE"
            }
        }
    )

    print(f"Seed completed successfully! Access the session at: /sessoes/{sessao_realizada.id}/")

if __name__ == '__main__':
    seed()
