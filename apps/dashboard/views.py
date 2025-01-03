from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from apps.accounts.models import MyUser
from apps.perfil.models import Perfil


@login_required
def index(request):
    is_admin = request.user.groups.filter(name='administrador').exists()
    users = MyUser.objects.all()
    return render(request, 'dashboard/index.html', {'is_admin': is_admin})


@login_required
def perfil_view(request, username):
    user_profile = get_object_or_404(MyUser, username=username)
    return render(request, 'perfil/index.html', {'user': user_profile})


@login_required
def personalize_dashboard(request):
    return render(request, 'dashboard/personalize.html')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

@login_required
def list_users_dashboard(request):
    users = Perfil.objects.select_related('perfil').all()  # Busca todos os perfis com o usuário associado
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    is_paginated = paginator.num_pages > 1
    
    return render(request, 'dashboard/users.html', {
        'page_obj': page_obj,
        'is_paginated': is_paginated,  # Flag para o template
    })

@login_required
def excluir_usuario(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)  # Substitua MyUser pelo modelo correto se necessário
    user.delete()  # Exclui o usuário
    messages.success(request, 'Usuário excluído com sucesso!')
    return redirect('list_users_dashboard')  # Redireciona para a lista de usuários

