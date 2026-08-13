# Wireframes

Wireframes de baixa fidelidade das 10 telas principais do fluxo de atendimento, criados no Claude Design. O objetivo aqui é registrar a estrutura e o fluxo de navegação entre telas, não o visual final.

## Fluxo geral

```
1a Login
  -> 1b Lista de crianças
       -> 1c Cadastro de criança (volta pra 1b ao salvar)
       -> 1d Seleção de sessão
            -> sessão não feita -> 1e Seleção de exercício
                 -> exercício tipo pergunta -> 1f
                 -> exercício tipo jogo de palavras -> 1g
                 -> encerrar sessão -> 1h Resultado da sessão
                      -> 1i Histórico da criança
            -> sessão já concluída -> 1j Confirmar repetição
                 -> confirmar -> 1e
                 -> cancelar -> fecha modal, volta pra 1d
       -> abrir histórico direto -> 1i Histórico da criança
            -> "repetir" numa sessão antiga -> 1j
```

## Telas

### 1a. Login da terapeuta
Campos de e-mail e senha, botão "Entrar" e link "esqueci minha senha".

### 1b. Lista de crianças
Lista das crianças cadastradas com busca e botão "+ Nova criança". Cada card mostra nome e idade, com ação "Atender" (vai para 1d). Tocar no card (fora do botão) abre o histórico da criança (1i).

### 1c. Cadastro de criança
Formulário com nome completo e data de nascimento. A idade é calculada e exibida automaticamente (não é campo editável). Salvar volta para 1b.

### 1d. Seleção de sessão
Mostra o nome/idade da criança selecionada e um grid com as 10 sessões do catálogo, cada uma com tag "concluída" ou "não feita".
- Sessão não feita: abre a seleção de exercícios (1e).
- Sessão concluída: abre o modal de confirmação de repetição (1j), já que repetir apaga o resultado anterior.

### 1e. Seleção de exercício
Grid com os 9 exercícios da sessão escolhida, cada um com o tipo (pergunta ou jogo de palavras) e uma tag indicando se já foi feito. Sem ordem obrigatória, a terapeuta escolhe qualquer um. Botão "Encerrar sessão e ver resultado" leva para 1h a qualquer momento.

### 1f. Exercício: pergunta aberta
Mostra o enunciado (ex.: "diga 3 animais com a letra B") e campos para até 3 respostas. Mostra número da tentativa e tempo decorrido. Botão "Confirmar" registra o resultado e volta para 1e.

### 1g. Exercício: jogo de palavras
Exemplo de caça-palavras: grade de letras, lista de palavras a encontrar, botão de dica e contador de palavras encontradas / tempo. Botão "Concluir" registra o resultado e volta para 1e.

### 1h. Resultado da sessão
Mostra o % de acerto médio, tempo total e a lista de exercícios com o resultado individual (% e tentativas). Ações: exportar PDF da sessão ou ir para o histórico da criança (1i).

### 1i. Histórico da criança
Lista das sessões já realizadas (data e % de acerto), com ações "repetir" (abre 1j) e "PDF" por sessão, além de um botão de exportar relatório consolidado.

### 1j. Modal de confirmação de repetição
Avisa que o resultado anterior da sessão será apagado e substituído. Confirmar leva para 1e (seleção de exercícios da sessão); cancelar apenas fecha o modal.

## Observações / pontos que já bateram com a modelagem do banco

- A tag "concluída" / "não feita" em 1d e 1e reflete diretamente o status de `SessaoRealizada` e a existência de `ExercicioResultado`.
- Os campos "tentativas" e "tempo" em 1f/1g/1h confirmam os campos `tentativas`, `tempo_segundos` e `percentual_acerto` já definidos em `02-modelagem-bd.md`.
- O fluxo do modal 1j (apagar e substituir ao confirmar) é exatamente a regra de negócio decidida para repetição de sessão.
- A seleção de exercícios em grid, sem ordem fixa, confirma a necessidade do campo `ordem_execucao`.

## Pontos em aberto

- Tela de troca de criança durante o atendimento (mencionada como sugestão de próxima iteração no próprio wireframe, ainda não desenhada).
- Variação do jogo de organizar letras (só o caça-palavras foi detalhado até agora).
- Definir se o login (1a) já entra no MVP ou se a v1 roda com um único usuário fixo (sua mãe), já que o modelo de dados já prevê `Terapeuta` como `User` do Django.

## Fonte

Wireframes criados no Claude Design (handoff `Projeto LB Wireframes.dc.html`).
