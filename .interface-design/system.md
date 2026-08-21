# Projeto LB — Sistema de Interface

Fonte de verdade completa: `docs/design-system.md` (documento do próprio projeto, já existia antes deste skill e continua sendo o lugar certo para novas decisões). Este arquivo é só um resumo operacional pro skill de interface-design.

## Direção
"Acolhimento com presença" — espaçamento generoso, cantos arredondados, mas contraste de cor mais forte que o usual (dois públicos: terapeuta pouco tech-savvy em tablet, e criança em sessão — nada cansativo/gritante, nada frio/burocrático).

## Stack
Django templates + Bootstrap 5 (CDN), sem framework JS, sem build step. Tokens vivem como CSS custom properties em `templates/base.html` (`:root`).

## Depth strategy
Sombra suave nos cards (`--shadow-card` / `--shadow-card-hover`), sem sombra nos inputs (borda sólida simples). Não misturar as duas.

## Paleta (ver docs/design-system.md para a tabela completa)
- `--color-primary` `#2D6E7E` — ações principais, títulos, links
- `--color-accent` `#FF6F61` — criar/salvar
- `--color-bg` `#F5F9FA`
- Perigo: `btn-danger`/`text-danger` padrão Bootstrap

## Raio
`--radius-card` 12px · `--radius-control` 8px (inputs) · `--radius-pill` 50px (botões)

## Componentes-chave
- **Card de item** (`.card-item`): sem borda, `--radius-card`, `--shadow-card`, hover `translateY(-4px)` + `--shadow-card-hover`.
- **Avatar circular**: 56×56px, iniciais, fundo `--color-accent`.
- **Botões** (`.btn`): pílula, `min-height: 44px` (40px em `.btn-sm`), `scale(0.97)` no `:active`.
- **Formulário**: campo a campo (não `as_p`), `.form-field` + `.form-label` + `.form-errors`, foco com anel na cor primária.
- **Estado vazio** (`.empty-state`): borda tracejada, título + texto + CTA — não um `<p>` solto.

## Convenção de segurança
Em confirmações destrutivas, "Cancelar" vem antes de "Deletar" na ordem visual (esquerda → direita), reduzindo risco de toque acidental num público não-tech em tablet.

## Pendências conhecidas
Telas de sessão/exercício ainda não construídas — devem herdar estes mesmos tokens quando forem criadas.
