from decimal import Decimal
from src.api.models import Produtos
from src.api.services.produto_service import ProdutosService
from bson.decimal128 import Decimal128
import pytest

# --- Teste de criação com sucesso ---
def test_service_criar_produto_sucesso():
    dados = {
        "Nome": "Feijão Preto",
        "Estoque": Decimal128("10.00"),
        "Unidade": "KG",
        "Valor_venda": Decimal128("8.00"),
        "Grupo": "Graos",
        "Preco_100g": Decimal128("0.80")
    }
    produto = ProdutosService.criar(dados)
    assert produto.id is not None
    assert produto.Nome == "Feijão Preto"

# --- Teste de atualização com sucesso ---
def test_service_atualizar_produto_sucesso(produto_db):
    # Cria o dado fictício
    dados_atualizados = {"Valor_venda": "600.00"}
    resultado = ProdutosService.atualizar(produto_db.id, dados_atualizados)
    # Se a requisição deu certo, ele segue a função
    assert resultado['status'] == 'sucesso'
    
    # Banco de dados é recarregado
    produto_db.reload()
    
    # Como o Valor_venda agora é um Decimal do Python, dá pra comparar diretamente
    assert produto_db.Valor_venda == Decimal("600.00")

# --- Teste de deleção ---
def test_service_deletar_produto_sucesso(produto_db):
    resultado = ProdutosService.deletar(produto_db.id)
    # O deletar retorna apenas True/False
    assert resultado is True 
    assert Produtos.objects(id=produto_db.id).first() is None

# --- Teste de erro ao atualizar produto inexistente ---
def test_service_atualizar_produto_nao_encontrado():
    resultado = ProdutosService.atualizar("507f1f77bcf86cd799439011", {"Nome": "Novo"})
    assert resultado['code'] == 404
    assert resultado['status'] == 'erro'