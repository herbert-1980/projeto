from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from apps.comments.forms import CommentForm
from django.utils.timezone import now
from django.utils.text import slugify
from unidecode import unidecode
from django.db.models import Q, Count, Case, When
from datetime import timedelta
from django.contrib import messages
from apps.comments.models import Comment
from django.views.generic import DetailView
from apps.news.forms import NewsForm
from apps.news.models import News, Categoria
from apps.enquetes.models import Enquete, Escolha
from apps.enquetes.forms import EnquetesForm
from apps.banners.models import Banner
from django.views import View
from django.utils import timezone
from django.shortcuts import render, redirect


class NewsIndex(ListView):
    model = News
    template_name = 'news/index.html'
    paginate_by = 6
    context_object_name = 'news_list'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pegar os Banners com destaque 2
        context['banners'] = Banner.objects.filter(destaque__in=[2])
        
        # Insere na News as enquetes Obter a enquete ativa
        enquete = Enquete.objects.filter(ativo=True).first()  # Pega a primeira enquete ativa

        # Criar o formulário com a enquete
        form = EnquetesForm(enquete=enquete) if enquete else None
        # Calcula a data de uma semana atrás
        context['enquete'] = enquete
        context['form'] = form
        
        last_week = now() - timedelta(days=7)

        # Filtra as notícias mais vistas na última semana
        context['breaking_news'] = News.objects.filter(
            status='published',
            is_published=True,
            published_at__gte=last_week
        ).order_by('-views')[:10]  # Limita às 10 notícias mais vistas

        # Notícias prioritárias
        context['priority_news'] = News.objects.filter(
            status='priority',
            is_published=True,
        ).order_by('-published_at')[:6]  # Limita às 6 notícias prioritárias

        # Últimas notícias da categoria economia
        context['economia'] = News.objects.filter(
            status='published',
            categorias__nome_categoria='Economia',
            is_published=True,
        ).order_by('-published_at').first()

        # Últimas notícias da categoria Viagens
        context['viagens'] = News.objects.filter(
            status='published',
            categorias__nome_categoria='Viagens',
            is_published=True,
        ).order_by('-published_at').first()

        # Últimas notícias da categoria Culinária
        normalized_category_name = unidecode('Culinária').lower()
        context['culinaria'] = News.objects.filter(
            status='published',
            categorias__nome_categoria__iexact='Culinária',
            is_published=True,
        ).order_by('-published_at').first()

        # Últimas notícias da categoria Tecnologia
        context['bairros'] = News.objects.filter(
            status='published',
            categorias__nome_categoria='Bairros',
            is_published=True,
        ).order_by('-published_at').first()

        # Adiciona as notícias mais populares
        context['popular_news'] = News.objects.filter(
            status='published',
            is_published=True
        ).order_by('-views')[:5]

        # Últimas notícias da categoria Tecnologia
        context['tecnologia'] = News.objects.filter(
            status='published',
            categorias__nome_categoria='Tecnologia',
            is_published=True,
        ).order_by('-published_at')[:2]
        
        return context

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug_title': self.slug_title})

    def featured_news_view(request):
        featured_news = News.objects.filter(is_featured=True).order_by('-published_at')[:5]  # Limitar a news
        return render(request, 'news/news_featured.html', {'featured_news': featured_news})

    def termos_de_uso(request):
        return render(request, 'news/termos_de_uso.html')


class NewsSearch(NewsIndex):
    template_name = 'news/news_search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        termo = self.request.GET.get('termo')
        data = self.request.GET.get('data')

        # Contar o número de comentários
        queryset = queryset.annotate(comment_count=Count('comments'))
        queryset = queryset.order_by('-published_at')  # Ordena pela data de publicação em ordem decrescente


        if not termo and not data:
            return queryset

        if termo:
            queryset = queryset.filter(
                Q(title__icontains=termo) |
                Q(subtitle__icontains=termo) |
                Q(slug_title__icontains=termo) |
                Q(author__first_name__icontains=termo) |
                Q(content__icontains=termo) |
                Q(resume__icontains=termo) |
                Q(categorias__nome_categoria__icontains=termo)
            )


        if data:
            try:
                # Converte a string da data para um objeto de data
                search_date = timezone.datetime.strptime(data, '%Y-%m-%d').date()
                search_date = timezone.make_aware(search_date)
                queryset = queryset.filter(published_at__date=search_date)
            except ValueError:
                pass # Lidar com erros caso a data não seja válida
            
        return queryset


class NewsCategorias(NewsIndex):
    template_name = 'news/news_by_category.html'

    def get_queryset(self):
        qs = super().get_queryset()

        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs

        qs = qs.filter(categorias__nome_categoria__iexact=categoria)

        return qs


