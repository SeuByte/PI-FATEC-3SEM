
import mongoengine as me
from mongoengine import EnumField
from enum import Enum

class StatusPedido(Enum):
    PENDENTE = "Pendente"
    APROVADO = "Aprovado"
    Cancelado = "Cancelado"





class Clientes(me.Document):
    Nome = me.StringField(required=True)
    Email = me.EmailField(required=True, unique=True)
    Senha = me.StringField(required=True)
    Celular = me.StringField()
    Telefone = me.StringField(required=True)
    Data_nasc = me.DateField(required=True)
    CPF = me.StringField(required=True, unique=True)
    CEP = me.StringField(required=True)
    Endereco = me.StringField(required=True)
    Bairro = me.StringField(required=True)
    Numero = me.IntField(required=True)
    Complemento = me.StringField()
    Cidade = me.StringField(required=True)
    Estado = me.StringField(required=True)
    
    
class Produtos(me.Document):
    Estoque = me.Decimal128Field(required=True)
    Nome = me.StringField(required=True)
    Unidade = me.StringField(required=True)
    Valor_venda = me.Decimal128Field(required=True)
    Grupo = me.StringField(required=True)
    Preco_100g = me.Decimal128Field(required=True)



class ItemCarrinho(me.EmbeddedDocument):
    Produto_id = me.ObjectIdField(required=True)
    Produto = me.StringField(required=True)
    Quantidade = me.IntField(required=True)
    Preco_unitario = me.Decimal128Field(required=True)
    Subtotal = me.Decimal128Field(required=True)
    
    
class Pedidos(me.Document):
    Carrinho_id = me.ObjectIdField(required=True)
    Cliente_id = me.ObjectIdField(required=True)
    Itens = me.ListField(me.EmbeddedDocumentField(ItemCarrinho))
    Status = EnumField(StatusPedido, default=StatusPedido.PENDENTE, required=True)
    Forma_pagamento = me.StringField(required=True)
    Valor_total = me.DecimalField(precision=2, force_string=True, required=True)

class Carrinho(me.Document):
    Cliente_id = me.ObjectIdField(required=True)
    Itens = me.ListField(me.EmbeddedDocumentField(ItemCarrinho))
    Valor_frete = me.Decimal128Field(null=True, default=0.0)
    Tipo_frete = me.StringField()
    
    
    
    
