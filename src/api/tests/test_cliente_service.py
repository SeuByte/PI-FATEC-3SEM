import pytest
from src.api.services.cliente_service import ClienteService
from src.api.models import Clientes
from django.contrib.auth.hashers import check_password

def test_listar_clientes_vazio():
    resultado = ClienteService.listar_cliente()
    assert resultado == []


def test_autenticar_caminho_feliz(cliente_db):

   
    email = cliente_db.Email
    senha = "senha_correta_definida_na_fixture" 
    
    resultado = ClienteService.autenticar(email, senha)
    
    assert resultado is not None
    assert resultado.Email == email
    assert resultado.id == cliente_db.id

def test_autenticar_email_nao_existente():
   
    email_fantasma = "inexistente@email.com"
    senha = "qualquer_senha"
    
    with pytest.raises(ValueError, match="Email ou senha incorretos"):
        ClienteService.autenticar(email_fantasma, senha)


def test_autenticar_senha_incorreta(cliente_db):
    with pytest.raises(ValueError, match="Email ou senha incorretos"):
        ClienteService.autenticar(cliente_db.Email, "senha_errada_qualquer")

def test_criar_cliente(dados_cliente_valido):
    
    novo = ClienteService.criar_cliente(dados_cliente_valido)
    
    assert Clientes.objects.count() == 1
    assert novo.Nome == dados_cliente_valido["Nome"]
    assert novo.Email == dados_cliente_valido["Email"]


def test_deletar_cliente_com_sucesso(cliente_db):
    # Passa o ID do cliente da fixture para a função
    resultado = ClienteService.deletar_cliente(cliente_db.id)
    
    assert resultado is True
    # Garante que o cliente realmente sumiu do banco de dados
    assert Clientes.objects.filter(id=cliente_db.id).count() == 0


def test_deletar_cliente_nao_encontrado():
    # Passa um ID válido para o ObjectId, mas que não existe no banco
    id_inexistente = "65f1a2b3c4d5e6f7a8b9c0d1" 
    
    with pytest.raises(ValueError, match="Cliente não encontrado."):
        ClienteService.deletar_cliente(id_inexistente)


def test_deletar_cliente_erro_id_invalido():
    # Testa o bloco genérico de Exception passando um ID num formato totalmente inválido
    id_invalido = "id-completamente-errado"
    
    # O ObjectId vai falhar ao tentar converter, caindo no Exception geral
    with pytest.raises(ValueError, match="Erro ao tentar deletar:"):
        ClienteService.deletar_cliente(id_invalido)
        


def test_editar_cliente_caminho_feliz(cliente_db):
    
    novos_dados = {
        "Nome": "Novo Nome Atualizado",
        "Senha": "nova_senha_segura_123"
    }
    
    # Executa a edição
    cliente_atualizado = ClienteService.editar_cliente(cliente_db.id, novos_dados)
    
    # Verifica dados simples
    assert cliente_atualizado.Nome == "Novo Nome Atualizado"
    
    # Verifica se a senha foi hasheada (o hash deve ser diferente da string original)
    assert check_password("nova_senha_segura_123", cliente_atualizado.Senha) is True
    assert cliente_atualizado.Senha != "nova_senha_segura_123"

def test_editar_cliente_nao_encontrado():
    
    id_inexistente = "65f1a2b3c4d5e6f7a8b9c0d1" 
    novos_dados = {"Nome": "Nome que não vai salvar"}
    
    with pytest.raises(ValueError, match="Cliente não encontrado."):
        ClienteService.editar_cliente(id_inexistente, novos_dados)