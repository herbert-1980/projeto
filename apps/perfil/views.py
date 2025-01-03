from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from apps.accounts.models import MyUser
from django.contrib import messages
from apps.perfil.forms import PerfilForm
from apps.perfil.models import Perfil


def calcular_idade(data_nascimento):
    hoje = datetime.now()
    idade = hoje.year - data_nascimento.year
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    return idade

def perfil_view(request, username=None):
    """perfil = get_object_or_404(MyUser.objects.select_related('perfil'), username=username)"""
     # Seleciona o usuário com o perfil relacionado
    usuario = get_object_or_404(MyUser.objects.select_related('perfil'), username=username)
    
    # Acessa o objeto perfil relacionado ao usuário
    perfil = usuario.perfil
    # Calcula a idade se a data de nascimento estiver disponível
    idade = calcular_idade(perfil.birth_date) if perfil and perfil.birth_date else None
    
    # Passa o usuário, o perfil e a idade para o contexto
    context = {
        'usuario': usuario,
        'perfil': perfil,
        'idade': idade,
    }
    
    return render(request, 'dashboard/perfil.html', context)
    
########## CRUD ###########

def criar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES)  # Inclua request.FILES para o upload de imagens
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user  # Associa o perfil ao usuário logado
            perfil.save()
            messages.success(request, 'Perfil criado com sucesso!')
            return redirect('listar_perfis')
    else:
        form = PerfilForm()
    return render(request, 'dashboard/criar_perfil.html', {'form': form})

def listar_perfis(request):
    perfis = Perfil.objects.all()
    return render(request, 'dashboard/listar_perfis.html', {'perfis': perfis})

def editar_perfil(request, usuario_id):
    perfil = get_object_or_404(Perfil, usuario__id=usuario_id)
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil', username=perfil.usuario.username)
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'dashboard/editar_perfil.html', {'form': form, 'perfil': perfil})

def excluir_perfil(request, usuario_id):
    perfil = get_object_or_404(Perfil, usuario__id=usuario_id)
    if request.method == 'POST':
        perfil.delete()
        messages.success(request, 'Perfil excluído com sucesso!')
        return redirect('listar_perfis')
    return render(request, 'dashboard/excluir_perfil.html', {'perfil': perfil})
