import pytest
from bson import ObjectId
from unittest.mock import patch, MagicMock
from rest_framework import status
from decimal import Decimal
from src.api.models import Carrinho
from django.urls import reverse

# =============================================================================
# FORÇANDO O MOCK DO DECORATOR GLOBALMENTE ANTES DE ATIVAR OS ENDPOINTS
# =============================================================================
TEST_EMAIL_CONTEXT = "joao@email.com"

def mock_token_required(func):
    def wrapper(request, *args, **kwargs):
        request.user_email = TEST_EMAIL_CONTEXT
        return func(request, *args, **kwargs)
    return wrapper

try:
    import src.api.utils.auth_utils as auth_utils
    auth_utils.token_required = mock_token_required
except ImportError:
    pass 



    # -------------------------------------------------------------------------
    # TESTES: Adicionar ao Carrinho (POST)
    # -------------------------------------------------------------------------
def test_view_adicionar_produto_com_sucesso(client, cliente_db, produto_db):

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

def test_view_adicionar_produto_inexistente_retorna_400(client, cliente_db):
      

        url = "/api/adicionar_carrinho/"
        payload = {
            "produto_id": str(ObjectId()),  
            "quantidade": 1
        }

        response = client.post(url, payload, format='json')

        assert response.status_code == 400
        assert response.data['message'] == "Produto não encontrado."

def test_view_adicionar_com_cliente_inexistente_no_token(client, produto_db):
       
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
def test_view_listar_carrinho_com_itens(client, cliente_db, produto_db):
    

        #Cria um item no carrinho para teste.
        Carrinho.objects.create(
            Cliente_id=cliente_db.id,
            Itens=[{
                "Produto_id": produto_db.id,
                "Produto": produto_db.Nome,
                "Quantidade": 2,
                "Preco_unitario": Decimal("12.50"),
                "Subtotal": Decimal("25.00")
            }]
        )

        url = "/api/listar_carrinho/"
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data['itens']) == 1
        #Comparando com a string formatada enviada na API do JSON ('25.00')
        assert response.data['valor_total'] == "25.00"

    # -------------------------------------------------------------------------
    # TESTES: Remover do Carrinho (DELETE)
    # -------------------------------------------------------------------------
def test_view_remover_item_com_sucesso(client, cliente_db, produto_db):
        
        # Chaves em iniciais Maiúsculas para evitar erro de FieldDoesNotExist
        Carrinho.objects.create(
            Cliente_id=cliente_db.id,
            Itens=[{
                "Produto_id": produto_db.id,
                "Produto": produto_db.Nome,
                "Quantidade": 1,
                "Preco_unitario": Decimal("12.50"),
                "Subtotal": Decimal("12.50")
            }]
        )

        url = "/api/remover_item_carrinho/"
        payload = {"produto_id": str(produto_db.id)}

        response = client.delete(url, payload, format='json')

        assert response.status_code == 200
        assert response.data['message'] == "Item removido com sucesso!"

def test_view_remover_sem_passar_produto_id(client, cliente_db):
       

        url = "/api/remover_item_carrinho/"
        payload = {} 

        response = client.delete(url, payload, format='json')

        assert response.status_code == 400
        assert "O campo 'produto_id" in response.data['error']

def test_view_remover_com_id_invalid_id_do_mongo(client, cliente_db):
     

        url = "/api/remover_item_carrinho/"
        payload = {"produto_id": "id-invalido-que-quebra-o-bson"}

        response = client.delete(url, payload, format='json')

        assert response.status_code == 400
        assert response.data['error'] == "O ID do produto enviado é invalido."
        
def test_adicionar_ao_carrinho_dados_invalidos(client, auth_setup):
        """
        Este teste envia dados que o serializer vai recusar, 
        forçando a execução do 'return error' na View.
        """
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
        
        # Payload propositalmente errado (ex: quantidade negativa)
        payload = {
            "produto_id": "507f1f17bcf86cd799439011",
            "quantidade": -1 
        }
        
        # O serializer vai falhar, o 'if not serializer.is_valid()' será True,
        # e o 'return error' será executado.
        url = "/api/adicionar_carrinho/"
        response = client.post(url, payload, format='json')
    
        assert response.status_code == 400    
        

CAMINHO_VIEW = 'src.api.views.carrinho_views' 

