# Projeto LB — App de Sessões Terapêuticas Infantis

> Aplicação web para apoiar sessões de atendimento psicopedagógico/terapêutico infantil, permitindo que a terapeuta conduza a criança por sessões de exercícios interativos, acompanhe o desempenho e exporte relatórios em PDF.

Projeto desenvolvido em parceria com Guilherme Leite, a partir de uma necessidade real: digitalizar o material de atendimento usado pela minha mãe (terapeuta) com crianças, tanto em atendimentos presenciais (tablet) quanto online (computador).

## Status do projeto

Em desenvolvimento — modelagem do banco de dados concluída, migrations aplicadas e admin configurado para os models principais. CRUD completo de Criança implementado. Fluxo de atendimento funcionando de ponta a ponta: escolher criança → escolher sessão → responder exercícios → salvar resultado → exportar relatório em PDF (por sessão e consolidado). Cinco tipos de exercício com correção e salvamento de resultado implementados (pergunta aberta, múltipla escolha, verdadeiro/falso, caça-palavras, organizar letras).

Pendências conhecidas: as 10 sessões reais ainda não foram cadastradas — hoje existe só um piloto com conteúdo de teste (inventado, não copiado do material da terapeuta), aguardando ela avaliar o formato antes de entrarmos com o conteúdo definitivo. O fluxo de correção também precisa de revisão: cada exercício salva seu resultado individualmente ao ser verificado, mas o ideal é um envio único no fim da sessão que só marca como concluída se tudo estiver certo (ver issues abertas no repositório).

## Funcionalidades principais

- Cadastro de crianças (nome + data de nascimento, com cálculo automático de idade em anos/meses)
- Suporte a múltiplas crianças, com troca entre atendimentos
- Fluxo de atendimento: escolher criança → escolher sessão → responder exercícios
- 10 sessões com 9 exercícios cada, sem ordem obrigatória — a terapeuta escolhe (catálogo real ainda em construção)
- Cinco tipos de exercício com correção automática: pergunta aberta, múltipla escolha, verdadeiro/falso, caça-palavras e organizar letras
- Registro de desempenho por exercício: % de acerto, número de tentativas, tempo e pontuação
- Histórico de desempenho por criança e por sessão
- Exportação de relatórios em PDF (por sessão e consolidado, com tempo total por sessão)

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
├── config/               # settings, urls e configuração raiz do Django
├── criancas/             # app: cadastro e CRUD de crianças
├── sessoes/              # app: catálogo de sessões, fluxo de atendimento e relatórios
│   ├── catalogo_data.py         # conteúdo das sessões/exercícios
│   └── management/commands/     # seed_catalogo: popula o catálogo a partir de catalogo_data.py
├── exercicios/           # app: exercícios (pergunta aberta, múltipla escolha, verdadeiro/falso, caça-palavras, organizar letras)
├── templates/
│   ├── sessoes/          # tela de sessão e renderizadores JS dos exercícios
│   └── relatorios/       # templates dos relatórios em PDF
├── docs/                 # documentação do processo de desenvolvimento
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
python manage.py seed_catalogo  # popula o catálogo de sessões/exercícios (piloto)
python manage.py runserver
```

**Windows**: a geração de PDF (WeasyPrint) depende do runtime nativo do GTK3
(Pango/GObject), que não vem com o `pip install`. Instale o [GTK+ for Windows
Runtime Environment](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)
(ou `winget install tschoonj.GTKForWindows`) e abra um terminal novo depois —
o instalador já ajusta o PATH do sistema. No Linux, `apt-get install
libpango-1.0-0 libpangoft2-1.0-0` costuma bastar.

## Equipe

- Daniel Nathan — [GitHub](https://github.com/Danithan)
- Guilherme Leite — [GitHub](https://github.com/Guilherme-Leite1701)

## Motivação

Este projeto nasceu como forma de praticar o ciclo completo de desenvolvimento de software (levantamento de requisitos → design → implementação → testes), aplicando os conhecimentos do curso de ADS em um caso de uso real e com propósito social.
