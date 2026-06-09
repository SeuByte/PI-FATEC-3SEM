from .base_serializer import BaseSerializer



class CarrinhoSerializer(BaseSerializer):
    
    #Visando que alguem mal intencioado tente enviar uma requisição via URL
    def validate_produto_id(self, value):
        if len(value) != 24:
            raise ValueError("O ID do produto deve ter 24 caracteres")
        return value
    def validate_quantidade(self, value):
        
        qtd = int(value)
        if qtd <=0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return qtd