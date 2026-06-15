from .base_serializer import BaseSerializer
from bson.errors import InvalidId
from bson import ObjectId
from src.api.models import Carrinho


class CarrinhoSerializer(BaseSerializer):
    print("Começo das validacoes")
    #Visando que alguem mal intencioado tente enviar uma requisição via URL
    def validate_produto_id(self, value):
       if not value:
           raise ValueError("O campo 'produto_id' é obrigatório e não pode ser nulo.")
       try:
           return str(ObjectId(value))
       except InvalidId:
           raise ValueError("O ID do produto deve conter 24 caracteres")
    def validate_quantidade(self, value):
        try:
            qtd = int(value)
        except (ValueError, TypeError):
            raise ValueError("A quantidade deve ser um número inteiro válido.")
        if qtd <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return qtd
    
    
    def validate_forma_pagamento(self, value):
        
        if not value:
            raise ValueError("O campo 'forma_pagamento' é obrigatório.")
        
        #Tipos de pagamento aceitos(Ficticio):
        formas_aceitas = ["Pix", "Cartao_Credito", "Cartao_Debito", "Boleto"]
        if value not in formas_aceitas:
            raise ValueError(f"Forma de pagamento inválida. Aceitos: {', '.join(formas_aceitas)}")
            
        return value
    
class FinalizarPedidoSerializer(BaseSerializer):  
    # Valida o estado do carrinho no banco
    def validate(self, data):
        print(f"DEBUG: Estamos dentro do validate geral")
        cliente_id = self.context.get('cliente_id')
        
        carrinho = Carrinho.objects(Cliente_id=ObjectId(str(cliente_id))).first()
        print(f"Carrinho do cliente: {carrinho}")
        
        print(f"id do cliente no serializer:{cliente_id}")
        if not carrinho or not carrinho.Itens:
            raise ValueError("Não foi possível finalizar o pedido: Seu carrinho está vazio ou não existe.")
        
        # Salva o carrinho no contexto para a View usar
        self.context['carrinho_validado'] = carrinho
        return data
    
    
    