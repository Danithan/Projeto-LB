# Documento de Requisitos

**App de Sessões Terapêuticas Infantis**

## 1. Visão Geral

Aplicação web para uso em sessões de atendimento psicopedagógico/terapêutico infantil. Permite que a terapeuta (usuária principal) conduza a criança através de sessões de exercícios, acompanhe o desempenho e exporte relatórios em PDF.

## 2. Atores

- **Criança (Aluno)**: executa os exercícios e jogos, sob supervisão da terapeuta.
- **Terapeuta**: supervisiona a sessão, cadastra crianças, acompanha desempenho e exporta relatórios.

## 3. Requisitos Funcionais (RF)

| Código | Descrição |
|---|---|
| RF01 | Cadastrar uma criança com nome e data de nascimento. |
| RF02 | Calcular e exibir automaticamente a idade da criança em anos + meses, a partir da data de nascimento. |
| RF03 | Suportar múltiplas crianças cadastradas, com troca entre atendimentos. |
| RF04 | Organizar o conteúdo em 10 sessões, cada uma com 9 exercícios, sem ordem obrigatória (a terapeuta escolhe qual sessão aplicar). |
| RF05 | Suportar ao menos dois tipos de exercício/jogo: (a) pergunta aberta/categoria (ex.: "diga 3 animais com a letra B"); (b) jogo de palavras (caça-palavras, organizar letras para formar uma palavra). |
| RF06 | Registrar, por exercício realizado: percentual de acerto, número de tentativas, tempo gasto e pontuação. |
| RF07 | Calcular a pontuação com base em tempo e percentual de acerto (fórmula exata ainda pendente de definição com a terapeuta). |
| RF08 | Permitir que a terapeuta visualize o histórico de desempenho por criança e por sessão. |
| RF09 | Permitir que a terapeuta exporte/baixe um relatório em PDF com os resultados de uma sessão específica. |
| RF10 | Permitir que a terapeuta exporte/baixe um relatório em PDF consolidado, somando os resultados de todas as sessões realizadas pela criança. |

## 4. Requisitos Não Funcionais (RNF)

| Código | Descrição |
|---|---|
| RNF01 | Interface simples e visual, adequada para uso por crianças (fontes grandes, poucos elementos por tela). |
| RNF02 | Layout responsivo, funcionando tanto em tablet quanto em computador. |
| RNF03 | Aplicação web on-line; requer conexão com internet para uso (uso offline foi descartado). |
| RNF04 | Capacidade de geração de documentos em PDF a partir dos dados armazenados. |

## 5. Regras de Negócio

- As sessões podem ser realizadas em qualquer ordem; é a terapeuta quem decide qual sessão a criança fará em cada atendimento.
- A pontuação é calculada com base em tempo gasto e percentual de acerto, mas a fórmula exata ainda não foi definida (pendência).
- A terapeuta pode alternar entre diferentes crianças cadastradas de um atendimento para outro.
- O sistema funciona em modo on-line; não há suporte a uso offline.

## 6. Pendências / Pontos Abertos

- Definir a fórmula exata de cálculo da pontuação (peso de acertos vs. tempo).
- Definir a stack tecnológica a ser utilizada no desenvolvimento.
- Definir o layout/wireframes das telas.
- Definir a modelagem do banco de dados.
