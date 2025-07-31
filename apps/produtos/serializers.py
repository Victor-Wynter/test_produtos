from rest_framework import serializers
from .models import Produto

class ProdutoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Produto com validação customizada.
    """
    tem_risco = serializers.ReadOnlyField()
    explicacao_risco = serializers.ReadOnlyField()
    
    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'tipo_espectro', 'thc_percentual', 'cbd_percentual',
            'categoria_terapeutica', 'status_anvisa', 'data_criacao',
            'data_atualizacao', 'tem_risco', 'explicacao_risco'
        ]
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao', 'tem_risco', 'explicacao_risco']
    
    def validate(self, data):
        """
        Validação customizada: se THC > 0.3%, status ANVISA não pode ser 'aprovado'.
        """
        thc_percentual = data.get('thc_percentual')
        status_anvisa = data.get('status_anvisa')
        
        if thc_percentual and status_anvisa:
            if thc_percentual > 0.3 and status_anvisa == 'aprovado':
                raise serializers.ValidationError(
                    "Produtos com THC superior a 0.3% não podem ter status 'aprovado' na ANVISA."
                )
        
        return data
    
    def to_representation(self, instance):
        """
        Customiza a representação para incluir labels dos choices.
        """
        data = super().to_representation(instance)
        data['tipo_espectro_label'] = instance.get_tipo_espectro_display()
        data['status_anvisa_label'] = instance.get_status_anvisa_display()
        data['categoria_terapeutica_label'] = instance.get_categoria_terapeutica_display()
        return data 