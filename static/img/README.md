# Logo do projeto

Quando a identidade visual for definida com a terapeuta, coloque o arquivo aqui como:

```
static/img/logo.png
```

A home e a navegação (`templates/base.html`, `templates/home.html`) detectam
esse arquivo automaticamente (ver `config/context_processors.py`) e passam a
exibi-lo no lugar do ícone "psychology" usado como placeholder. Não é
necessário alterar nenhum template ou view — basta adicionar o arquivo.
