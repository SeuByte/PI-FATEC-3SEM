import pytest
from src.api.services.cliente_service import ClienteService
from src.api.models import Clientes

def test_listar_clientes_vazio():
    resultado = ClienteService.listar_cliente()
    assert resultado == []



def test_autenticar_senha_incorreta(cliente_db):
    with pytest.raises(ValueError, match="Email ou senha incorretos"):
        ClienteService.autenticar(cliente_db.Email, "senha_errada_qualquer")

def test_criar_cliente(dados_cliente_valido):
    #
    novo = ClienteService.criar_cliente(dados_cliente_valido)
    
    assert Clientes.objects.count() == 1
    assert novo.Nome == dados_cliente_valido["Nome"]
    assert novo.Email == dados_cliente_valido["Email"]