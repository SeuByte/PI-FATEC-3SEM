from rest_framework import status
import jwt

def test_acesso_negado_token_vazio(client, auth_setup):
    """Testa se o sistema rejeita um header 'Bearer ' vazio."""
    client.credentials(HTTP_AUTHORIZATION='Bearer ')
    response = client.get(auth_setup['url'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_acesso_negado_header_sem_prefixo_bearer(client, auth_setup):
    """Testa se o sistema rejeita quando o token é enviado sem a palavra 'Bearer'."""
    client.credentials(HTTP_AUTHORIZATION=f"{auth_setup['token']}")
    response = client.get(auth_setup['url'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_acesso_negado_token_modificado_no_payload(client, auth_setup):
    """Testa a integridade: alguém alterou o email dentro do token, a assinatura deve invalidar."""
    # O token é 'header.payload.signature'. Vamos alterar o payload.
    partes = auth_setup['token'].split('.')
    # payload hackeado: '{"email": "hackeado@teste.com"}' em base64
    payload_hackeado = "eyJlbWFpbCI6ICJoYWNrZWFkb0B0ZXN0ZS5jb20ifQ"
    token_corrompido = f"{partes[0]}.{payload_hackeado}.{partes[2]}"
    
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_corrompido}')
    response = client.get(auth_setup['url'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_acesso_negado_token_com_chave_diferente(client, auth_setup):
    """Testa se o sistema rejeita um token assinado por uma chave secreta diferente."""
    # Cria um token com uma chave secreta FALSA
    token_falso = jwt.encode({"email": "usuario@teste.com"}, "chave-secreta-errada", algorithm="HS256")
    
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_falso}')
    response = client.get(auth_setup['url'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED