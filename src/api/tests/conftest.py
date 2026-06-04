import os
import django

# --- CONFIGURAÇÃO ANTES DE QUALQUER IMPORT ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.janete.settings')
django.setup()

import pytest
from mongoengine import connect, disconnect
from rest_framework.test import APIClient
from src.api.models import Produtos, Clientes
from bson.decimal128 import Decimal128
from django.contrib.auth.hashers import make_password

#  Configuração do banco para apagar sempre os dados testes
@pytest.fixture(autouse=True)
def setup_db():
    disconnect()
    connect('test_db_teste', host='mongodb://localhost:27017', port=27017)
    Produtos.objects.delete()
    Clientes.objects.all().delete()

    yield
    disconnect()
    

#  Fixture para o cliente da API
@pytest.fixture
def client():
    return APIClient()

# Fixture para criar um produto de teste
@pytest.fixture
def produto_db():
    return Produtos.objects.create(
        Nome="Arroz integral",
        Estoque=Decimal128("10.00"),
        Unidade="KG",
        Valor_venda=Decimal128("500.00"),
        Grupo="Graos",
        Preco_100g=Decimal128("12.50")
    )
    

@pytest.fixture
def dados_cliente_valido():
    return {
        "Nome": "João Silva",
        "Email": "joao@email.com",
        "Senha": "SenhaForte123!@#",
        "Telefone": "11999999999",
        "Data_nasc": "1990-01-01",
        "CPF": "12345678901",
        "CEP": "12345678",
        "Endereco": "Rua Exemplo",
        "Bairro": "Centro",
        "Numero": "100",
        "Cidade": "Araras",
        "Estado": "SP"
    }

@pytest.fixture
def cliente_db(dados_cliente_valido):
    # Usa o dicionário da fixture acima para salvar no banco
  
    
    dados = dados_cliente_valido.copy()
    dados['Senha'] = make_password(dados['Senha'])
    return Clientes.objects.create(**dados)

    
    
