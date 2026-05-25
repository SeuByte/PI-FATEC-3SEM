#ClienteSerializer implementa as normas especificas para clientes.
#Exemplo: Para CPF é necessario 11 digitos.
from core.models import Clientes
from datetime import date
from .base_serializer import BaseSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.contrib.auth.hashers import make_password
class ClienteSerializer(BaseSerializer):
   MENSAGENS ={
      
   }
   def to_representation(self):
       data_formatada = self.obj.Data_nasc.strftime("%d-%m-%Y") if self.obj.Data_nasc else None
       return {
         "id": str(self.obj.id),
         "Nome": self.obj.Nome,
         "Email": self.obj.Email,
         "Telefone": self.obj.Telefone,
         "Celular":self.obj.Celular,
         "Data_nasc": data_formatada,
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
   
   def validate_Nome(self, value):
      if not value or str(value).strip() == "":
         raise ValueError("O campo nome é obrigatório.")
      return value
   
   def validate_Endereco(self, value):
      if not value or str(value).strip() == "":
         raise ValueError("O campo Endereço é obrigatório.")
      return value
      
   def validate_Bairro(self, value):
      if not value or str(value).strip() == "":
         raise ValueError("O campo Bairro é obrigatório.")
      return value
      
   def validate_Numero(self, value):
      if not value or str(value).strip() == "":
         raise ValueError("O campo Numero é obrigatório.")
      return value
   
   def validate_Email(self, value):
      if "@" not in value:
         raise ValueError("O email deve conter @ !")
         
      if Clientes.objects(Email=value).first():
         raise ValueError("Esta conta já existe.")
      return value
    
   def validate_CEP(self, value):
      cep_limpo = ''.join(filter(str.isdigit, str(value)))
      if len(cep_limpo) != 8:
         raise ValueError("O CEP deve conter 8 digitos !")
      return cep_limpo 
    
   def validate_Celular(self, value):
      cel_limpo = ''.join(filter(str.isdigit, str(value)))
      if len(cel_limpo) != 11:
         raise ValueError("O celular deve conter 11 digitos")
      return cel_limpo 
    
    
   def validate_Telefone(self, value):
      tel_limpo = ''.join(filter(str.isdigit, str(value)))
      if len(tel_limpo) < 10:
          raise ValueError("O telefone deve conter 10 digitos")
      return tel_limpo
   
   
   def validate_Data_nasc(self, value):
         if isinstance(value, date):
            return value
         
         try:
            data_str = str(value).replace('-', '/')
            
            dia, mes, ano = data_str.split('/')
            
            data_obj = date(int(ano), int(mes), int(dia))
            
         except (ValueError, IndexError):
            raise ValueError("Formato de data inválido. Use o padrão DD/MM/AAAA (ex: 30/05/2026)")

         if data_obj > date.today():
            raise ValueError("A data não pode ser futura")
         
         return data_obj
      
      
   def save(self):
      return super().save(Clientes)

   
   def save(self):
      pass
      
      
    
    
   