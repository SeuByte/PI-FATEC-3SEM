from core.models import Produtos
from decimal import Decimal, ROUND_HALF_UP

def format_money(value):
    return str(
        Decimal(value).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
    )

class ProdutoSerializer:

    def __init__(self, obj=None, data=None):
        self.obj = obj
        self.data_input = data

    def to_representation(self):
        return {
            "id": str(self.obj.id),
            "Nome": self.obj.Nome,
            "Estoque": self.obj.Estoque,
            "Valor_venda": format_money(self.obj.Valor_venda),
            "Grupo": self.obj.Grupo,
            "Preco_100g": format_money(self.obj.Preco_100g),
        }

    def is_valid(self):
        if not self.data_input.get("Nome"):
            raise Exception("Nome é obrigatório")
        return True

    def save(self):
        produto = Produtos(**self.data_input)
        produto.save()
        return produto