import pytest
from bson import ObjectId
from unittest.mock import patch
from src.api.models import Carrinho, Clientes

# =============================================================================
# FORÇANDO O MOCK DO DECORATOR GLOBALMENTE ANTES DE ATIVAR OS ENDPOINTS
# =============================================================================
# Armazenamos o email padrão de teste em uma variável global simples
TEST_EMAIL_CONTEXT = "joao@email.com"

def mock_token_required(func):
    def wrapper(request, *args, **kwargs):
        # Injeta dinamicamente o e-mail que estiver setado no contexto atual do teste
        request.user_email = TEST_EMAIL_CONTEXT
        return func(request, *args, **kwargs)
    return wrapper

# Aplica o mock no utilitário de autenticação antes do Django interpretar as views nos testes
try:
    import src.api.utils.auth_utils as auth_utils
    auth_utils.token_required = mock_token_required
except ImportError:
    pass


class TestCarrinhoViews:

    # -------------------------------------------------------------------------
    # TESTES: Adicionar ao Carrinho (POST)
    # -------------------------------------------------------------------------
    def test_view_adicionar_produto_com_sucesso(self, client, cliente_db, produto_db):
        # """Testa o endpoint adicionando produto com dados válidos."""
        global TEST_EMAIL_CONTEXT
        TEST_EMAIL_CONTEXT = cliente_db.Email  # Garante que usa o email correto da fixture

        url = "/api/adicionar_carrinho/"  
        payload = {
            "produto_id": str(produto_db.id),
            "quantidade": 3
        }

        response = client.post(url, payload, format='json')

        assert response.status_code == 201
        assert response.data['message'] == "Produto adicionado ao carrinho com sucesso !"
        
        carrinho = Carrinho.objects(Cliente_id=cliente_db.id).first()
        assert carrinho is not None
        assert str(carrinho.Cliente_id) == str(cliente_db.id)

    def test_view_adicionar_produto_inexistente_retorna_400(self, client, cliente_db):
        # """Deve retornar erro 400 se o produto não existir no banco."""
        global TEST_EMAIL_CONTEXT
        TEST_EMAIL_CONTEXT = cliente_db.Email

        url = "/api/adicionar_carrinho/"
        payload = {
            "produto_id": str(ObjectId()),  
            "quantidade": 1
        }

        response = client.post(url, payload, format='json')

        assert response.status_code == 400
        assert response.data['message'] == "Produto não encontrado."

    def test_view_adicionar_com_cliente_inexistente_no_token(self, client, produto_db):
        # """Testa o comportamento se o e-mail do token não for achado no banco."""
        global TEST_EMAIL_CONTEXT
        TEST_EMAIL_CONTEXT = "fantasma@email.com"

        url = "/api/adicionar_carrinho/"
        payload = {
            "produto_id": str(produto_db.id),
            "quantidade": 1
        }
        
        response = client.post(url, payload, format='json')

        assert response.status_code == 404
        assert response.data['message'] == "Cliente não encontrado."

    # -------------------------------------------------------------------------
    # TESTES: Listar Carrinho (GET)
    # -------------------------------------------------------------------------
    def test_view_listar_carrinho_com_itens(self, client, cliente_db, produto_db):
        # """Cria um carrinho no banco e testa a rota de listagem."""
        global TEST_EMAIL_CONTEXT
        TEST_EMAIL_CONTEXT = cliente_db.Email

        Carrinho.objects.create(
            Cliente_id=cliente_db.id,
            Itens=[{
                "produto_id": produto_db.id,
                "produto": produto_db.Nome,
                "quantidade": 2,
                "preco_unitario": 12.50,
                "subtotal": 25.00
            }]
        )

        url = "/api/listar_carrinho/"
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data['itens']) == 1
        assert response.data['valor_total'] == 25.00

    # -------------------------------------------------------------------------
    # TESTES: Remover do Carrinho (DELETE)
    # -------------------------------------------------------------------------
    def test_view_remover_item_com_sucesso(self, client, cliente_db, produto_db):
        # """Garante a remoção do item pela rota remover_item_carrinho."""
        global TEST_EMAIL_CONTEXT
        TEST_EMAIL_CONTEXT = cliente_db.Email

        Carrinho.objects.create(
            Cliente_id=cliente_db.id,
            Itens=[{
                "produto_id": produto_db.id,
                "produto": produto_db.Nome,
                "quantidade": 1,
                "preco_unitario": 12.50,
                "subtotal": 12.50
            }]
        )

        url = "/api/remover_item_carrinho/"
        payload = {"produto_id": str(produto_db.id)}

        response = client.delete(url, payload, format='json')

        assert response.status_code == 200
        assert response.data['message'] == "Item removido com sucesso!"

    def test_view_remover_sem_passar_produto_id(self, client, cliente_db):
        # """Valida o erro 400 ao tentar deletar sem mandar o produto_id."""
        global TEST_EMAIL_CONTEXT
        TEST_EMAIL_CONTEXT = cliente_db.Email

        url = "/api/remover_item_carrinho/"
        payload = {} 

        response = client.delete(url, payload, format='json')

        assert response.status_code == 400
        assert "O campo 'produto_id" in response.data['error']

    def test_view_remover_com_id_invalid_id_do_mongo(self, client, cliente_db):
        # """Valida se captura o InvalidId do BSON enviando ID corrompido."""
        global TEST_EMAIL_CONTEXT
        TEST_EMAIL_CONTEXT = cliente_db.Email

        url = "/api/remover_item_carrinho/"
        payload = {"produto_id": "id-invalido-que-quebra-o-bson"}

        response = client.delete(url, payload, format='json')

        assert response.status_code == 400
        assert response.data['error'] == "O ID do produto enviado é invalido."