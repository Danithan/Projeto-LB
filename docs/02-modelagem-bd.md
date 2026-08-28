# Modelagem do Banco de Dados

Este documento descreve as entidades principais do Projeto LB, seus campos e relacionamentos, servindo de base para os models do Django.

## Visão geral das entidades

- **Crianca**: cadastro de cada criança atendida.
- **Tema**: categorização temática visual das sessões (ex.: Estimulação & Formas, Alfabetização & Linguagem).
- **SessaoModelo**: o "catálogo" das sessões (nomenclatura, objetivo terapêutico, tema e faixa etária recomendada).
- **ExercicioModelo**: os exercícios de cada sessão do catálogo.
- **SessaoRealizada**: registro de que uma criança passou (ou está passando) por uma sessão específica, em uma data específica. É aqui que entra o histórico.
- **ExercicioResultado**: o desempenho da criança em cada exercício dentro de uma sessão realizada (% de acerto, tentativas, tempo, pontuação).

A ideia central: **Tema/SessaoModelo/ExercicioModelo são o conteúdo fixo e estrutural** (definido uma vez, reaproveitado para todas as crianças), enquanto **SessaoRealizada/ExercicioResultado são o histórico real de atendimento** de cada criança.

## Entidades

### Tema

| Campo | Tipo | Observações |
|---|---|---|
| id | PK | |
| nome | CharField (unique) | Ex.: "Alfabetização & Linguagem", "Raciocínio & Lógica" |
| descricao | TextField | opcional |
| cor | CharField | código HEX para identificação visual e badges |
| icone | CharField | classe de ícone Bootstrap (ex.: bi-shapes, bi-fonts) |
| criado_em | DateTimeField (auto) | |

### Terapeuta

Usa o `User` padrão do Django (com `AbstractUser` ou um `Profile` associado, se precisar de campos extras como CRP/registro profissional). Cada `SessaoRealizada` passa a ter um FK para o terapeuta responsável.

### Crianca

| Campo | Tipo | Observações |
|---|---|---|
| id | PK | |
| nome | CharField | |
| data_nascimento | DateField | idade em anos/meses é calculada, não armazenada |
| criada_em | DateTimeField (auto) | |
| ativa | BooleanField | default True, permite "arquivar" sem apagar histórico |

### SessaoModelo

| Campo | Tipo | Observações |
|---|---|---|
| id | PK | |
| numero | IntegerField | 1 a 10 (ou números de teste no piloto) |
| titulo | CharField | Nomenclatura oficial da sessão |
| objetivo | TextField | Objetivo pedagógico e meta terapêutica |
| descricao | TextField | opcional |
| faixa_etaria | CharField | Recomendação etária (3 a 5 anos, 6 a 10 anos, 11+ anos) |
| tema | FK -> Tema | Categoria temática da sessão (opcional/SET_NULL) |

### ExercicioModelo

| Campo | Tipo | Observações |
|---|---|---|
| id | PK | |
| sessao_modelo | FK -> SessaoModelo | |
| numero | IntegerField | 1 a 9, dentro da sessão |
| tipo | CharField (choices) | `pergunta_aberta` ou `jogo_palavras` |
| enunciado | TextField | ex.: "diga 3 animais com a letra B" |
| configuracao | JSONField | dados específicos do tipo (ex.: lista de letras do caça-palavras, palavra a organizar, categoria esperada) |

O campo `configuracao` em JSON evita criar uma tabela separada para cada tipo de jogo agora. Se no futuro surgirem muitos tipos com regras muito diferentes, dá para migrar para tabelas específicas por tipo.

### SessaoRealizada

| Campo | Tipo | Observações |
|---|---|---|
| id | PK | |
| crianca | FK -> Crianca | |
| sessao_modelo | FK -> SessaoModelo | qual sessão do catálogo foi usada |
| terapeuta | FK -> User | quem conduziu a sessão |
| data | DateTimeField | quando ocorreu |
| status | CharField (choices) | `em_andamento`, `concluida` |
| observacoes | TextField | anotações livres da terapeuta, opcional |

### ExercicioResultado

| Campo | Tipo | Observações |
|---|---|---|
| id | PK | |
| sessao_realizada | FK -> SessaoRealizada | |
| exercicio_modelo | FK -> ExercicioModelo | qual exercício do catálogo |
| ordem_execucao | IntegerField | ordem em que a criança realmente fez o exercício, já que não há ordem obrigatória |
| percentual_acerto | DecimalField/FloatField | |
| tentativas | IntegerField | |
| tempo_segundos | IntegerField | |
| pontuacao | IntegerField | |
| respondido_em | DateTimeField (auto) | |

## Relacionamentos (resumo)

```
Crianca (1) ----- (N) SessaoRealizada (N) ----- (1) SessaoModelo
                        |
                        (1)
                        |
                        (N)
              ExercicioResultado
                        |
                        (N)
                        |
                        (1)
              ExercicioModelo (N) ----- (1) SessaoModelo
```

## Decisões tomadas

1. **Terapeuta é um usuário do sistema.** Resolvido acima com o FK para `User` em `SessaoRealizada`.
2. **Ordem livre dos exercícios.** Resolvido acima com o campo `ordem_execucao` em `ExercicioResultado`.
3. **Repetir uma sessão para a mesma criança.** Deve ser permitido, mas exige apagar o resultado salvo antes, passando por uma tela de confirmação. Isso é regra de negócio na camada de aplicação (view/service), não muda o schema: ao confirmar a repetição, a view apaga (ou marca como substituída) a `SessaoRealizada` anterior e cria uma nova. Se no futuro quiser manter as duas no histórico em vez de apagar, dá pra trocar por um campo `substituida_por` (self-FK) em vez de deletar de verdade.
4. **Relatório consolidado.** Confirmado: gerado sob demanda a partir de consultas em `SessaoRealizada` + `ExercicioResultado`, sem tabela própria. Se mais pra frente for necessário manter histórico dos PDFs já exportados, cria-se uma entidade `RelatorioGerado` nessa hora.

## Próximo passo

Com esse modelo validado, o próximo passo é traduzir isso para `models.py` do Django (apps sugeridos: `criancas`, `sessoes`, `exercicios`) e gerar as migrations iniciais.
