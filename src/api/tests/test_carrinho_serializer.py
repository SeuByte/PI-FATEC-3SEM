import pytest
from bson import ObjectId
from src.api.serializers.carrinho_serializer import CarrinhoSerializer, FinalizarPedidoSerializer
from src.api.models import Carrinho


# -------------------------------------------------------------------------
# TESTES: Casos de Sucesso
# -------------------------------------------------------------------------

def test_serializer_com_dados_validos():
    """Deve validar com sucesso quando o produto_id e a quantidade estão corretos."""
    id_valido = str(ObjectId())  # Gera um ID de 24 caracteres hexadecimais
    dados_entrada = {
        "produto_id": id_valido,
        "quantidade": 5
    }

    serializer = CarrinhoSerializer(data=dados_entrada)
    
    assert serializer.is_valid() is True
    assert serializer.validated_data["produto_id"] == id_valido
    assert serializer.validated_data["quantidade"] == 5


def test_serializer_converte_quantidade_string_numerica_para_int():
    """Garante que se enviarem '10' (string), o serializer converte para 10 (int)."""
    id_valido = str(ObjectId())
    dados_entrada = {
        "produto_id": id_valido,
        "quantidade": "10"
    }

    serializer = CarrinhoSerializer(data=dados_entrada)
    
    assert serializer.is_valid() is True
    assert serializer.validated_data["quantidade"] == 10
    assert isinstance(serializer.validated_data["quantidade"], int)


# -------------------------------------------------------------------------
# TESTES: Validação de produto_id
# -------------------------------------------------------------------------

def test_serializer_com_produto_id_invalido_deve_falhar():
    """Deve falhar na validação se o produto_id não for um ObjectId válido."""
    dados_entrada = {
        "produto_id": "id-invalido-curto",
        "quantidade": 2
    }

    serializer = CarrinhoSerializer(data=dados_entrada)
    
    assert serializer.is_valid() is False
    assert "produto_id" in serializer.errors
    assert "O ID do produto deve conter 24 caracteres" in str(serializer.errors["produto_id"])


# -------------------------------------------------------------------------
# TESTES: Validação de quantidade
# -------------------------------------------------------------------------

def test_serializer_com_quantidade_menor_ou_igual_a_zero_deve_falhar():
    """Deve acusar erro se a quantidade enviada for 0 ou negativa."""
    id_valido = str(ObjectId())
    
    # Testando com ZERO
    serializer_zero = CarrinhoSerializer(data={"produto_id": id_valido, "quantidade": 0})
    assert serializer_zero.is_valid() is False
    assert "A quantidade deve ser maior que zero." in str(serializer_zero.errors["quantidade"])

    # Testando com NEGATIVO
    serializer_negativo = CarrinhoSerializer(data={"produto_id": id_valido, "quantidade": -3})
    assert serializer_negativo.is_valid() is False
    assert "A quantidade deve ser maior que zero." in str(serializer_negativo.errors["quantidade"])


def test_serializer_com_quantidade_nao_inteira_deve_falhar():
    """Deve recusar strings de texto puro na quantidade."""
    id_valido = str(ObjectId())
    dados_entrada = {
        "produto_id": id_valido,
        "quantidade": "muitos"  # Força o ValueError
    }

    serializer = CarrinhoSerializer(data=dados_entrada)
    
    assert serializer.is_valid() is False
    assert "quantidade" in serializer.errors
    assert "A quantidade deve ser um número inteiro válido." in str(serializer.errors["quantidade"])
    
    
@pytest.mark.django_db
def test_finalizar_pedido_serializer_carrinho_vazio(cliente_db):
    # Setup: Cliente existe, mas NÃO tem carrinho no banco
    serializer = FinalizarPedidoSerializer(
        data={"forma_pagamento": "Pix"}, 
        context={'cliente_id': cliente_db.id}
    )
    
    # Isso vai disparar o ValueError (Linha vermelha)
    assert serializer.is_valid() is False
    assert "carrinho está vazio" in str(serializer.errors['non_field_errors'])

@pytest.mark.django_db
def test_finalizar_pedido_serializer_sucesso(cliente_db, produto_db):
    
    Carrinho.objects.create(
        Cliente_id=cliente_db.id,
        Itens=[{
            "Produto_id": produto_db.id,
            "Produto": "Arroz integral",  
            "Quantidade": 1,
            "Preco_unitario": "12.50",      
            "Subtotal": "12.50"             
        }]
    )
    
    serializer = FinalizarPedidoSerializer(
        data={"forma_pagamento": "Pix"}, 
        context={'cliente_id': cliente_db.id}
    )
    
    assert serializer.is_valid() is True
    assert 'carrinho_validado' in serializer.context
    
def test_serializer_forma_pagamento_vazia_deve_falhar():
    
    data = {"produto_id": "507f1f17bcf86cd799439011", "quantidade": 1, "forma_pagamento": ""}
    serializer = CarrinhoSerializer(data=data)
    
    assert serializer.is_valid() is False
    assert "obrigatório" in str(serializer.errors["forma_pagamento"])

def test_serializer_forma_pagamento_invalida_deve_falhar():
    
    data = {"produto_id": "507f1f17bcf86cd799439011", "quantidade": 1, "forma_pagamento": "Bitcoin"}
    serializer = CarrinhoSerializer(data=data)
    
    assert serializer.is_valid() is False
    assert "Forma de pagamento inválida" in str(serializer.errors["forma_pagamento"])

def test_serializer_forma_pagamento_sucesso():
   
    data = {"produto_id": "507f1f17bcf86cd799439011", "quantidade": 1, "forma_pagamento": "Pix"}
    serializer = CarrinhoSerializer(data=data)
    
    assert serializer.is_valid() is True
    assert serializer.validated_data["forma_pagamento"] == "Pix"
    
def test_serializer_produto_id_nulo_deve_falhar():
    """Força o campo a ser nulo/vazio para cobrir a linha do raise."""
    data = {"produto_id": "", "quantidade": 1}
    serializer = CarrinhoSerializer(data=data)
    
    # O serializer deve falhar e carregar o  ValueError
    assert serializer.is_valid() is False
    assert "produto_id" in serializer.errors
    assert "obrigatório" in str(serializer.errors["produto_id"])
    
def test_adicionar_ao_carrinho_serializer_invalido(client, auth_setup):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_setup['token']}")
    
    # Envia um dado que viola a regra do serializer (ex: quantidade negativa)
    payload = {"produto_id": "507f1f17bcf86cd799439011", "quantidade": -5}
    
    response = client.post("/api/adicionar_carrinho/", payload, format='json')
    
   
    assert response.status_code == 400