from django.db.models import Count
from apps.empresas.models import Empresa


class EmpresaCountMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa_count'] = Empresa.objects.count()  # Contagem de empresas
        return context
