from django.db import models

# Create your models here.

class Produto(models.Model):
    """
    Modelo para representar produtos com informações sobre THC, CBD e status ANVISA.
    """
    
    # Choices para tipo_espectro
    TIPO_ESPECTRO_CHOICES = [
        ('sativa', 'Sativa'),
        ('indica', 'Indica'),
        ('hibrida', 'Híbrida'),
    ]
    
    # Choices para status_anvisa
    STATUS_ANVISA_CHOICES = [
        ('aprovado', 'Aprovado'),
        ('pendente', 'Pendente'),
        ('reprovado', 'Reprovado'),
    ]
    
    # Choices para categoria_terapeutica
    CATEGORIA_TERAPEUTICA_CHOICES = [
        ('neurologia', 'Neurologia'),
        ('pediatria', 'Pediatria'),
        ('oncologia', 'Oncologia'),
        ('dermatologia', 'Dermatologia'),
        ('outros', 'Outros'),
    ]
    
    # Campos do modelo
    nome = models.CharField(max_length=200, verbose_name="Nome do Produto")
    tipo_espectro = models.CharField(
        max_length=10, 
        choices=TIPO_ESPECTRO_CHOICES,
        verbose_name="Tipo de Espectro"
    )
    thc_percentual = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        verbose_name="Percentual de THC (%)"
    )
    cbd_percentual = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        verbose_name="Percentual de CBD (%)"
    )
    categoria_terapeutica = models.CharField(
        max_length=20,
        choices=CATEGORIA_TERAPEUTICA_CHOICES,
        verbose_name="Categoria Terapêutica"
    )
    status_anvisa = models.CharField(
        max_length=10,
        choices=STATUS_ANVISA_CHOICES,
        default='pendente',
        verbose_name="Status ANVISA"
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.nome} - {self.get_tipo_espectro_display()}"
    
    @property
    def tem_risco(self):
        """
        Verifica se o produto tem risco baseado no THC > 0.3% e categoria específica.
        """
        return (
            self.thc_percentual > 0.3 and 
            self.categoria_terapeutica in ['neurologia', 'pediatria']
        )
    
    @property
    def explicacao_risco(self):
        """
        Retorna explicação do risco se aplicável.
        """
        if self.tem_risco:
            return f"Produto com THC {self.thc_percentual}% para {self.get_categoria_terapeutica_display()} - requer atenção especial"
        return None
