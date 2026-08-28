from django.core.management.base import BaseCommand
import json
import os
from django.conf import settings

from exercicios.models import ExercicioModelo
from sessoes.models import SessaoModelo, Tema


class Command(BaseCommand):
    help = "Popula Tema, SessaoModelo e ExercicioModelo a partir de catalogo_gerado.json"

    def handle(self, *args, **options):
        # 1. Criação de Temas Padrão
        temas_padrao = [
            {
                "nome": "Estimulação & Formas",
                "descricao": "Exercícios de percepção visual, sombras, contornos e associação para primeira infância.",
                "cor": "#10B981",
                "icone": "bi-shapes"
            },
            {
                "nome": "Alfabetização & Linguagem",
                "descricao": "Consciência fonológica, anagramas, formação de palavras e ortografia.",
                "cor": "#3B82F6",
                "icone": "bi-fonts"
            },
            {
                "nome": "Raciocínio & Lógica",
                "descricao": "Problemas lógicos, identificação de intrusos, operações e categorização.",
                "cor": "#F59E0B",
                "icone": "bi-puzzle"
            },
            {
                "nome": "Cognição Abstrata & Enigmas",
                "descricao": "Pensamento lateral, metáforas, polissemia, dedução e sequências numéricas.",
                "cor": "#8B5CF6",
                "icone": "bi-lightbulb"
            },
            {
                "nome": "Piloto de Testes",
                "descricao": "Sessões experimentais para validação de interface e formatos.",
                "cor": "#64748B",
                "icone": "bi-flask"
            },
        ]

        temas_map = {}
        for t_info in temas_padrao:
            tema_obj, _ = Tema.objects.update_or_create(
                nome=t_info["nome"],
                defaults={
                    "descricao": t_info["descricao"],
                    "cor": t_info["cor"],
                    "icone": t_info["icone"],
                }
            )
            temas_map[t_info["nome"]] = tema_obj

        self.stdout.write(self.style.SUCCESS(f"{len(temas_padrao)} temas padrão configurados."))

        json_path = os.path.join(settings.BASE_DIR, 'catalogo_gerado.json')
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"Arquivo não encontrado: {json_path}"))
            return
            
        with open(json_path, 'r', encoding='utf-8') as f:
            exercicios_data = json.load(f)
            
        # Agrupar por faixa etária
        agrupamento = {}
        for ex in exercicios_data:
            faixa = ex.get('faixaEtaria', 'Geral')
            if faixa not in agrupamento:
                agrupamento[faixa] = []
            agrupamento[faixa].append(ex)
            
        # Mapeamento do engineType para os choices do ExercicioModelo
        engine_map = {
            "SINGLE_CHOICE": "multipla_escolha",
            "TRUE_FALSE": "verdadeiro_falso",
            "ANAGRAM_ORDER": "ordena_letras",
            "GAP_FILL": "preenche_lacunas_letras"
        }
            
        sessao_numero = 1
        for faixa, exercicios_lista in agrupamento.items():
            # Achar tema ideal baseado na faixa
            tema_obj = temas_map.get("Piloto de Testes")
            if "3 a 5" in faixa.lower():
                tema_obj = temas_map.get("Estimulação & Formas")
            elif "6 a 10" in faixa.lower():
                tema_obj = temas_map.get("Alfabetização & Linguagem")
            elif "11" in faixa.lower():
                tema_obj = temas_map.get("Cognição Abstrata & Enigmas")

            sessao_modelo, created = SessaoModelo.objects.update_or_create(
                numero=sessao_numero,
                defaults={
                    "titulo": f"Sessão Completa: {faixa}",
                    "descricao": f"Todos os exercícios da faixa etária {faixa}",
                    "objetivo": f"Desenvolver habilidades cognitivas adequadas para {faixa}.",
                    "faixa_etaria": faixa,
                    "tema": tema_obj,
                },
            )
            acao = "criada" if created else "atualizada"
            self.stdout.write(f"Sessão {sessao_modelo.numero} ({sessao_modelo.titulo}) [Tema: {tema_obj.nome}] {acao}.")

            for ex_data in exercicios_lista:
                # O ID é usado como numero do exercício dentro da sessão, 
                # como o ID já é único de 1 a 270, isso evita conflitos
                numero_ex = ex_data["id"]
                tipo_db = engine_map.get(ex_data.get("engineType"), "pergunta_aberta")
                
                ExercicioModelo.objects.update_or_create(
                    sessao_modelo=sessao_modelo,
                    numero=numero_ex,
                    defaults={
                        "tipo": tipo_db,
                        "enunciado": ex_data["prompt"],
                        "configuracao": ex_data,
                    },
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"  -> {len(exercicios_lista)} exercício(s) sincronizado(s)."
                )
            )
            sessao_numero += 1

        total_sessoes = SessaoModelo.objects.count()
        total_exercicios = ExercicioModelo.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Catálogo sincronizado: {total_sessoes} sessão(ões), {total_exercicios} exercício(s) no total."
            )
        )
