import os
import django
import pytest
from mongoengine import connect, disconnect
from src.api.serializers.produto_serializer import ProdutoSerializer
from decimal import Decimal

# --- CONFIGURAÇÃO ANTES DE QUALQUER IMPORT ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.janete.settings')
django.setup()

from rest_framework.test import APIClient
from src.api.models import Produtos
from bson.decimal128 import Decimal128

@pytest.fixture(autouse=True)
def setup_db():
    disconnect()
    # Porta 27018 (Docker), ignorando a porta 27017 (Windows)
    connect('test_db_teste', host='localhost', port=27018)
    Produtos.objects.delete()
    yield
    disconnect()

@pytest.fixture
def client():
    return APIClient()

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

class TestProdutoViews:

    # --- SUCESSO ---
    
    # /// PESQUISA ///
    def test_listar_produtos_sucesso(self, client, produto_db):
        #1. Faz a requisição pra URL 
        response = client.get('/api/produtos/')
        #2. Caso a requisição retorne 200, o teste continua.
        assert response.status_code == 200

    def test_listar_produto_id_sucesso(self, client, produto_db):
        response = client.get(f'/api/produtos/{produto_db.id}/')
        assert response.status_code == 200
        
    def test_filtrar_produtos_por_grupo(self, client, produto_db):
        # Nenhum outro produto alem dos Graos é exibido
        response = client.get('/api/produtos/?grupo=Graos')
        print(f"\nRESPOSTA DO FILTRO: {response.data}")
        assert response.status_code == 200  
        lista_produtos = response.data['data']
        # Verifica se o produto retornado realmente pertence ao grupo
        assert len(lista_produtos) > 0
        assert lista_produtos[0]['Grupo'] == 'Graos'            
       
    # /// CRIAR PRODUTO ///
    def test_criar_produto_sucesso(self, client):
        payload = {"Nome": "amendoim", "Estoque": "5.0", "Unidade": "KG", "Valor_venda": "10.00", "Grupo": "Graos", "Preco_100g": "1.00"}
        response = client.post('/api/criar_produto/', data=payload, format='json')
        
        if response.status_code != 200:
            
            print(f"\nERRO DO CRIAR PRODUTO: {response.data}")
            
        assert response.status_code == 200
    # /////////////////////////////////////////////////////////////////////////////////////////////    
     
     
        
    # /// EDITAR PRODUTO ///
    def test_editar_produto_sucesso(self, client, produto_db):
        #Cria o produto ficticio
        payload = {"Nome": "Arroz Nobre", "Estoque": "5.0", "Unidade": "KG", "Valor_venda": "103.00", "Grupo": "Graos", "Preco_100g": "12.00"}
        
        # 1. Faz a edição do produto criado
        response = client.put(f'/api/editar_produto/{produto_db.id}/', data=payload, format='json')
        assert response.status_code == 200
        
        # 2. Recarrega o objeto do banco para ver se ele mudou
        produto_db.reload() 
        print(f"\n--- DADO ATUALIZADO NO BANCO: {produto_db.to_mongo().to_dict()} ---")
        if response.status_code != 200 or response.status_code != 400:
            print(f"\nERRO DO EDITAR PRODUTO: {response.data}")
        # 3. Compara com o nome depois de recarregado o banco.
        assert produto_db.Nome == "Arroz Nobre"    
        
    def test_atualizar_preco_produto(self, client, produto_db):
        # Envia dados que alteram o preço
        payload = {"Nome": "Arroz Integral", "Estoque": "10.0", "Unidade": "KG", 
                "Valor_venda": "550.00", "Grupo": "Graos", "Preco_100g": "13.00"}
        
        #Faz a requisição e envia pra URL correta
        response = client.put(f'/api/editar_produto/{produto_db.id}/', data=payload, format='json')
        #Caso a requisicao retorne 200, o teste continua
        assert response.status_code == 200
        
        produto_db.reload()
        # Verifica se a matemática bate
        assert produto_db.Valor_venda == Decimal("550.00")
        
        
    def test_editar_produto_dados_idênticos(self, client, produto_db):
        # Envia os mesmos dados que já estão no banco
        payload = {
            "Nome": "Arroz integral", # Nome original
            "Estoque": "10.0", 
            "Unidade": "KG", 
            "Valor_venda": "500.00", 
            "Grupo": "Graos", 
            "Preco_100g": "12.50"
        }
        
        response = client.put(f'/api/editar_produto/{produto_db.id}/', data=payload, format='json')
        # Deve aceitar, pois é o mesmo produto
        assert response.status_code == 200
        
        
             
    # /////////////////////////////////////////////////////////////////////////////////////////////        
    
    #Teste para deletar o produto
    def test_deletar_produto_sucesso(self, client, produto_db):
        # pega a URL certa do teste
        response = client.delete(f'/api/deletar_produto/{produto_db.id}/')
        #Verifica se a API confirmou a deleção com sucesso.
        assert response.status_code == 200






    # --- FALHA ---
    def test_criar_produto_invalido(self, client):
        #Tenta criar apenas com nome vazio
        payload = {"Nome": ""}
        #Envia a requisicao pra URL
        response = client.post('/api/criar_produto/', data=payload, format='json')
        assert response.status_code == 400
        
    def test_criar_produto_estoque_negativo(self, client):
        #Cria um dado ficticio pra teste com valor errado.
        payload = {
                "Nome": "Pimenta do reino", 
                "Estoque": -10.0,  # Valor inválido
                "Unidade": "KG", 
                "Valor_venda": 10.00,
                "Grupo": "Vegetais",
                "Preco_100g": 90.00
            }
        #Envia a requisição com dado errado
        response = client.post('/api/criar_produto/', data=payload, format='json')
        # O sistema deve impedir isso! aqui o erro é o sucesso.
        assert response.status_code == 400

    def test_deletar_produto_nao_encontrado(self, client):
        #Manda uma requisição na URL deletar, com um ObjectID que não existe
        response = client.delete('/api/deletar_produto/507f1f77bcf86cd799439011/')
        #O sistema barra por não encontrar o ObjectID
        assert response.status_code == 404
        
        
    def test_editar_produto_conflito_nome(self, client, produto_db):
        # 1. Cria um SEGUNDO produto no banco (o Feijão)
        Produtos.objects.create(
            Nome="Feijão", 
            Estoque=Decimal128("5.0"), 
            Unidade="KG", 
            Valor_venda=Decimal128("10.00"), 
            Grupo="Graos", 
            Preco_100g=Decimal128("1.00")
        )
        
        # 2. Tenta editar o Arroz (produto_db) para o nome "Feijão"
        # Isso deve disparar o erro de validação de duplicidade
        payload = {
            "Nome": "Feijão", 
            "Estoque": "5.0", 
            "Unidade": "KG", 
            "Valor_venda": "10.00", 
            "Grupo": "Graos", 
            "Preco_100g": "1.00"
        }
        
        response = client.put(f'/api/editar_produto/{produto_db.id}/', data=payload, format='json')
        
        # O sistema deve barrar com 400 por causa da regra de unicidade
        assert response.status_code == 400
        
        # Opcional: Verifica se a mensagem de erro é a que esperamos
        assert "Já existe um produto com esse nome" in str(response.data['message']) 
        print(f"\n--- MENSAGEM CAPTURADA: {response.data['message']} ---") 
  