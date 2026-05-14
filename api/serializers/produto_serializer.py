#ProdutoSerializer é onde será implementado as normas especificas para Produtos
#Exemplo: É necessario que o produto esteja vinculado ao um grupo para ser registrado.

from core.models import Produtos
from .base_serializer import BaseSerializer
from decimal import Decimal, ROUND_HALF_UP

def format_money(value):
    if value is None: return "0.00"
    return str(
        Decimal(value).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
    )

class ProdutoSerializer(BaseSerializer):

    def to_representation(self):
        return {
            "id": str(self.obj.id),
            "Nome": getattr(self.obj, 'Nome', ''),
            "Estoque": getattr(self.obj, 'Estoque', 0),
            "Valor_venda": format_money(getattr(self.obj, 'Valor_venda', 0)),
            "Grupo": getattr(self.obj, 'Grupo', ''),
            "Preco_100g": format_money(getattr(self.obj, 'Preco_100g', 0)),
        }

    def is_valid(self):
        if not self.data_input.get("Nome"):
            raise Exception("O Nome do produto é obrigatório")
        
        if not self.data_input.get("Grupo"):
            raise Exception("O Produto deve estar registrado em um Grupo")
            
        return True

    def save(self):
        return super().save(Produtos)