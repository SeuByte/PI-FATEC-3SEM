#ProdutoSerializer é onde será implementado as normas especificas para Produtos
#Exemplo: É necessario que o produto esteja vinculado ao um grupo para ser registrado.

from src.core.models import Produtos
from .base_serializer import BaseSerializer
from decimal import Decimal, ROUND_HALF_UP
from decimal import Decimal, InvalidOperation

def format_money(value):
    if value is None: return "0.00"
    return str(
        Decimal(value).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
    )
    
required_fields = ['Nome', 'Estoque', 'Unidade', 'Valor_venda', 'Grupo', 'Preco_100g']

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

    def validate_Nome(self, value):
        nome = value.strip()
        produto_existente = Produtos.objects.filter(
            Nome__iexact = nome
        ).first()
        if produto_existente:
            raise ValueError("Já existe um produto com esse nome !")
        if not nome:
            raise ValueError("O Nome do produto é obrigatório")
        if len(nome.strip()) < 3:
            raise ValueError("O nome do produto deve conter ao menos 3 caracteres")
        if len(nome.strip()) > 50:
            raise ValueError("O nome do produto é muito grande")
        return nome
    
    def validate_Grupo(self, value):
        if not value:
            raise ValueError("O produto deve pertencer a um grupo!")
        return value
    
    def validate_Estoque(self, value):
        if value == "":
            raise ValueError("O produto deve conter estoque a cima de zero !")
        try:
            estoque = Decimal(str(value))
            
            if estoque < 0:
                raise ValueError("O produto não pode ter estoque negativo !")
            return estoque
        except (InvalidOperation, ValueError, TypeError) as e:
            print(f"DEBUG: Erro na conversão Decimal: {e}")
            raise ValueError("O estoque deve conter um numero decimal válido, exemplo: 50.00")
    
    def validate_Unidade(self, value):
        if not value:
            raise ValueError("O produto deve conter o tipo de Unidade !")
        return value
        
    def validate_Valor_venda(self, value):
        if value == "" :
            raise ValueError("O valor venda é necessario.")
        return value
    
    def validate_Preco_100g(self, value):
        if value == "":
            raise ValueError("O preço de 100g é necessario.")
        try:
            preco_100g = Decimal(str(value))
            if preco_100g < 0:
                raise ValueError("O preço de 100g não pode ser negativo !")
            return preco_100g
        except(InvalidOperation, ValueError, TypeError):
            raise ValueError("O preço de 100g deve conter um numero decimal válido, exemplo: 7.00")
                
            
    
    
    
    
    def save(self):
        return super().save(Produtos)