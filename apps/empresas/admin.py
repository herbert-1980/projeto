from django.contrib import admin
from apps.empresas.models import Empresa, HorarioFuncionamento

# Personalização do título e cabeçalho do admin
admin.site.site_title = 'Administração CoophaNews'
admin.site.site_header = 'Administração CoophaNews'
admin.site.index_title = 'CoophaNews'


# Inline para Horários de Funcionamento
class HorarioFuncionamentoInline(admin.TabularInline):  # TabularInline para exibição compacta
    model = HorarioFuncionamento
    extra = 1  # Número de linhas extras para adicionar horários no admin
    fields = ('dia_da_semana', 'abertura', 'fechamento', 'fechado')  # Campos exibidos
    ordering = ('dia_da_semana',)  # Ordenação padrão
    verbose_name = 'Horário de Funcionamento'
    verbose_name_plural = 'Horários de Funcionamento'


# Configuração personalizada do modelo Company no admin
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razao', 'get_categorias', 'fantasia', 'cnpj', 'telefone', 'bairro', 'cep', 'logo')  # Campos exibidos na listagem
    search_fields = ('razao', 'fantasia', 'cnpj', 'bairro')  # Campos para busca
    list_filter = ('bairro', 'cep')  # Filtros laterais
    filter_horizontal = ('categorias',)  # Interface para selecionar categorias (campo ManyToMany)
    list_per_page = 10  # Paginação

    # Configuração dos campos no formulário de edição
    fieldsets = (
        (None, {
            'fields': (
                'razao', 'fantasia', 'cnpj', 'logo',
                'telefone', 'rua', 'num', 'bairro', 'cep', 'cidade', 'estado',
                'categorias', 'latitude', 'longitude', 'mapa_url'
            )
        }),
    )

    inlines = [HorarioFuncionamentoInline]  # Adiciona os horários como um inline na edição da empresa

    def get_categorias(self, obj):
        """Exibe as categorias da empresa na listagem."""
        return ", ".join([categoria.nome_categoria for categoria in obj.categorias.all()])
    get_categorias.short_description = 'Categorias'


# Registra o modelo Empresa com a configuração personalizada
admin.site.register(Empresa, EmpresaAdmin)
