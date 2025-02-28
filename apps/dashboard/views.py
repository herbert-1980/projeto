from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from apps.accounts.models import MyUser
from apps.news.forms import NewsForm
from apps.news.models import News
from apps.perfil.models import Perfil
from apps.enquetes.models import Enquete
from apps.enquetes.forms import EnquetesForm


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

##################################CRUD DASHBOARD NEWS #############################
class DashboardNewsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/create_news.html'
    form_class = NewsForm

    def get_initial(self):
        return {'author': self.request.user}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.get_initial())
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            if not news.slug_title:
                news.slug_title = slugify(news.title)
            news.save()
            form.save_m2m()

            messages.success(request, 'Notícia adicionada com sucesso!')
            return redirect(reverse('dashboard_news_list'))
        else:
            messages.error(request, 'Erro ao criar notícia. Por favor, verifique os campos.')
            return render(request, self.template_name, {'form': form})

class DashboardNewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'dashboard/listar_noticias.html'
    paginate_by = 10
    context_object_name = 'news_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Notícias"
        context['total_news'] = News.objects.count()
        return context

class DashboardNewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    template_name = 'dashboard/update_news.html'
    form_class = NewsForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(News, pk=pk)

    def get(self, request, *args, **kwargs):
        news = self.get_object() # Pega a notícia que será editada
        form = self.form_class(instance=news)
        return render(request, self.template_name, {'form': form, 'news': news})

    def post(self, request, *args, **kwargs):
        news = self.get_object() # pega a notícia correta
        form = self.form_class(request.POST, request.FILES, instance=news)

        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            if not news.slug_title:
                news.slug_title = slugify(news.title)
            news.save()
            form.save_m2m()

            messages.success(request, 'Notícia atualizada com sucesso!')
            return redirect('dashboard_news_list')
        else:
            messages.error(request, 'Erro ao atualizar notícia. Por favor, verifique os campos.')
            return render(request, self.template_name, {'form': form, 'news': news})
    
class DashboardNewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('dashboard_news_list')    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Excluir Noticia"
        return context

##################################CRUD DASHBOARD ENQUETES #############################
class DashboardEnqueteListView(ListView):
    model = Enquete
    template_name = 'dashboard/listar_enquetes.html'

class DashboardEnqueteCreateView(LoginRequiredMixin, CreateView):
    model = Enquete
    form_class = EnquetesForm
    template_name = 'dashboard/create_enquete.html'
    success_url = reverse_lazy('enquete_list')

    def form_valid(self,form):
        return super().form_valid(form)

class DashboardEnqueteUpdateView(UpdateView):
    model = Enquete
    fields = ('pergunta', 'ativo')
    template_name = 'dashboard/update_enquete.html'
    success_url = 'dashboard/listar_enquetes.html'

class DashboardEnqueteDeleteView(DeleteView):
    model = Enquete
    success_url = reverse_lazy('dashboard_enquete_list') 
