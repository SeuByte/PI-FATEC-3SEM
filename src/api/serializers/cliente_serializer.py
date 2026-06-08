#ClienteSerializer implementa as normas especificas para clientes.
#Exemplo: Para CPF é necessario 11 digitos.
import requests
from src.api.models import Clientes
from datetime import datetime, date
from .base_serializer import BaseSerializer
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.contrib.auth.hashers import make_password


#validação de CPF
def validar_cpf_matematicamente(cpf):
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        value = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            return False
    return True

class ClienteSerializer(BaseSerializer):
  
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
    # Limpa o CPF
    cpf_limpo = ''.join(filter(str.isdigit, str(value)))
    
    # 1. Verifica tamanho
    if len(cpf_limpo) != 11:
        raise ValueError("O CPF deve conter exatamente 11 dígitos.")
    
    # 2. Verifica se é matematicamente válido
    if not validar_cpf_matematicamente(cpf_limpo):
        raise ValueError("CPF inválido.")
        
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
         raise ValueError("O CEP deve conter 8 dígitos.")
      
      # Validação via API externa (ViaCEP)
      response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/")
      data = response.json()
      
      if 'erro' in data:
         raise ValueError("CEP não encontrado na base dos Correios.")
         
      return cep_limpo
    
   def validate_Celular(self, value):
      cel_limpo = ''.join(filter(str.isdigit, str(value)))
      if len(cel_limpo) != 11:
         raise ValueError("O celular deve conter 11 digitos")
      return cel_limpo 
    
    
   def validate_Telefone(self, value):
      tel_limpo = ''.join(filter(str.isdigit, str(value)))
      if len(tel_limpo) != 10:
          raise ValueError("O telefone deve conter 10 digitos")
  
      return tel_limpo
   
   


   def validate_Data_nasc(self, value):
      # 1. Se já for um objeto date, retorna direto
      if isinstance(value, date):
         return value

      # 2. Tenta converter de string para data
      # Formatos suportados: DD/MM/AAAA, DD-MM-AAAA, AAAA-MM-DD
      formatos_possiveis = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"]
      
      for formato in formatos_possiveis:
         try:
               data_obj = datetime.strptime(str(value), formato).date()
               
               # Validação de data futura
               if data_obj > date.today():
                  raise ValueError("A data de nascimento não pode ser no futuro.")
               
               return data_obj
         except ValueError:
               continue # Tenta o próximo formato

      # 3. Se nenhum formato funcionou, lança erro
      raise ValueError("Formato de data inválido. Use DD/MM/AAAA ou AAAA-MM-DD.")
         
         
   def save(self):
      if not hasattr(self, 'obj') or self.obj is None:
            self.obj = Clientes(**self.validated_data)
      else:
            # Se for atualização, atualiza os campos
          for attr, value in self.validated_data.items():
               setattr(self.obj, attr, value)
        
      return self.obj.save()

   
   
      
      
    
    
   