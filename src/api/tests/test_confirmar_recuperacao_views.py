import pytest
from django.urls import reverse

from src.usuarios.models import (
    RecuperarSenhaModel
)


# Sucesso
@pytest.mark.django_db
def test_confirmar_recuperacao_sucesso(
    client,
    cliente_db
):

    RecuperarSenhaModel.objects.create(
        email=cliente_db.Email,
        token="123456"
    )

    response = client.post(
        reverse("confirmar_recuperacao"),
        {
            "email": cliente_db.Email,
            "token": "123456",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "NovaSenha123"
        },
        format="json"
    )

    assert response.status_code == 200


# Token inválido
@pytest.mark.django_db
def test_confirmar_recuperacao_token_invalido(
    client,
    cliente_db
):

    response = client.post(
        reverse("confirmar_recuperacao"),
        {
            "email": cliente_db.Email,
            "token": "999999",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "NovaSenha123"
        },
        format="json"
    )

    assert response.status_code == 400


# Cliente inexistente
@pytest.mark.django_db
def test_confirmar_recuperacao_cliente_inexistente(
    client
):

    RecuperarSenhaModel.objects.create(
        email="teste@email.com",
        token="123456"
    )

    response = client.post(
        reverse("confirmar_recuperacao"),
        {
            "email": "teste@email.com",
            "token": "123456",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "NovaSenha123"
        },
        format="json"
    )

    assert response.status_code == 400


# Token já utilizado
@pytest.mark.django_db
def test_confirmar_recuperacao_token_utilizado(
    client,
    cliente_db
):

    RecuperarSenhaModel.objects.create(
        email=cliente_db.Email,
        token="123456",
        utilizado=True
    )

    response = client.post(
        reverse("confirmar_recuperacao"),
        {
            "email": cliente_db.Email,
            "token": "123456",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "NovaSenha123"
        },
        format="json"
    )

    assert response.status_code == 400