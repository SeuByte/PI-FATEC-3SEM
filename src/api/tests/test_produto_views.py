from decimal import Decimal
from src.api.models import Produtos
from bson.decimal128 import Decimal128
import pytest

# --- SUCESSO ---

# /// PESQUISA ///
def test_listar_produtos_sucesso(client, produto_db):
    response = client.get('/api/produtos/')
    assert response.status_code == 200

def test_listar_produto_id_sucesso(client, produto_db):
    response = client.get(f'/api/produtos/{produto_db.id}/')
    assert response.status_code == 200
    
def test_filtrar_produtos_por_grupo(client, produto_db):
    response = client.get('/api/produtos/?grupo=Graos')
    assert response.status_code == 200  
    lista_produtos = response.data['data']
    assert len(lista_produtos) > 0
    assert lista_produtos[0]['Grupo'] == 'Graos'            

# /// CRIAR PRODUTO ///
def test_criar_produto_sucesso(client):
    payload = {"Nome": "amendoim", "Estoque": "5.0", "Unidade": "KG", "Valor_venda": "10.00", "Grupo": "Graos", "Preco_100g": "1.00"}
    response = client.post('/api/criar_produto/', data=payload, format='json')
    assert response.status_code == 200

# /// EDITAR PRODUTO ///
def test_editar_produto_sucesso(client, produto_db):
    payload = {"Nome": "Arroz Nobre", "Estoque": "5.0", "Unidade": "KG", "Valor_venda": "103.00", "Grupo": "Graos", "Preco_100g": "12.00"}
    response = client.put(f'/api/editar_produto/{produto_db.id}/', data=payload, format='json')
    assert response.status_code == 200
    
    produto_db.reload() 
    assert produto_db.Nome == "Arroz Nobre"    
    
def test_atualizar_preco_produto(client, produto_db):
    payload = {"Nome": "Arroz Integral", "Estoque": "10.0", "Unidade": "KG", 
               "Valor_venda": "550.00", "Grupo": "Graos", "Preco_100g": "13.00"}
    
    response = client.put(f'/api/editar_produto/{produto_db.id}/', data=payload, format='json')
    assert response.status_code == 200
    
    produto_db.reload()
    assert produto_db.Valor_venda == Decimal("550.00")
    
def test_editar_produto_dados_idênticos(client, produto_db):
    payload = {
        "Nome": "Arroz integral", 
        "Estoque": "10.0", 
        "Unidade": "KG", 
        "Valor_venda": "500.00", 
        "Grupo": "Graos", 
        "Preco_100g": "12.50"
    }
    response = client.put(f'/api/editar_produto/{produto_db.id}/', data=payload, format='json')
    assert response.status_code == 200

# /// DELETAR PRODUTO ///
def test_deletar_produto_sucesso(client, produto_db):
    response = client.delete(f'/api/deletar_produto/{produto_db.id}/')
    assert response.status_code == 200

# --- FALHA ---
def test_criar_produto_invalido(client):
    payload = {"Nome": ""}
    response = client.post('/api/criar_produto/', data=payload, format='json')
    assert response.status_code == 400
    
def test_criar_produto_estoque_negativo(client):
    payload = {
            "Nome": "Pimenta do reino", 
            "Estoque": -10.0,
            "Unidade": "KG", 
            "Valor_venda": 10.00,
            "Grupo": "Vegetais",
            "Preco_100g": 90.00
        }
    response = client.post('/api/criar_produto/', data=payload, format='json')
    assert response.status_code == 400

def test_deletar_produto_nao_encontrado(client):
    response = client.delete('/api/deletar_produto/507f1f77bcf86cd799439011/')
    assert response.status_code == 404
    
def test_editar_produto_conflito_nome(client, produto_db):
    Produtos.objects.create(
        Nome="Feijão", 
        Estoque=Decimal128("5.0"), 
        Unidade="KG", 
        Valor_venda=Decimal128("10.00"), 
        Grupo="Graos", 
        Preco_100g=Decimal128("1.00")
    )
    
    payload = {
        "Nome": "Feijão", 
        "Estoque": "5.0", 
        "Unidade": "KG", 
        "Valor_venda": "10.00", 
        "Grupo": "Graos", 
        "Preco_100g": "1.00"
    }
    
    response = client.put(f'/api/editar_produto/{produto_db.id}/', data=payload, format='json')
    assert response.status_code == 400
    assert "Já existe um produto com esse nome" in str(response.data)