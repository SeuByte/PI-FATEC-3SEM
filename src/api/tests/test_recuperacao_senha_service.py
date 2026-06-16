import pytest
from src.api.services.recuperacao_senha_service import RecuperarSenhaService
from src.usuarios.models import RecuperarSenhaModel

# Sucesso
@pytest.mark.django_db
def test_gerar_token_sucesso():

    email = "teste@email.com"

    token = RecuperarSenhaService.gerar_token(
        email
    )

    registro = (
        RecuperarSenhaModel.objects.filter(
            email=email,
            token=token
        ).first()
    )

    assert registro is not None
    assert registro.email == email
    assert registro.token == token


@pytest.mark.django_db
def test_token_deve_ter_seis_digitos():

    token = RecuperarSenhaService.gerar_token(
        "teste@email.com"
    )

    assert len(token) == 6
    assert token.isdigit()