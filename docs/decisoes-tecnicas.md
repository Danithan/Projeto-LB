# Decisões Técnicas

Este documento registra as principais decisões de arquitetura e tecnologia tomadas durante o desenvolvimento do projeto, junto com a justificativa de cada uma.

## Stack escolhida

| Camada | Tecnologia |
|---|---|
| Back-end | Django |
| Front-end (páginas) | Templates do Django + HTML/CSS |
| Interatividade dos jogos | JavaScript (Vanilla JS) |
| Banco de dados (desenvolvimento) | SQLite |
| Banco de dados (produção, futuro) | PostgreSQL |
| Geração de PDF | WeasyPrint |
| Estilização | CSS puro / Bootstrap |

## Justificativas

### Por que Django (back-end)

- A equipe já tem mais familiaridade com Python do que com outras linguagens, o que reduz a curva de aprendizado nessa fase.
- O admin panel automático do Django resolve boa parte do cadastro de crianças (RF01-RF03) e da visualização de histórico (RF08) sem a necessidade de construir uma interface CRUD do zero.
- O ORM integrado facilita a modelagem e manipulação do banco de dados sem necessidade de escrever SQL manualmente.
- Estrutura padronizada (MVT) ajuda a manter o código organizado à medida que o projeto cresce.

### Por que Vanilla JS para os jogos

- Os exercícios interativos (caça-palavras, organizar letras) são simples o suficiente para não justificar a complexidade de um framework front-end (React, Vue).
- Evita introduzir um segundo ecossistema de tecnologia enquanto a equipe ainda está consolidando os fundamentos.

### Por que SQLite (desenvolvimento) e PostgreSQL (produção)

- SQLite já vem configurado por padrão no Django, sem necessidade de instalação, o que agiliza o início do desenvolvimento e os testes.
- PostgreSQL é indicado para quando o sistema estiver em uso real com a terapeuta, por oferecer mais robustez, suporte a acessos concorrentes e melhor infraestrutura para backups.

### Por que WeasyPrint (geração de PDF)

- Converte HTML/CSS diretamente em PDF, o que se encaixa naturalmente com o Django (que já gera páginas HTML). Os relatórios de sessão e consolidado (RF09, RF10) podem ser construídos como templates HTML e depois exportados, sem necessidade de uma biblioteca de PDF mais complexa ou de baixo nível.

## Pendências relacionadas a essas decisões

- Avaliar, ao longo do desenvolvimento, se Bootstrap será adotado integralmente ou se o time optará por CSS próprio.
- Planejar o momento da migração de SQLite para PostgreSQL, antes do uso em produção pela terapeuta.
