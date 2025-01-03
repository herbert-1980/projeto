from venv import logger
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from apps.accounts.permissions import grupo_colaborador_required
from apps.accounts.forms import CustomUserCreationForm, UserChangeForm, CustomPasswordResetForm
from apps.empresas.forms import EmpresaForm
from apps.perfil.forms import PerfilForm
from apps.perfil.models import Perfil
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from apps.accounts.models import MyUser
from django.urls import reverse
import logging 


logger = logging.getLogger(__name__)


# Create your views here.
def timeout_view(request):
    return render(request, 'timeout.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='administrador').exists():
                return redirect(reverse('admin:index'))
            elif user.groups.filter(name='colaborador').exists():
                return redirect(reverse('dashboard'))
            else:
                return redirect(reverse('success'))
        else:
            messages.error(request, 'Email ou senha inválidos')

    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'registration/login.html')


# Registrar Usuario
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.save()
            
            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)
            
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('success')
        else:
            # Tratar quando usuario já existe, senhas... etc...
            messages.error(request, 'A senha deve ter pelo menos 1 caractere maiúsculo, \
                1 caractere especial e no minimo 8 caracteres.')
    form = CustomUserCreationForm()
    return render(request, "registration/register.html",{"form": form})
    

# View para completar o perfil do usuário
def complete_user_profile_view(request):
    return render(request, "complete_user_profile")

def success(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    return render(request, 'registration/success.html')

@login_required()
def update_my_user(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=request.user, user=request.user)
    return render(request, 'user_update.html', {'form': form})


@login_required()
@grupo_colaborador_required(['administrador', 'colaborador'])
def update_user(request, user_id):
    user = get_object_or_404(MyUser, pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'O perfil de usuário foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=user, user=request.user)
    return render(request, 'user_update.html', {'form': form})


def password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
            )
            messages.success(request, 'Um email para redefinição de senha foi enviado.')
            return redirect(reverse('password_reset_done'))
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset_form.html', {'form': form})


@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def list_users(request): # Lista Cliente 
    list_users = MyUser.objects.select_related('perfil').filter(is_superuser=False) 
    return render(request, 'user_list.html', {'list_users': list_users})


@login_required
@grupo_colaborador_required(['administrador', 'colaborador'])
def user_add(request):
    user_form = CustomUserCreationForm()
    perfil_form = PerfilForm()
    user_groups = Group.objects.all()  # Todos os grupos disponíveis

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)

        if user_form.is_valid():
            try:
                # Salva o novo usuário
                usuario = user_form.save()

                # Adiciona o usuário ao grupo padrão ou ao grupo selecionado
                group_id = request.POST.get('group')  # Pega o ID do grupo selecionado

                if group_id and Group.objects.filter(id=group_id).exists():
                    group = Group.objects.get(id=group_id)
                    usuario.groups.add(group)
                else:
                    group, created = Group.objects.get_or_create(name='usuario')
                    usuario.groups.add(group)

                # Verifica se o perfil já existe
                perfil, created = Perfil.objects.get_or_create(usuario=usuario, defaults={'nome': usuario.get_full_name()})
                # Cria o perfil para o usuário
                perfil = perfil_form.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

                if created:
                    print(f"Perfil criado com usuário: {perfil.usuario.username} e nome: {perfil.nome}")
                else:
                    print(f"O perfil já existe para o usuário {usuario.username}")

                messages.success(request, 'Usuário adicionado com sucesso.')
                return redirect('complete_user_profile', user_id=usuario.id)

            except IntegrityError as e:
                logger.error(f"Erro ao criar o grupo ou perfil: {e}")
                messages.error(request, 'Erro ao adicionar o usuário ou criar o perfil.')
                return redirect('user_add')
            except Exception as e:
                logger.error(f"Erro inesperado: {e}")
                messages.error(request, 'Ocorreu um erro inesperado.')
                return redirect('user_add')

        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')

    context = {
        'user_form': user_form,
        'user_groups': user_groups,
    }

    return render(request, "user_add.html", context) 


@login_required
@grupo_colaborador_required(['administrador', 'colaborador'])
def list_users_dashboard(request):
    group_filter = request.GET.get('group', None)
    status_filter = request.GET.get('status', None)

    list_users_dashboard = MyUser.objects.filter(is_superuser=False)  # Filtra apenas usuários normais, não superusuários
    if group_filter:
        list_users_dashboard = list_users_dashboard.filter(groups__name=group_filter)

    if status_filter:
        list_users_dashboard = list_users_dashboard.filter(is_active=(status_filter== 'Ativo'))

    user_groups = Group.objects.values_list('name', flat=True)
    statuses = ['Ativo', 'Desativado']
    return render(request, 'dashboard/users.html', {
        'list_users_dashboard': list_users_dashboard,
        'user_groups': user_groups,
        'statuses': statuses,
    })  # Renderiza no template do app dashboard


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Atualiza a sessão para não desconectar o usuário
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('success')  # Redirecione para onde desejar
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})

@login_required
@grupo_colaborador_required(['administrador', 'colaborador'])
def complete_user_profile(request, user_id):
    usuario = get_object_or_404(MyUser, id=user_id)
    perfil_form = PerfilForm(instance=usuario.perfil)  # Carregar o perfil existente
    empresa_form = EmpresaForm()

    if request.method == 'POST':
        perfil_form = PerfilForm(request.POST, request.FILES, instance=usuario.perfil)
        empresa_form = EmpresaForm(request.POST, request.FILES)

        if perfil_form.is_valid():
            perfil_form.save()  # Atualiza o perfil existente
            messages.success(request, 'Perfil atualizado com sucesso.')
        else:
            messages.error(request, 'Por favor, corrija os erros no Formulário de Perfil.')

        if empresa_form.is_valid():
            empresa = empresa_form.save(commit=False)
            empresa.usuario = usuario
            empresa.save()
            usuario.perfil.empresa = empresa  # Relaciona a empresa com o perfil
            usuario.perfil.save()
            messages.success(request, 'Empresa atualizada com sucesso.')
        else:
            messages.error(request, 'Por favor, corrija os erros no Formulário da Empresa.')

        return redirect('user_list')

    context = {
        'usuario': usuario,
        'perfil_form': perfil_form,
        'empresa_form': empresa_form,
    }

    return render(request, 'complete_user_profile.html', context)

