
import mongoengine as me

class Clientes(me.Document):
    Nome = me.StringField(required=True)
    Email = me.EmailField(required=True, unique=True)
    Senha = me.StringField(required=True)
    Celular = me.StringField()
    Telefone = me.StringField(required=True)
    Data_nasc = me.DateField(required=True)
    CPF = me.StringField(required=True)
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
    

class Carrinho(me.Document):
    Cliente_id = me.ObjectIdField(required=True)
    Itens = me.ListField(me.DictField())
    Valor_frete = me.IntField( null =True, default=None)
    Tipo_frete = me.StringField()
    
    
    
    
