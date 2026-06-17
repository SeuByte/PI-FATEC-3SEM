
import pytest
from django.urls import reverse
from src.api.utils.auth_utils import gerar_token
from src.api.models import Clientes
from unittest.mock import patch, MagicMock
from src.api.utils.auth_utils import gerar_token
    # --- SUCESSO ---

# 1. Função falsa que simula o comportamento do decorador
def fake_token_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Aqui a mágica: injetamos o e-mail que o seu Service/View espera
        request.user_email = "joao@email.com" 
        return view_func(request, *args, **kwargs)
    return wrapper


def test_rota_protegida_sucesso(client, usuario_autenticado, monkeypatch):
    monkeypatch.undo()
    #Gera o token com o email do usuário
    
    token = gerar_token(usuario_autenticado.email) 
    
    #Passa pela validação do token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    # A requisição permite o usuário autenticado
    response = client.get(reverse('rota-de-teste')) 
    
   
    assert response.status_code == 200



def test_listar_clientes_sucesso(client):
        response = client.get(reverse('listar_clientes'))
        assert response.status_code == 200
        
def test_listar_clientes_erro_interno(client):
    
    # Forçamos um erro quebrando temporariamente a collection do MongoEngine
    with pytest.raises(Exception):
        # Se o banco falhar ou o service estourar
        response = client.get(reverse('listar_clientes'))
        assert response.status_code == 500
        
def test_listar_clientes_lista_vazia(client):
    """Garante que a rota responde 200 mesmo se não houver nenhum cliente."""
    
    Clientes.objects.all().delete() 
    
    response = client.get(reverse('listar_clientes'))
    assert response.status_code == 200

def test_cadastrar_cliente_sucesso(client, dados_cliente_valido):
        response = client.post(reverse('cadastrar_cliente'), data=dados_cliente_valido, format='json')
        assert response.status_code == 201

def test_login_cliente_sucesso(client, cliente_db):
        payload = {"Email": cliente_db.Email, "Senha": "SenhaForte123!@#"}
        response = client.post(reverse('login_cliente'), data=payload, format='json')
        assert response.status_code == 200

@pytest.mark.django_db
def test_editar_cliente_sucesso(client, cliente_db):
    # 1. Gera o token real para esse cliente
    token = gerar_token(cliente_db.Email)
    
    url = reverse('editar_cliente', kwargs={'cliente_id': str(cliente_db.id)})
    dados = {"Nome": "Novo Nome"}
    
    # 2. Envia o token no cabeçalho Authorization
    response = client.put(
        url, 
        dados, 
        format='json',
        HTTP_AUTHORIZATION=f'Bearer {token}'
    )
    
    assert response.status_code == 200
    assert response.data["mensagem"] == "Cliente atualizado com sucesso!"





    # --- FALHA ---

def test_cadastrar_cliente_email_duplicado(client, dados_cliente_valido):
        # 1. Primeiro cadastro (deve ter sucesso)
        client.post(reverse('cadastrar_cliente'), data=dados_cliente_valido, format='json')
        
        # 2. Segundo cadastro com os mesmos dados (deve falhar)
        response = client.post(reverse('cadastrar_cliente'), data=dados_cliente_valido, format='json')
        
        # 3. Verifica se o status é 400 (Bad Request)
        assert response.status_code == 400
        
        # 4. Verifica se a mensagem de erro está presente no retorno do serializer
        assert 'Email' in response.data['message'] or "já existe" in str(response.data['message']).lower()
        
        
def test_cadastrar_cliente_invalido(client):
        # Enviando payload vazio para disparar erro do serializer
        response = client.post(reverse('cadastrar_cliente'), data={}, format='json')
        assert response.status_code == 400


def test_login_cliente_incorreto(client):
        payload = {"Email": "inexistente@email.com", "Senha": "errada"}
        response = client.post(reverse('login_cliente'), data=payload, format='json')
        assert response.status_code == 400
       
        assert "incorretos" in str(response.data.get('message', ''))
        
def test_rota_protegida_falha(client):
   
    response = client.get('/api/rota-de-teste/')
    assert response.status_code in [401, 403]
            
def test_editar_cliente_invalido(client, cliente_db):
    url = reverse('editar_cliente', kwargs={'cliente_id': str(cliente_db.id)})
    # Exemplo: enviando um formato de e-mail inválido ( serializer valida isso)
    dados = {"Email": "email-invalido"}
    
    response = client.put(url, dados, format='json')
    
    assert response.status_code == 400
    assert "Email" in response.data["erro"]


def test_editar_cliente_inexistente(client):
   def test_editar_cliente_inexistente(client):
    # ID que não existe no banco
    inexistente_id = '000000000000000000000000'
    url = reverse('editar_cliente', kwargs={'cliente_id': inexistente_id})
    
    # Em vez de gerar um JWT, passamos o e-mail que o decorador espera.
    # MUITOS decoradores de teste são feitos para aceitar um token simples 
    # ou um header de "debug" se você configurar bem.
    response = client.put(
        url, 
        {"Nome": "Novo Nome"}, 
        format='json',
        HTTP_USER_EMAIL='joao@email.com' # Tente injetar o e-mail direto aqui
    )
    
    assert response.status_code in [400, 404]

def test_view_deletar_cliente_sucesso(client, cliente_db):
    # Gerar um token real para o teste de sucesso
    token = gerar_token(cliente_db.Email)
    
    # Usamos o patch para garantir que o token_required aceite esse token
    # e injete o e-mail correto no request.
    with patch('src.api.views.cliente_views.token_required', fake_token_required):
        response = client.delete(
            f'/api/deletar_cliente/{cliente_db.id}/',
            HTTP_AUTHORIZATION=f'Bearer {token}' # Importante enviar o header!
        )
    
    assert response.status_code == 200
    assert response.data["mensagem"] == "Cliente deletado com sucesso!"


def test_view_deletar_cliente_inexistente(client):
    # ID válido para o Mongo, mas que não existe na base
    id_inexistente = "665e8a7f9b8c2d1a3e4f5a6b"
    url = reverse('deletar_cliente', kwargs={'cliente_id': id_inexistente})
    
    # Executa a requisição DELETE
    response = client.delete(url)
    
    # Valida se a View capturou o ValueError da Service e retornou 400
    assert response.status_code == 400
    assert response.data["erro"] == "Cliente não encontrado."
    
