#ProdutoSerializer é onde será implementado as normas especificas para Produtos
#Exemplo: É necessario que o produto esteja vinculado ao um grupo para ser registrado.

from src.api.models import Produtos
from .base_serializer import BaseSerializer
from decimal import Decimal, ROUND_HALF_UP
from decimal import Decimal, InvalidOperation
from bson import ObjectId

def format_money(value):
    if value is None: return "0.00"
    return str(
        Decimal(value).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
    )
    
required_fields = ['Estoque', 'Nome', 'Unidade', 'Valor_venda', 'Grupo', 'Preco_100g']

class ProdutoSerializer(BaseSerializer):

    def to_representation(self):
        return {
            "id": str(self.obj.id),
            "Estoque": getattr(self.obj, 'Estoque', 0),
            "Nome": getattr(self.obj, 'Nome', ''),
            "Valor_venda": format_money(getattr(self.obj, 'Valor_venda', 0)),
            "Grupo": getattr(self.obj, 'Grupo', ''),
            "Preco_100g": format_money(getattr(self.obj, 'Preco_100g', 0)),
        }

    def validate_Nome(self, value):
        nome = value.strip()
        query = Produtos.objects(Nome__iexact=nome)
        
        if hasattr(self, 'obj') and self.obj and self.obj.id:
            # Garantimos que estamos comparando Objetos do tipo ObjectId, não strings
          
            current_id = ObjectId(str(self.obj.id)) 
            query = query.filter(id__ne=current_id)
            
        if query.count() > 0:
            raise ValueError(f"Já existe um produto com esse nome !'{nome}'!")
            
        # Validações de tamanho
        if not nome or not nome.strip():
            raise ValueError("O nome é obrigatório.")
        if len(nome) < 3:
            raise ValueError("O nome do produto deve conter ao menos 3 caracteres")
        if len(nome) > 100:
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
            raise ValueError("O estoque deve conter um número decimal válido, exemplo: 50.00")
    
    def validate_Unidade(self, value):
        if not value:
            raise ValueError("O produto deve conter o tipo de Unidade !")
        return value
        
    def validate_Valor_venda(self, value):
        if value == "" :
            raise ValueError("O valor venda é necessario.")
        try:
            valor_venda = Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("O valor de venda deve ser um numero decimal válido")
        if valor_venda < 0:
                raise ValueError("O valor venda não pode ser negativo")
        return valor_venda
      
    
    def validate_Preco_100g(self, value):
        if value == "":
            raise ValueError("O preço de 100g é necessario.")
        
        try:
            preco_100g = Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("O valor deve ser um numero decimal válido")
            
        if preco_100g < 0:
            # Esta mensagem só aparece se for um número, mas negativo
            raise ValueError("O preço de 100g não pode ser negativo !")
            
        return preco_100g
                
            
    
    
    
    
    def save(self):
        # Garante que o objeto self.obj exista antes de salvar
        if not hasattr(self, 'obj') or self.obj is None:
            raise ValueError("Nenhum objeto para salvar.")
        
        return self.obj.save()