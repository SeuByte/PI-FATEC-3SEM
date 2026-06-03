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

#  Configuração do banco para todos os testes
@pytest.fixture(autouse=True)
def setup_db():
    disconnect()
    connect('test_db_teste', host='mongodb://localhost:27017', port=27017)
    Produtos.objects.delete()
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
    
    
