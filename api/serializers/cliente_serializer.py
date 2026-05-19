#ClienteSerializer implementa as normas especificas para clientes.
#Exemplo: Para CPF é necessario 11 digitos.
from core.models import Clientes
from .base_serializer import BaseSerializer
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.contrib.auth.hashers import make_password
class ClienteSerializer(BaseSerializer):
   def to_representation(self):
       return {
         "id": str(self.obj.id),
         "Nome": self.obj.Nome,
         "Email": self.obj.Email,
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
    
   def validate_Senha(self, value):
      if len(value) < 8:
         raise ValueError("A senha deve conter pelo menos 8 digitos !")
      django_validate_password(value)
      return make_password(value)
   
   
   def validate_CPF(self, value):
      cpf_limpo = ''.join(filter(str.isdigit, str(value)))
      if len(cpf_limpo) != 11:
         raise ValueError("O CPF deve conter 11 digitos !")
      return cpf_limpo
    
   def validate_Tel(self, value):
   
       if len(value) < 11:
          raise ValueError("O telefone deve conter 11 digitos")
       return self.validate_Tel
    
    
    
   def save(self):
       return super().save(Clientes)