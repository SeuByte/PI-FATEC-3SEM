import pytest
from bson import ObjectId
from src.api.serializers.carrinho_serializer import CarrinhoSerializer


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