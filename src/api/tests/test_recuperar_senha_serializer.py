import pytest
from src.api.serializers.recuperacao_senha_serializer import (
    RecuperarSenhaSerializer
)


@pytest.mark.django_db
class TestRecuperarSenhaSerializer:

    def test_should_validate_valid_payload(self):

        payload = {
            "email": "teste@email.com",
            "token": "123456",
            "nova_senha": "Senha1234",
            "confirmar_senha": "Senha1234"
        }

        serializer = RecuperarSenhaSerializer(
            data=payload
        )

        assert serializer.is_valid()
        assert serializer.errors == {}

    def test_should_contain_expected_fields(self):

        serializer = RecuperarSenhaSerializer()

        assert set(serializer.fields.keys()) == {
            "email",
            "token",
            "nova_senha",
            "confirmar_senha"
        }

    def test_should_not_validate_invalid_email(self):

        payload = {
            "email": "email-invalido",
            "token": "123456",
            "nova_senha": "Senha1234",
            "confirmar_senha": "Senha1234"
        }

        serializer = RecuperarSenhaSerializer(
            data=payload
        )

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_should_not_validate_missing_email(self):

        payload = {
            "token": "123456",
            "nova_senha": "Senha1234",
            "confirmar_senha": "Senha1234"
        }

        serializer = RecuperarSenhaSerializer(
            data=payload
        )

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_should_not_validate_different_passwords(self):

        payload = {
            "email": "teste@email.com",
            "token": "123456",
            "nova_senha": "Senha1234",
            "confirmar_senha": "Senha5678"
        }

        serializer = RecuperarSenhaSerializer(
            data=payload
        )

        assert not serializer.is_valid()

    def test_should_not_validate_short_password(self):

        payload = {
            "email": "teste@email.com",
            "token": "123456",
            "nova_senha": "1234567",
            "confirmar_senha": "1234567"
        }

        serializer = RecuperarSenhaSerializer(
            data=payload
        )

        assert not serializer.is_valid()