@pytest.fixture
def mock_cliente():
    """Cria um cliente falso para os testes"""
    cliente = MagicMock()
    cliente.id = "1234567890abcdef12345678"
    cliente.Email = "usuario@teste.com"
    return cliente

@pytest.fixture
def mock_pedido():
    """Cria um pedido falso retornado pelo Service"""
    pedido = MagicMock()
    pedido.id = "pedido_abc123"
    pedido.Status.value = "PENDENTE"
    return pedido

# =====================================================================
# CENÁRIO 1: SUCESSO (201 Created)
# =====================================================================
@patch(f'{CAMINHO_VIEW}.CarrinhoService')
@patch(f'{CAMINHO_VIEW}.FinalizarPedidoSerializer')
@patch(f'{CAMINHO_VIEW}.Clientes')
def test_finalizar_carrinho_sucesso(mock_clientes, mock_serializer_class, mock_service, client, auth_setup, mock_cliente, mock_pedido):
    # 1. Configurando os Mocks (O que o banco e o service vão responder)
    mock_clientes.objects.return_value.first.return_value = mock_cliente
    
    # Configura o mock do serializer para dizer que is_valid() é True
    mock_serializer_instance = mock_serializer_class.return_value
    mock_serializer_instance.is_valid.return_value = True
    mock_serializer_instance.context.get.return_value = MagicMock() # Carrinho validado falso
    
    # Configura o service para retornar nosso pedido falso
    mock_service.finalizar_carrinho.return_value = mock_pedido
    
    # 2. Executando a requisição
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
    payload = {"forma_pagamento": "PIX"}
    
    url = reverse('finalizar_carrinho') 
    response = client.post(url, data=payload, format='json')
    
    # 3. Asserts
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == "Pedido finalizado com sucesso!"
    assert response.data['data']['pedido_id'] == "pedido_abc123"
    
    # Garante que o Service foi chamado com os parâmetros certos
    mock_service.finalizar_carrinho.assert_called_once()

# =====================================================================
# CENÁRIO 2: CLIENTE NÃO ENCONTRADO (404 Not Found)
# =====================================================================
@patch(f'{CAMINHO_VIEW}.Clientes')
def test_finalizar_carrinho_cliente_nao_encontrado(mock_clientes, client, auth_setup):
    # Simula que a busca no banco retornou None
    mock_clientes.objects.return_value.first.return_value = None
    
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
    url = reverse('finalizar_carrinho') 
    response = client.post(url, data={}, format='json')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['message'] == "Cliente não encontrado."

