from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from apps.empresas import models, forms
from apps.empresas.models import Empresa
from django.utils import timezone


class EmpresaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Empresa
    template_name = 'company_list.html'
    context_object_name = 'empresas'
    paginate_by = 10
    permission_required = 'empresas.view_empresa'

    def get_queryset(self):
        queryset = super().get_queryset()
        fantasia = self.request.GET.get('fantasia')

        if fantasia:
            queryset = queryset.filter(fantasia__icontains=fantasia)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa_count'] = Empresa.objects.count()
        
        # Filtrar empresas que estão abertas no momento
        now = timezone.localtime() # Horário Local Atual
        empresas = context['empresas']
        for empresa in empresas:
            empresa.is_open_now = empresa.is_open(now)
        
        return context

# Create
class EmpresaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Empresa
    form_class = forms.EmpresaForm
    template_name = 'company_create.html'
    success_url = reverse_lazy('company_list')
    permission_required = 'empresas.add_empresa'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa_count'] = Empresa.objects.count()
        return context

# Details
class EmpresaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Empresa
    template_name = 'company_detail.html'
    permission_required = 'empresas.view_empresa'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = self.object.categorias.all()
        context['empresa_count'] = Empresa.objects.count()
        return context


# Update
class EmpresaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Empresa
    form_class = forms.EmpresaForm
    template_name = 'company_update.html'
    success_url = reverse_lazy('company_list')
    permission_required = 'empresas.change_empresa'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa_count'] = Empresa.objects.count()  # Adicionando a contagem aqui
        return context

# Delete
class EmpresaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Empresa
    template_name = 'company_delete.html'
    success_url = reverse_lazy('empresa_list')
    permission_required = 'empresas.delete_empresa'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa_count'] = Empresa.objects.count()  # Adicionando a contagem aqui
        return context
