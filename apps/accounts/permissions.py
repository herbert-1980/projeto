from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps


def grupo_colaborador_required(groups):
    def decorator(view_func):
        @wraps(view_func)
        @login_required  # Verifica se o usuário está logado
        def wrapper(request, *args, **kwargs):
            # Se o usuário for superusuário, ele terá acesso total
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Verifica se o usuário pertence a um dos grupos permitidos
            if request.user.groups.filter(name__in=groups).exists():
                return view_func(request, *args, **kwargs)
            else:
                # Exibe uma mensagem de erro e redireciona
                messages.error(request, 'Você não tem permissão para acessar esta página.')
                return redirect('home')  # Redireciona para a página inicial

        return wrapper
    return decorator
