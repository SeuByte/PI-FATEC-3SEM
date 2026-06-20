import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_recuperar_senha_sucesso(
    client,
    cliente_db
):

    response = client.post(
        reverse("recuperar_senha"),
        {
            "email": cliente_db.Email
        },
        format="json"
    )

    assert response.status_code == 200

    assert response.data["success"] is True

    assert (
        response.data["message"]
        ==
        "Token enviado para o email."
    )


@pytest.mark.django_db
def test_recuperar_senha_cliente_inexistente(
    client
):

    response = client.post(
        reverse("recuperar_senha"),
        {
            "email": "naoexiste@email.com"
        },
        format="json"
    )

    assert response.status_code == 404

    assert response.data["success"] is False

    assert (
        response.data["message"]
        ==
        "Cliente não encontrado"
    )