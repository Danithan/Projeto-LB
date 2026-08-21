# Sistema de Design — Projeto LB

Este documento registra as decisões de design visual do projeto, pra manter consistência conforme novas telas forem criadas (sessões, exercícios, histórico, relatórios). A ideia: escolher os valores uma vez, documentar o porquê, e reaproveitar — em vez de cada tela nova "inventar" espaçamento, cor ou raio de borda do zero.

Inspirado nos princípios de design system do repositório [interface-design](https://github.com/Dammyjay93/interface-design) (Craft · Memory · Consistency), adaptados manualmente aqui já que o projeto usa Django + templates, não Claude Code.

## Contexto de uso

Dois públicos usam a interface, com necessidades diferentes:
- **Terapeuta**: não muito envolvida com tecnologia — precisa de clareza, contraste bom, botões óbvios, sem elementos escondidos ou gestos complexos.
- **Criança**: em sessão de atendimento — não pode ser um visual que distrai ou cansa (nada muito saturado/gritante), mas também não pode ser frio/burocrático.

Isso empurrou as escolhas pro meio-termo: acolhedor mas sóbrio, nunca "infantilizado" a ponto de parecer bagunçado, nunca "corporativo" a ponto de parecer frio.

## Direção

**Personalidade**: Acolhimento com presença — espaçamento generoso e cantos arredondados (acolhedor), mas com contraste de cor mais forte que o usual pra garantir clareza visual pra quem não tem intimidade com tecnologia.

**Referência mais próxima** (dos direcionamentos do interface-design): *Warmth & Approachability* (espaçamento generoso, sombras suaves), com um pouco mais de contraste de cor puxado de *Boldness & Clarity*.

## Paleta de cores

| Papel | Cor | Hex |
|---|---|---|
| Primária (ações principais, títulos, links) | Azul-petróleo | `#2D6E7E` |
| Destaque (ações de sucesso/criar, elementos de atenção positiva) | Coral | `#FF6F61` |
| Fundo da página | Cinza-azulado bem claro | `#F5F9FA` |
| Perigo (deletar, avisos) | Vermelho Bootstrap padrão (`btn-danger`) | — |

**Regra**: os tipos de exercício (pergunta aberta, caça-palavras, organizar letras) **não** ganham cor própria — usam a mesma paleta acima em todas as telas. Mantém o visual previsível independente de qual exercício a criança está fazendo.

**Sem emojis/ícones decorativos** — visual limpo, texto e cor fazem o trabalho de comunicar hierarquia.

## Tokens

### Espaçamento
Generoso — prioriza respiro visual sobre densidade de informação por tela. Na prática (classes Bootstrap já usadas): `mb-4`, `mb-5`, `p-4`, `gap-3`/`gap-4`.

### Raio de borda
Moderado — 8 a 12px. Nem reto (frio demais), nem "pill" total (infantilizado demais).
- Cards: `border-radius: 12px` (ou `20px` nos cards de destaque tipo listagem de crianças, avaliar caso a caso)
- Botões: `border-radius: 50px` (formato pílula) — decisão já tomada nos botões existentes, mantida como exceção intencional pro elemento de ação principal

### Profundidade (sombra vs. borda)
Mistura, dependendo do elemento:
- **Cards de conteúdo** (crianças, sessões, exercícios): sombra suave (`box-shadow: 0 4px 14px rgba(0,0,0,0.08)`), sem borda visível — sensação de "flutuar"
- **Elementos de formulário/inputs**: borda sólida simples (padrão Bootstrap), sem sombra — foco em clareza de onde clicar/digitar

### Tipografia
`'Segoe UI', system-ui, sans-serif` — fonte do sistema, sem carregar fonte externa (mantém carregamento rápido, importante pra uso em tablet).

## Padrões (componentes)

### Card de item (ex.: criança, sessão)
- Borda: nenhuma
- Raio: 12–20px
- Sombra: `0 4px 14px rgba(0,0,0,0.08)`, com hover elevando pra `0 10px 24px rgba(0,0,0,0.14)` + leve translação pra cima (`translateY(-4px)`)
- Padding interno: `p-4`
- Uso: listagem de crianças (grid de cards), e deve se repetir nas próximas listagens (sessões, histórico)

### Avatar circular (inicial do nome)
- 56x56px, círculo, texto centralizado, cor de fundo em gradiente laranja/coral
- Uso: ao lado do nome em cards de listagem, pra dar identidade visual rápida sem depender de foto

### Botão primário (ação de criar/salvar)
- Formato pílula (`border-radius: 50px`)
- Cor: verde Bootstrap (`btn-success`) pra ações de criar/salvar — considerar migrar pro coral (`#FF6F61`) como cor de destaque própria do projeto, ainda pendente de decisão
- Padding generoso: `px-4 py-2`

### Botão secundário (editar, cancelar)
- Mesmo formato pílula
- Outline, não preenchido (`btn-outline-primary`, `btn-outline-secondary`)

### Botão de perigo (deletar)
- Outline vermelho (`btn-outline-danger`) na listagem; preenchido (`btn-danger`) na tela de confirmação — reforça que a confirmação é o ponto de não-retorno

## Tokens CSS (implementação)

Desde a refinação do CRUD de Criança, a paleta e a escala de raio/sombra deixaram de existir só como valores soltos no `<style>` de `templates/base.html` e passaram a ser variáveis CSS em `:root`, reaproveitáveis por qualquer tela nova (sessões, exercícios, histórico):

```css
--color-primary       /* #2D6E7E — ações principais, títulos, links */
--color-accent        /* #FF6F61 — ação de criar/salvar */
--color-bg            /* #F5F9FA — fundo da página */
--color-text / --color-text-muted
--radius-card          /* 12px */
--radius-control       /* 8px — inputs */
--radius-pill          /* 50px — botões */
--shadow-card / --shadow-card-hover
```

Telas novas devem consumir essas variáveis em vez de repetir hex/px soltos.

## Botões — alvo de toque

Todo `.btn` tem `min-height: 44px` (WCAG, pensando em uso em tablet pela terapeuta) e feedback tátil (`scale(0.97)` no `:active`). `.btn-sm` (usado nos cards da listagem) fica em 40px — abaixo do ideal, mas aceitável para ações secundárias (Editar/Deletar) dentro de um card já compacto.

## Ordem de botões em confirmação destrutiva

Na tela de confirmar exclusão, o botão "Cancelar" vem **antes** do "Deletar" (nessa ordem, da esquerda pra direita) — a ação mais segura fica na posição que o usuário toca primeiro/por hábito, reduzindo risco de exclusão acidental num público que não tem intimidade com tecnologia. O botão "Deletar" continua preenchido em vermelho (`btn-danger`) pra não perder a clareza de que é uma ação de risco.

## Estados de formulário

Os campos do `CriancaForm` usam `form-control` explícito no widget (Bootstrap não estiliza `<input>` sozinho) e são renderizados campo a campo no template (não `{{ form.as_p }}`), com label, texto de ajuda e lista de erros próprios (`.form-errors`) — abre espaço pra customizar cada campo conforme os próximos formulários (sessão, exercício) forem criados. O foco dos inputs usa anel na cor primária (`--color-primary`) em vez do azul padrão do Bootstrap, pra manter a paleta consistente.

## Pendências / próximas decisões

- [x] Cor dos botões de ação já usa coral (`#FF6F61`) via `.btn-coral` — paleta e código estavam alinhados, item fechado.
- [x] Raio dos cards padronizado em 12px (`--radius-card`) — não existe mais nenhuma classe `.card-crianca` com 20px no código.
- [x] `<input type="date">` estilizado junto dos demais campos via `.form-control` + `--radius-control`.
- [ ] Definir estilo visual das telas de sessão e exercício (ainda não construídas) seguindo os mesmos tokens deste documento.
- [ ] Avaliar se `.btn-sm` (40px) nos cards da listagem deveria virar tamanho padrão (44px) conforme o uso real em tablet for testado com a terapeuta.

---
*Última atualização: refinação de craft do CRUD de Criança (tokens CSS, formulário campo a campo, estado vazio, ordem de botões destrutivos)*
