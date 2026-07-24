# Projeto LB — App de Sessões Terapêuticas Infantis

> Aplicação web para apoiar sessões de atendimento psicopedagógico/terapêutico infantil, permitindo que a terapeuta conduza a criança por sessões de exercícios interativos, acompanhe o desempenho e exporte relatórios em PDF.

Projeto desenvolvido em parceria com Guilherme Leite, a partir de uma necessidade real: digitalizar o material de atendimento usado pela minha mãe (terapeuta) com crianças, tanto em atendimentos presenciais (tablet) quanto online (computador).

## Status do projeto

Em desenvolvimento — atualmente na fase de **modelagem do banco de dados / wireframes**.

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
| Estilização | CSS puro / Bootstrap |

Justificativa completa das escolhas em [`docs/decisoes-tecnicas.md`](./docs/decisoes-tecnicas.md).

## Documentação do processo

Todo o processo de desenvolvimento — do levantamento de requisitos até as decisões técnicas — está documentado na pasta [`docs/`](./docs):
 
- [`01-requisitos.md`](./docs/01-requisitos.md) — documento de requisitos funcionais e não funcionais
- [`decisoes-tecnicas.md`](./docs/decisoes-tecnicas.md) — registro de decisões e justificativas
- `02-modelagem-bd.md` — modelagem do banco de dados *(em breve)*
- `03-wireframes/` — telas do aplicativo *(em breve)*

## Como executar localmente

> Instruções serão adicionadas conforme a stack for definida e o projeto avançar.

## Equipe

- Daniel Nathan — [Github](https://github.com/Danithan)
- Guilherme Leite — [A definir]

## Motivação

Este projeto nasceu como forma de praticar o ciclo completo de desenvolvimento de software (levantamento de requisitos → design → implementação → testes), aplicando os conhecimentos do curso de ADS em um caso de uso real e com propósito social.
