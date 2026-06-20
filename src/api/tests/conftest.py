import os
import django

# --- CONFIGURAÇÃO ANTES DE QUALQUER IMPORT ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.janete.settings')
django.setup()

import pytest
from mongoengine import connect, disconnect, get_connection
from pymongo.errors import ConnectionFailure
from rest_framework.test import APIClient
from src.api.models import Produtos, Clientes
from bson import Decimal128, ObjectId
from django.contrib.auth.hashers import make_password
from types import SimpleNamespace
from django.urls import reverse
from src.api.utils.auth_utils import gerar_token
from src.usuarios.models import FuncionarioModel

#  Configuração do banco para apagar sempre os dados testes
@pytest.fixture(autouse=True)
def force_db_connection():

    try:
        get_connection(alias="default")
    except Exception:
        connect(
            "teste_db_teste",
            host="mongodb://localhost:27017",
            alias="default"
        )

    Clientes.objects.delete()
    Produtos.objects.delete()

    yield

    Clientes.objects.delete()
    Produtos.objects.delete()
    

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
        "Telefone": "1199999999",
        "Celular": "11999999999",
        "Data_nasc": "1990-01-01",
        "CPF": "12345678909",
        "CEP": "01310000",
        "Endereco": "Rua Exemplo",
        "Bairro": "Centro",
        "Numero": "100",
        "Cidade": "Araras",
        "Estado": "SP"
    }

@pytest.fixture
def cliente_db(dados_cliente_valido):
    # 1. Faz a cópia para não sujar a fixture base
    dados = dados_cliente_valido.copy()
    
    # 2. OBRIGATÓRIO: Hashear a senha ANTES de instanciar o objeto
    # Isso garante que o objeto 'cliente' já nasça com o hash
    dados['Senha'] = make_password(dados['Senha'])
    
    # 3. Instancia e salva
    cliente = Clientes(**dados)
    cliente.save()
    
    # 4. Reload é fundamental para ver o que realmente está no banco
    cliente.reload()
    return cliente
@pytest.fixture
def usuario_autenticado(cliente_db):
    #  um "objeto fake" que o Django vai aceitar
    # O DRF só precisa que o objeto tenha is_authenticated = True
    user_fake = SimpleNamespace(
        pk=ObjectId(cliente_db.id),
        email=cliente_db.Email
        
    )
    return user_fake


#Rota de teste para o arquivo test_auth_login    
@pytest.fixture
def auth_setup():
    return {
        "url": reverse('rota-de-teste'),
        "token": gerar_token("usuario@teste.com")
    }

@pytest.fixture
def funcionario_db(db):

    return FuncionarioModel.objects.create(
        nome_completo="João Silva",
        email="funcionario@email.com",
        telefone="11999999999",
        senha="123456",
        cargo="Analista"
    )
    
    