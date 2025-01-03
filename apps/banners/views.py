from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from apps.banners import models
from apps.banners.models import Banner
from apps.categorias.models import Categoria
from apps.empresas.models import Empresa
from django.http import JsonResponse


class BannerView(ListView):
    model = models.Banner
    template_name = 'banner_list.html'
    context_object_name = 'banners'
    paginate_by = 9

    def get_queryset(self):
        
        # Filtra apenas os banners do tipo 'Destaque' (destaque=2) e ativos
        return Banner.objects.filter(destaque=2, data_inicio__lte=timezone.now(), data_final__gte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona apenas os banners ativos ao contexto
        context['banner_count'] = self.get_queryset().count()
        context['current_datetime'] = timezone.now()
        context['total_empresas'] = Empresa.objects.count()
        return context


def banners_vip(request):
    # Obtendo os banners VIP ativos
    banners_vip = Banner.objects.filter(destaque=4, data_inicio__lte=timezone.now(), data_final__gte=timezone.now())

    # Adicionado os Banners VIP ao contexto
    context = {
        'banners_vip': banners_vip,
        'vip_count': banners_vip.count(),
        'banner_global': banners_vip.first() if banners_vip.exists() else None,  # Um banner para exibição inicial
    }

    return render(request, 'banners/banners_vip.html', context)


class BannerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Banner
    template_name = 'banners/banner_detail.html'
    context_object_name = 'banner'
    permission_required = 'banners.view_banner'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona categorias associadas ao banner
        context['company_categorias'] = self.object.categorias.all()
        return context

    def get_object(self, queryset=None):
        banner = super().get_object(queryset)
        # Valida se o banner está ativo
        if not banner.is_active():
            raise Http404("Este banner não está ativo.")
        return banner


class BannersPorCategoriaView(ListView):
    model = Banner
    template_name = 'banners_por_categoria.html'
    context_object_name = 'banners'

    def get_queryset(self):
        # Obter a categoria pelo ID fornecido na URL e filtrar banners ativos
        self.categoria = get_object_or_404(Categoria, id=self.kwargs['categoria_id'])
        return Banner.objects.filter(
            categorias=self.categoria,
            destaque__in=[1, 2],
            data_inicio__lte=timezone.now(),
            data_final__gte=timezone.now()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        context['banners_count'] = self.get_queryset().count()
        return context


def get_banner_images(request, banner_id):
    try:
        banner = Banner.objects.get(id=banner_id)
        additional_images = banner.additional_images.all()  # Supondo que há um campo adicional para imagens extras
        images = [img.image.url for img in additional_images]
        response_data = {
            'main_image': banner.banner.url if banner.banner else None,
            'additional_images': images,
        }
        return JsonResponse(response_data)
    except Banner.DoesNotExist:
        return JsonResponse({'error': 'Banner não encontrado'}, status=404)
    