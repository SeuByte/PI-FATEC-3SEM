#ClienteSerializer implementa as normas especificas para clientes.
#Exemplo: Para CPF é necessario 11 digitos.
from core.models import Clientes
from .base_serializer import BaseSerializer

class ClienteSerializer(BaseSerializer):
   def to_representation(self):
       return {
         "id": str(self.obj.id),
         "Nome": self.obj.Nome,
         "Email": self.obj.Email,
         "Senha": self.obj.Senha,
         "Telefone": self.obj.Telefone,
         "Data_nasc": self.obj.Data_nasc,
         "CPF": self.obj.CPF,
         "CEP": self.obj.CEP,
         "Endereco": self.obj.Endereco,
         "Bairro": self.obj.Bairro,
         "Numero": self.obj.Numero,
         "Complemento": self.obj.Complemento,
         "Cidade": self.obj.Cidade,
         "Estado": self.obj.Estado
      }
    
    
   def save(self):
       return super().save(Clientes)