class NewsDetail(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    # O campo no modelo que corresponde ao slug
    slug_field = 'slug_title'
    
    # O nome do parâmetro slug da url
    slug_url_kwarg = 'slug_title'

    def get(self, request, form=None, *args, **kwargs):
        """if not form:
            form = CommentForm
        return render(request, self.template_name, {'form': form, 'object': self.get_object()})"""
        # Obtém o objeto de notícia
        self.object = self.get_object()

        # Incrementa a contagem de visualizações
        self.object.views += 1
        self.object.save(update_fields=['views'])  # Atualiza apenas o campo de visualizações

        # Chama o método da superclasse para obter o contexto
        context = self.get_context_data(object=self.object, **kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_priority_news'] = True  # Adiciona o contexto para esconder o componente
        context['hide_featured_news'] = True
        context['is_news_detail'] = True
        context['search_news'] = True
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(comment_news=self.object, comment_published=True, parent__isnull=True).order_by('created_at')
        context['comment_count'] = context['comments'].count()  # Adiciona a contagem de comentários

        # Pegar os Banners com destaque 2
        context['banners'] = Banner.objects.filter(destaque__in=[2])
        
        # Insere na News as enquetes Obter a enquete ativa
        context['enquetes'] = Enquete.objects.filter(ativo=True).first()  # Pega a primeira enquete ativa
        
        """# Média de avaliações (estrelas)
        ratings = context['comments'].filter(rating__isnull=False).values_list('rating', flat=True)
        if ratings:
            context['average_rating'] = float(sum(ratings) / len(ratings))  # Garante que é um float
        else:
            context['average_rating'] = 0.0  # Se não houver avaliações ainda
"""
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        parent_id = request.POST.get('parent_id')
        if form.is_valid():
            comment = form.save(commit=False)
            # Associa o comentário à notícia correta
            comment.comment_news = self.get_object()
            
            # Verifica se é uma resposta a outro comentário
            # parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    messages.error(request, "Comentário da Notícia não Existe!")
                    return self.get(request, form=form, *args, **kwargs)
                    
            if request.user.is_authenticated:
                comment.comment_user = request.user  # ou outro campo de usuário, se houver
                comment.save()
                messages.success(request, 'Comentário e avaliação enviado com sucesso!')
                return redirect('news_detail', slug_title=self.get_object().slug_title)
            else:
                # Se o usuário não estiver autenticado, adiciona um erro no formulário
                form.add_error(None, 'Você precisa estar logado para enviar um comentário.')
                # Renderiza novamente a página com o formulário e mensagens de erro

        return self.get(request, form=form, *args, **kwargs)

class PopularNewsView(ListView):
    template_name = 'news/popular_news.html'
    context_object_name = 'news_list'

    # paginate_by = 5  # Se você quiser paginação, ajuste conforme necessário

    def get_queryset(self):
        # Ordena as notícias por visualizações e limita a 5
        return News.objects.filter(
            status='published',
            is_published=True,
            principal_image__isnull=False  # Garante que haja uma imagem principal
        ).order_by('-views')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.objects.filter(status='published', is_published=True).order_by('-views')[:5]
        return context


class NewsByCategoryView(ListView):
    model = News
    template_name = 'news/news_by_category.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        slug_categoria = self.kwargs.get('slug_categoria')
        return News.objects.filter(categorias__slug_categoria=slug_categoria)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug_categoria = self.kwargs.get('slug_categoria')
        context['categoria'] = Categoria.objects.get(slug_categoria=slug_categoria)
        return context


def newsShare(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.share += 1  # Usa 'share', que é o nome do campo no modelo
    news.save(update_fields=['share'])  # Atualiza apenas o campo 'share'
    return redirect('news_detail', slug_title=news.slug_title)


def news_list_view(request):
    # Obtenha as notícias publicadas
    news = News.objects.filter(is_published=True)

    # Obtenha enquetes ativas
    enquete = Enquete.objects.filter(ativo=True).first()
    form = None
    
    if enquete:
        form = EnquetesForm(enquete=enquete)

    context = {
        'news': news,
        'enquete': enquete,  # Adiciona as enquetes ao contexto
        'form': form,
    }
    
    return render(request, 'news/enquetes_list.html', context)


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

############################## CRUD ##################################
class DashboardNewsView(View):
    template_name = 'news/criar_noticia.html'
    form_class = NewsForm

    def get_context(self, form=None):
        """Método auxiliar para criar o contexto"""
        news_list = News.objects.filter(is_published=True)
        if form is None:
            form = self.form_class()
        return {
            'news_list': news_list,
            'form': form,
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            # Atribui o autor e cria o slug se necessário
            news.author = request.user
            if not news.slug_title:
                news.slug_title = slugify(news.title)
            news.save()
            messages.success(request, 'Notícia adicionada com sucesso!')
            return redirect(reverse('news_dashboard'))
        else:
            print("Erros do Formulário:", form.errors)
            context = self.get_context(form)
            return render(request, self.template_name, context)
