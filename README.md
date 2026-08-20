# Projeto LB — App de Sessões Terapêuticas Infantis

> Aplicação web para apoiar sessões de atendimento psicopedagógico/terapêutico infantil, permitindo que a terapeuta conduza a criança por sessões de exercícios interativos, acompanhe o desempenho e exporte relatórios em PDF.

Projeto desenvolvido em parceria com Guilherme Leite, a partir de uma necessidade real: digitalizar o material de atendimento usado pela minha mãe (terapeuta) com crianças, tanto em atendimentos presenciais (tablet) quanto online (computador).

## Status do projeto

Em desenvolvimento — modelagem do banco de dados concluída e todas as migrations aplicadas (`criancas`, `sessoes`, `exercicios`). Admin configurado para os models principais. CRUD completo de Criança implementado (listar, cadastrar, editar, deletar), com cálculo automático de idade e estilização inicial via Bootstrap + sistema de design próprio. Próximas etapas: popular catálogo de sessões/exercícios via admin, e construir o fluxo de escolha de criança → sessão.

## Funcionalidades principais

- Cadastro de crianças (nome + data de nascimento, com cálculo automático de idade em anos/meses)
- Suporte a múltiplas crianças, com troca entre atendimentos
- 10 sessões com 9 exercícios cada, sem ordem obrigatória — a terapeuta escolhe
- Dois tipos de exercício: perguntas abertas/categoria (ex.: "diga 3 animais com a letra B") e jogos de palavras (caça-palavras, organizar letras)
- Registro de desempenho por exercício: % de acerto, número de tentativas, tempo e pontuação
- Histórico de desempenho por criança e por sessão
- Exportação de relatórios em PDF (por sessão e consolidado)

## Stack tecnológica

| Camada | Tecnologia |
|---|---|
| Back-end | Django |
| Front-end (páginas) | Templates do Django + HTML/CSS |
| Interatividade dos jogos | JavaScript (Vanilla JS) |
| Banco de dados (desenvolvimento) | SQLite |
| Banco de dados (produção, futuro) | PostgreSQL |
| Geração de PDF | WeasyPrint |
| Estilização | Bootstrap + CSS customizado |

Justificativa completa das escolhas em [`docs/decisoes-tecnicas.md`](./docs/decisoes-tecnicas.md).

## Estrutura do projeto

```
Projeto-LB/
├── config/          # settings, urls e configuração raiz do Django
├── criancas/        # app: cadastro e CRUD de crianças
├── sessoes/         # app: catálogo de sessões e fluxo de atendimento
├── exercicios/      # app: exercícios (pergunta aberta, caça-palavras, organizar letras)
├── templates/        # templates base compartilhados entre apps
├── docs/            # documentação do processo de desenvolvimento
├── manage.py
├── requirements.txt
└── README.md
```

## Documentação do processo

Todo o processo de desenvolvimento — do levantamento de requisitos até as decisões técnicas — está documentado na pasta [`docs/`](./docs):

- [`01-requisitos.md`](./docs/01-requisitos.md) — documento de requisitos funcionais e não funcionais
- [`decisoes-tecnicas.md`](./docs/decisoes-tecnicas.md) — registro de decisões e justificativas
- [`02-modelagem-bd.md`](./docs/02-modelagem-bd.md) — modelagem do banco de dados
- [`03-wireframes.md`](./docs/03-wireframes.md) — telas do aplicativo
- [`design-system.md`](./docs/design-system.md) — sistema de design (paleta, espaçamento, componentes)

## Como executar localmente

```bash
git clone https://github.com/Danithan/Projeto-LB.git
cd Projeto-LB
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Equipe

- Daniel Nathan — [GitHub](https://github.com/Danithan)
- Guilherme Leite — [GitHub](https://github.com/Guilherme-Leite1701)

## Motivação

Este projeto nasceu como forma de praticar o ciclo completo de desenvolvimento de software (levantamento de requisitos → design → implementação → testes), aplicando os conhecimentos do curso de ADS em um caso de uso real e com propósito social.
