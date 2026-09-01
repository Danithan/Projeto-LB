from django.contrib.staticfiles import finders


def branding(request):
    """Disponibiliza o caminho da logo pra templates, quando definida (issue #34).

    Enquanto `static/img/logo.png` não existir, os templates continuam usando
    o ícone placeholder atual — basta soltar o arquivo depois, sem mexer em código.
    """
    logo_path = 'img/logo.png'
    return {
        'logo_static_path': logo_path if finders.find(logo_path) else None,
    }
