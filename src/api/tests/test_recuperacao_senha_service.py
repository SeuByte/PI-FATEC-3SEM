import pytest
from datetime import date

from api.models import Clientes
from api.services.recuperacao_senha_service import RecuperarSenhaService


@pytest.mark.django_db
def test_gerar_token_sucesso():

    Clientes(
        Nome="Cliente Teste",
        Email="teste@email.com",
        Senha="123456",
        Telefone="11999999999",
        Data_nasc=date(2000, 1, 1),
        CPF="12345678901",
        CEP="13600000",
        Endereco="Rua Teste",
        Bairro="Centro",
        Numero=123,
        Cidade="Araras",
        Estado="SP"
    ).save()

    token = RecuperarSenhaService.gerar_token(
        "teste@email.com"
    )

    assert token is not None


@pytest.mark.django_db
def test_token_deve_ter_seis_digitos():

    Clientes(
        Nome="Cliente Teste",
        Email="teste@email.com",
        Senha="123456",
        Telefone="11999999999",
        Data_nasc=date(2000, 1, 1),
        CPF="12345678901",
        CEP="13600000",
        Endereco="Rua Teste",
        Bairro="Centro",
        Numero=123,
        Cidade="Araras",
        Estado="SP"
    ).save()

    token = RecuperarSenhaService.gerar_token(
        "teste@email.com"
    )

    assert len(token) == 6
    assert token.isdigit()