# =====================================================================
# CENÁRIO 3: SERIALIZER INVÁLIDO (400 Bad Request)
# =====================================================================
@patch(f'{CAMINHO_VIEW}.FinalizarPedidoSerializer')
@patch(f'{CAMINHO_VIEW}.Clientes')
def test_finalizar_carrinho_dados_invalidos(mock_clientes, mock_serializer_class, client, auth_setup, mock_cliente):
    mock_clientes.objects.return_value.first.return_value = mock_cliente
    
    # Simula que a validação falhou e retorna os erros
    mock_serializer_instance = mock_serializer_class.return_value
    mock_serializer_instance.is_valid.return_value = False
    mock_serializer_instance.errors = {"forma_pagamento": ["Este campo é obrigatório."]}
    
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
    url = reverse('finalizar_carrinho') 
    response = client.post(url, data={}, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "forma_pagamento" in response.data['message']

# =====================================================================
# CENÁRIO 4: ERRO DE REGRA DE NEGÓCIO DO SERVICE (400 Bad Request)
# =====================================================================
@patch(f'{CAMINHO_VIEW}.CarrinhoService')
@patch(f'{CAMINHO_VIEW}.FinalizarPedidoSerializer')
@patch(f'{CAMINHO_VIEW}.Clientes')
def test_finalizar_carrinho_erro_regra_negocio(mock_clientes, mock_serializer_class, mock_service, client, auth_setup, mock_cliente):
    mock_clientes.objects.return_value.first.return_value = mock_cliente
    
    mock_serializer_instance = mock_serializer_class.return_value
    mock_serializer_instance.is_valid.return_value = True
    
    # Simula o Service "estourando" um ValueError (ex: Carrinho vazio)
    mock_service.finalizar_carrinho.side_effect = ValueError("O carrinho está vazio.")
    
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
    url = reverse('finalizar_carrinho') 
    response = client.post(url, data={}, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['message'] == "O carrinho está vazio."

# =====================================================================
# CENÁRIO 5: ERRO INTERNO NO SERVIDOR (500 Internal Server Error)
# =====================================================================
@patch(f'{CAMINHO_VIEW}.CarrinhoService')
@patch(f'{CAMINHO_VIEW}.FinalizarPedidoSerializer')
@patch(f'{CAMINHO_VIEW}.Clientes')
def test_finalizar_carrinho_erro_interno_servidor(mock_clientes, mock_serializer_class, mock_service, client, auth_setup, mock_cliente):
    mock_clientes.objects.return_value.first.return_value = mock_cliente
    
    mock_serializer_instance = mock_serializer_class.return_value
    mock_serializer_instance.is_valid.return_value = True
    
    # Simula um erro inesperado no banco ou na rede
    mock_service.finalizar_carrinho.side_effect = Exception("Erro bizarro de conexão com MongoDB")
    
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
    url = reverse('finalizar_carrinho') 
    response = client.post(url, data={"forma_pagamento": "PIX"}, format='json')
    
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data['message'] == "Erro interno ao finalizar o carrinho"
    
# =====================================================================
# CENÁRIOS 6: Atualizar Quantidade (PATCH)
# =====================================================================

@patch(f'{CAMINHO_VIEW}.CarrinhoService')
@patch(f'{CAMINHO_VIEW}.CarrinhoSerializer')
@patch(f'{CAMINHO_VIEW}.Clientes')
def test_atualizar_quantidade_sucesso(mock_clientes, mock_serializer_class, mock_service, client, auth_setup, mock_cliente):
    # 1. Configuração dos Mocks
    mock_clientes.objects.return_value.first.return_value = mock_cliente
    
    mock_serializer_instance = mock_serializer_class.return_value
    mock_serializer_instance.is_valid.return_value = True
    mock_serializer_instance.validated_data = {"produto_id": "prod123", "quantidade": 5}
    
    # 2. Execução
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
    payload = {"produto_id": "prod123", "quantidade": 5}
    
    url = reverse('editar_carrinho') # Certifique-se que o nome da rota é esse
    response = client.patch(url, data=payload, format='json')
    
    # 3. Asserts
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == "Carrinho atualizado com sucesso!"
    mock_service.atualizar_quantidade.assert_called_once()

@patch(f'{CAMINHO_VIEW}.CarrinhoSerializer')
@patch(f'{CAMINHO_VIEW}.Clientes')
def test_atualizar_quantidade_serializer_invalido(mock_clientes, mock_serializer_class, client, auth_setup):
    # 1. Configura o Serializer para falhar
    mock_serializer_instance = mock_serializer_class.return_value
    mock_serializer_instance.is_valid.return_value = False
    mock_serializer_instance.errors = {"quantidade": ["Este campo é obrigatório."]}
    
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
    response = client.patch(reverse('editar_carrinho'), data={}, format='json')
    
    assert response.status_code == 400
    assert "quantidade" in response.data['message']

@patch(f'{CAMINHO_VIEW}.CarrinhoService')
@patch(f'{CAMINHO_VIEW}.CarrinhoSerializer')
@patch(f'{CAMINHO_VIEW}.Clientes')
def test_atualizar_quantidade_erro_negocio(mock_clientes, mock_serializer_class, mock_service, client, auth_setup, mock_cliente):
    mock_clientes.objects.return_value.first.return_value = mock_cliente
    
    mock_serializer_instance = mock_serializer_class.return_value
    mock_serializer_instance.is_valid.return_value = True
    mock_serializer_instance.validated_data = {"produto_id": "prod123", "quantidade": 5}
    
    # Simula erro de negócio (ex: item não existe no carrinho)
    mock_service.atualizar_quantidade.side_effect = ValueError("Item não encontrado no carrinho.")
    
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
    response = client.patch(reverse('editar_carrinho'), data={"produto_id": "prod123", "quantidade": 5}, format='json')
    
    assert response.status_code == 400
    assert response.data['message'] == "Item não encontrado no carrinho."
    

    
def test_adicionar_ao_carrinho_serializer_invalido(client, auth_setup):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
    
    # Envia um dado que viola a regra do serializer (ex: quantidade negativa)
    payload = {"produto_id": "507f1f17bcf86cd799439011", "quantidade": -5}
    
    response = client.post("/api/adicionar_carrinho/", payload, format='json')
    
   
    assert response.status_code == 400
