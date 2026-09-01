# Sistema de Design — Projeto LB

Este documento registra as decisões de design visual do projeto, pra manter consistência conforme novas telas forem criadas (sessões, exercícios, histórico, relatórios). A ideia: escolher os valores uma vez, documentar o porquê, e reaproveitar — em vez de cada tela nova "inventar" espaçamento, cor ou raio de borda do zero.

Inspirado nos princípios de design system do repositório [interface-design](https://github.com/Dammyjay93/interface-design) (Craft · Memory · Consistency), adaptados manualmente aqui já que o projeto usa Django + templates, não Claude Code.

> **Atualização**: a direção visual abaixo substitui a paleta "azul-petróleo + coral" original. As telas foram prototipadas em alta fidelidade no [Stitch](https://stitch.withgoogle.com) (protótipo "Portal PsicoPedagógico Interativo") e implementadas em cima do CRUD/fluxo real já existente — os tokens deste documento agora refletem exatamente o que está em `templates/base.html`.

## Contexto de uso

Dois públicos usam a interface, com necessidades diferentes:
- **Terapeuta**: não muito envolvida com tecnologia — precisa de clareza, contraste bom, botões óbvios, sem elementos escondidos ou gestos complexos.
- **Criança**: em sessão de atendimento — não pode ser um visual que distrai ou cansa (nada muito saturado/gritante), mas também não pode ser frio/burocrático.

Isso empurrou as escolhas pro meio-termo: acolhedor mas sóbrio, nunca "infantilizado" a ponto de parecer bagunçado, nunca "corporativo" a ponto de parecer frio.

## Direção

**Personalidade**: "Acolhimento Clínico" — uma base off-white (reduz fadiga visual em sessões longas) com formas orgânicas e paleta suave, mas mantendo rigor profissional via grid estruturado e tipografia bem definida. Evita tanto o visual frio/corporativo quanto o infantilizado.

**Elevação**: sem sombras pesadas — profundidade vem de camadas tonais (fundo do sidebar mais escuro que o conteúdo) e bordas finas de 1px, não de `box-shadow` forte.

## Paleta de cores

| Papel | Uso | Hex |
|---|---|---|
| `--color-primary` | Ações principais, títulos, links, progresso | Verde-menta escuro `#246a51` |
| `--color-primary-container` | Fundo de botão primário, avatar/ícone de destaque | `#6baf92` |
| `--color-secondary` | Navegação ativa, foco de inputs | Azul cerúleo `#356287` |
| `--color-secondary-container` | Badge/estado "em andamento" | `#a8d3fe` |
| `--color-tertiary` | Progresso, acentos secundários | Lavanda `#63578a` |
| `--color-tertiary-container` | Ícone de exercícios, barra de progresso | `#a89ad2` |
| `--color-bg` | Fundo da página | Off-white `#f9f9f7` |
| `--color-surface` | Fundo de cards/inputs | `#ffffff` |
| `--color-surface-container-low/high` | Sidebar, tonal layers | `#f4f4f2` / `#e8e8e6` |
| `--color-text` / `--color-text-muted` | Texto principal / secundário | `#1a1c1b` / `#3f4944` |
| `--color-error` / `--color-error-container` | Deletar, alerta | `#ba1a1a` / `#ffdad6` |

**Regra**: os tipos de exercício não ganham cor própria de marca — usam a mesma paleta acima (ícone por tipo, ver `sessoes/views.py::ICONE_POR_TIPO`), mantendo o visual previsível independente do exercício.

## Tokens

### Tipografia
- **Quicksand** (600/700) para títulos — terminações arredondadas, aproximável para crianças.
- **Nunito Sans** (400/700) para corpo de texto e rótulos — legibilidade alta para a terapeuta.
- Carregadas via Google Fonts (`templates/base.html`), junto com o ícone **Material Symbols Outlined**.

### Espaçamento
Generoso — prioriza respiro visual sobre densidade de informação por tela (`gap-3`/`gap-4`, `p-4`/`p-md-5`).

### Raio de borda
- `--radius-card`: `1rem` — cards de conteúdo.
- `--radius-control`: `0.5rem` — inputs, ícones em caixa.
- `--radius-pill`: `9999px` — botões (`.btn`), badges de status.

### Profundidade (sombra vs. borda)
- **Cards**: borda de 1px (`--color-border` = `#bfc9c2`), sem sombra em repouso; sombra suave só no `:hover` (`--shadow-card`).
- **Inputs**: borda sólida de 1px, engrossa pra 2px + anel azul no `:focus` — sem sombra decorativa.

## Layout — casca do app (sidebar + topo + navegação inferior)

Toda tela autenticada (exceto login) usa a casca definida em `templates/base.html`:
- **Sidebar** (desktop, ≥768px): logo, navegação (Crianças / Sessões / Histórico / Configurações) e CTA "Nova Sessão" (só aparece com uma criança no contexto).
- **Barra superior**: breadcrumbs simples (Dashboard/Histórico) + usuário + Sair.
- **Navegação inferior** (mobile, <768px): mesmos 4 itens da sidebar, sidebar escondida.

A view passa `active` (`'criancas' | 'sessoes' | 'historico'`) e, quando aplicável, `crianca` no contexto — isso é o que liga os links "Sessões"/"Histórico" da sidebar à criança certa.

## Padrões (componentes)

### Card de item (criança, sessão, exercício)
- `.card-item`: borda 1px + `--radius-card`, sem sombra em repouso, eleva levemente no hover.
- Padding interno generoso (`p-4` a `p-md-5`).

### Avatar circular (inicial do nome)
- 56–88px conforme o contexto, círculo com a inicial do nome em `Quicksand` sobre `--color-surface-container-high`.

### Botão primário — `.btn-coral`
O nome da classe é histórico (era coral, hoje resolve pro verde-menta `--color-primary-container`) e é reutilizado tanto nos templates quanto no JS do motor de exercícios (`templates/sessoes/exercicios_components.html`) — **não renomear sem atualizar os dois lugares**.

### Botão secundário / de perigo
- Secundário: `.btn-outline-primary`, borda 2px, sem preenchimento.
- Perigo: outline vermelho na listagem, preenchido (`.btn-danger`) só na tela de confirmação — reforça que a confirmação é o ponto de não-retorno.

### Badges de status
Pílula com peso 700, cor por estado: `primary-container` (concluída/feito), `secondary-container` (em andamento/continuar), `surface-container-high` (pendente/não feita), `error-container` (abaixo de 50% de acerto).

## Botões — alvo de toque

Todo `.btn` tem `min-height: 44px` (WCAG, pensando em uso em tablet) e feedback tátil (`scale(0.97)` no `:active`).

## Ordem de botões em confirmação destrutiva

Em qualquer confirmação (deletar criança, repetir sessão), o botão de cancelar/voltar vem **antes** da ação na ordem visual esquerda→direita — reduz risco de ação acidental num público sem muita intimidade com tecnologia.

## Estados de formulário

Campos usam `.form-control`/`.form-select` explícitos, renderizados campo a campo (não `{{ form.as_p }}`), com label, texto de ajuda e lista de erros própria (`.form-errors`). Foco usa anel na cor secundária (`--color-secondary`), não o azul padrão do Bootstrap.

## Fluxo de exercícios (sessão)

A sessão é um fluxo único e contínuo: todos os exercícios da sessão são renderizados em sequência numa mesma página (`sessoes:sessao_detail`), reaproveitando o motor de renderização já existente (`ExerciseRenderers` em `exercicios_components.html`). Cada "Verificar" só atualiza o estado local (JS) — nada é salvo no servidor até o clique em "Enviar sessão", no rodapé. Se tudo estiver certo (regra: `percentual_acerto == 100` por exercício), a sessão é marcada como concluída; se algo estiver errado, as respostas são salvas mesmo assim e a criança é levada de volta ao primeiro exercício errado (destacado em vermelho) para tentar de novo. Ver issue #28 e `docs/03-wireframes.md` (fluxo 1a–1j, desatualizado quanto à tela por exercício).

## Pendências / próximas decisões

- [x] Paleta, tipografia e ícones migrados para o sistema "Acolhimento Clínico" (protótipo Stitch).
- [x] Telas de seleção de sessão/exercício, resultado da sessão, histórico da criança e confirmação de repetição implementadas com dados reais.
- [ ] Padronizar `.btn-sm` (40px, usado nos ícones de editar/deletar do card de criança) para 44px se o uso em tablet mostrar necessidade.
- [ ] Tipos de exercício `cruzadinha` e `preenche_lacunas_letras` ainda não têm dados reais cadastrados para validar visualmente (só piloto com os outros 6 tipos).

---
*Última atualização: migração da identidade visual para o protótipo Stitch ("Acolhimento Clínico"), com telas de resultado, histórico e repetição de sessão conectadas ao backend real.*
