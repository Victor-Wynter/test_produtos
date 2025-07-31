from django.contrib import admin
from .models import Produto

# Register your models here.

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Produto.
    """
    list_display = [
        'nome', 'tipo_espectro', 'thc_percentual', 'cbd_percentual',
        'categoria_terapeutica', 'status_anvisa', 'tem_risco', 'data_criacao'
    ]
    list_filter = [
        'tipo_espectro', 'categoria_terapeutica', 'status_anvisa', 'data_criacao'
    ]
    search_fields = ['nome', 'categoria_terapeutica']
    readonly_fields = ['data_criacao', 'data_atualizacao', 'tem_risco', 'explicacao_risco']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo_espectro')
        }),
        ('Composição', {
            'fields': ('thc_percentual', 'cbd_percentual')
        }),
        ('Classificação', {
            'fields': ('categoria_terapeutica', 'status_anvisa')
        }),
        ('Informações do Sistema', {
            'fields': ('data_criacao', 'data_atualizacao', 'tem_risco', 'explicacao_risco'),
            'classes': ('collapse',)
        }),
    )
    
    def tem_risco(self, obj):
        """
        Exibe se o produto tem risco no admin.
        """
        return obj.tem_risco
    tem_risco.boolean = True
    tem_risco.short_description = 'Tem Risco'
