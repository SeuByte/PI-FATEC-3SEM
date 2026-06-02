
import os
import django
import pytest
# 1. Primeiro configuramos o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.janete.settings')
django.setup()



import pytest
from rest_framework.test import APIClient
from src.api.models import Produtos
from bson.decimal128 import Decimal128
from mongoengine import connect, disconnect


@pytest.fixture(autouse=True)
def setup_db():
    disconnect() # Desconecta de qualquer banco real
    connect('mongoenginetest', host='mongomock://localhost')
    yield
    disconnect()



@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def produto_db():
    # Limpa o banco antes de criar o produto de teste
    Produtos.objects.delete()
    return Produtos.objects.create(
        Nome="Arroz integral",
        Estoque=Decimal128("10"),
        Unidade="KG",
        Valor_venda=Decimal128("500.00"),
        Grupo="Graos",
        Preco_100g=Decimal128("12.50")
    )

class TestProdutoViews:

    def test_listar_produtos_sucesso(self, client, produto_db):
        # Substitua '/api/produtos/' pela rota real definida no seu urls.py
        response = client.get('/api/produtos/') 
        assert response.status_code == 200
        # Verifica se o retorno contém dados
        assert len(response.json()['data']) > 0

    def test_criar_produto_sucesso(self, client):
        dados = {
            "Nome": "Feijao",
            "Estoque": 50,
            "Unidade": "KG",
            "Valor_venda": 10.00,
            "Grupo": "Graos",
            "Preco_100g": 1.00
        }
        response = client.post('/api/produtos/', dados, format='json')
        assert response.status_code == 200 
        assert Produtos.objects(Nome="Feijao").first() is not None

    def test_deletar_produto_sucesso(self, client, produto_db):
        url = f'/api/produtos/{produto_db.id}/'
        response = client.delete(url)
        assert response.status_code == 200
        assert Produtos.objects.count() == 0