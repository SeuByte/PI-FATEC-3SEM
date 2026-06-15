
from django.urls import reverse
from src.api.utils.auth_utils import gerar_token
from src.api.models import Clientes

    # --- SUCESSO ---

def test_rota_protegida_sucesso(client, usuario_autenticado):
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

def test_cadastrar_cliente_sucesso(client, dados_cliente_valido):
        response = client.post(reverse('cadastrar_cliente'), data=dados_cliente_valido, format='json')
        assert response.status_code == 201

def test_login_cliente_sucesso(client, cliente_db):
        payload = {"Email": cliente_db.Email, "Senha": "SenhaForte123!@#"}
        response = client.post(reverse('login_cliente'), data=payload, format='json')
        assert response.status_code == 200

def test_editar_cliente_sucesso(client, cliente_db):
    url = reverse('editar-cliente', kwargs={'cliente_id': str(cliente_db.id)})
    dados = {"Nome": "Nome Alterado"}
    
    response = client.put(url, dados, format='json')
    
    assert response.status_code == 200
    assert response.data["mensagem"] == "Cliente atualizado com sucesso!"
    
    # Verifica se salvou no banco
    cliente_db.reload()
    assert cliente_db.Nome == "Nome Alterado"





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
    url = reverse('editar-cliente', kwargs={'cliente_id': str(cliente_db.id)})
    # Exemplo: enviando um formato de e-mail inválido ( serializer valida isso)
    dados = {"Email": "email-invalido"}
    
    response = client.put(url, dados, format='json')
    
    assert response.status_code == 400
    assert "Email" in response.data["erro"]

def test_editar_cliente_inexistente(client):
    url = reverse('editar-cliente', kwargs={'cliente_id': '665e8a7f9b8c2d1a3e4f5a6b'})
    dados = {"Nome": "Inexistente"}
    
    response = client.put(url, dados, format='json')
    
    assert response.status_code == 400
    assert response.data["erro"] == "Cliente não encontrado."

def test_view_deletar_cliente_sucesso(client, cliente_db):
    # Monta a URL com o ID do cliente existente
    url = reverse('deletar_cliente', kwargs={'cliente_id': str(cliente_db.id)})
    
    # Executa a requisição DELETE
    response = client.delete(url)
    
    # Validações da resposta da View
    assert response.status_code == 200
    assert response.data["mensagem"] == "Cliente deletado com sucesso!"
    
    # Garante que o cliente foi de fato removido do banco
    assert Clientes.objects.filter(id=cliente_db.id).count() == 0


def test_view_deletar_cliente_inexistente(client):
    # ID válido para o Mongo, mas que não existe na base
    id_inexistente = "665e8a7f9b8c2d1a3e4f5a6b"
    url = reverse('deletar_cliente', kwargs={'cliente_id': id_inexistente})
    
    # Executa a requisição DELETE
    response = client.delete(url)
    
    # Valida se a View capturou o ValueError da Service e retornou 400
    assert response.status_code == 400
    assert response.data["erro"] == "Cliente não encontrado."