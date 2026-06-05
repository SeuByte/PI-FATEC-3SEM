
import mongoengine as me
from datetime import datetime, timezone

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


class Funcionario(me.Document):
    Nome_completo = me.StringField(required=True)
    Cpf = me.StringField(required=True, unique=True)
    Data_nascimento = me.DateTimeField()
    Email_corporativo = me.EmailField()
    Cargo = me.StringField()
    Departamento = me.StringField()
    Salario = me.DecimalField(precision=2)
    Data_admissao = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    Ativo = me.BooleanField(default=True)
    Is_admin = me.BooleanField(default=False)
    
    
