import os
import django
from django.conf import settings

# --- CONFIGURAÇÃO ANTES DE QUALQUER IMPORT ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.janete.settings')
django.setup()

import pytest
from mongoengine import connect, disconnect
from rest_framework.test import APIClient
from src.api.models import Produtos
from bson.decimal128 import Decimal128

# 1. Configuração do banco para todos os testes
@pytest.fixture(autouse=True)
def setup_db():
    disconnect()
    connect('test_db_teste', host='localhost', port=27018, alias='default')
    Produtos.objects.delete()
    yield
    disconnect()

# 2. Fixture para o cliente da API
@pytest.fixture
def client():
    return APIClient()

# 3. Fixture para criar um produto de teste
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