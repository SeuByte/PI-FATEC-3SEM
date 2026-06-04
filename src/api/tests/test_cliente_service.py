import pytest
from django.contrib.auth.hashers import make_password
from src.api.services.cliente_service import ClienteService
from src.api.models import Clientes

# Remova a classe e use funções soltas

def test_listar_clientes_vazio():
    resultado = ClienteService.listar_cliente()
    assert resultado == []

def test_autenticar_sucesso():
    senha_original = "senha123"
    cliente = Clientes.objects.create(
        Nome="Matheus",
        Email="teste@email.com",
        Senha=make_password(senha_original),
        Telefone="11999999999",
        Data_nasc="2000-01-01",
        CPF="12345678900",
        CEP="12345678",
        Endereco="Rua X",
        Bairro="Bairro Y",
        Numero="10",
        Cidade="Cidade Z",
        Estado="SP"
    )
    
    resultado = ClienteService.autenticar("teste@email.com", senha_original)
    assert resultado.Email == cliente.Email


def test_autenticar_senha_incorreta(cliente_db):
    
    # Tenta logar com uma senha errada
    resultado = ClienteService.autenticar(cliente_db.Email, "senha_errada_qualquer")
    assert resultado is None  # Retorna o erro que o service dispara.


def test_criar_cliente():
    dados = {
        "Nome": "Matheus",
        "Email": "matheus@email.com",
        "Senha": "123",
        "Telefone": "11999999999",
        "Data_nasc": "2000-01-01",
        "CPF": "12345678900",
        "CEP": "12345678",
        "Endereco": "Rua X",
        "Bairro": "Bairro Y",
        "Numero": "10",
        "Cidade": "Cidade Z",
        "Estado": "SP"
    }
    novo = ClienteService.criar_cliente(dados)
    assert Clientes.objects.count() == 1
    assert novo.Nome == "Matheus"