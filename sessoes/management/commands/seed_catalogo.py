from django.core.management.base import BaseCommand

from exercicios.models import ExercicioModelo
from sessoes.catalogo_data import SESSOES
from sessoes.models import SessaoModelo


class Command(BaseCommand):
    help = "Popula SessaoModelo e ExercicioModelo a partir de sessoes/catalogo_data.py"

    def handle(self, *args, **options):
        if not SESSOES:
            self.stdout.write(self.style.WARNING("SESSOES está vazio em sessoes/catalogo_data.py — nada a fazer."))
            return

        for sessao_data in SESSOES:
            sessao_modelo, created = SessaoModelo.objects.update_or_create(
                numero=sessao_data["numero"],
                defaults={
                    "titulo": sessao_data["titulo"],
                    "descricao": sessao_data.get("descricao", ""),
                },
            )
            acao = "criada" if created else "atualizada"
            self.stdout.write(f"Sessão {sessao_modelo.numero} ({sessao_modelo.titulo}) {acao}.")

            for exercicio_data in sessao_data.get("exercicios", []):
                ExercicioModelo.objects.update_or_create(
                    sessao_modelo=sessao_modelo,
                    numero=exercicio_data["numero"],
                    defaults={
                        "tipo": exercicio_data["tipo"],
                        "enunciado": exercicio_data["enunciado"],
                        "configuracao": exercicio_data.get("configuracao", {}),
                    },
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"  -> {len(sessao_data.get('exercicios', []))} exercício(s) sincronizado(s)."
                )
            )

        total_sessoes = SessaoModelo.objects.count()
        total_exercicios = ExercicioModelo.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Catálogo sincronizado: {total_sessoes} sessão(ões), {total_exercicios} exercício(s) no total."
            )
        )
