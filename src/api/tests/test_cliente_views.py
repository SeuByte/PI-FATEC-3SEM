
from django.urls import reverse


    # --- SUCESSO ---

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

    # --- FALHA ---

def test_cadastrar_cliente_email_duplicado(client, dados_cliente_valido):
        # 1. Primeiro cadastro (deve ter sucesso)
        client.post(reverse('cadastrar_cliente'), data=dados_cliente_valido, format='json')
        
        # 2. Segundo cadastro com os mesmos dados (deve falhar)
        response = client.post(reverse('cadastrar_cliente'), data=dados_cliente_valido, format='json')
        
        # 3. Verifica se o status é 400 (Bad Request)
        assert response.status_code == 400
        
        # 4. Verifica se a mensagem de erro está presente no retorno do serializer
        # O DRF retorna um dicionário de erros
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