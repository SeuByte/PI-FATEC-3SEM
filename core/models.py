import mongoengine as me

class Clientes(me.Document):
    Nome = me.StringField(required=True)
    Email = me.StringField(required=True)
    Senha = me.StringField(required=True)
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
    Estoque = me.IntField(required=True)
    Nome = me.StringField(required=True)
    Unidade = me.StringField(required=True)
    Valor_venda = me.FloatField(required=True)
    Grupo = me.StringField(required=True)
    Preco_100g = me.FloatField(required=True)