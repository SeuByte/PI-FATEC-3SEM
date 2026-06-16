# src/api/tests/test_confirmar_recuperacao_serializer.py

import pytest

from src.api.serializers.confirmar_recuperacao_serializer import (
    ConfirmarRecuperacaoSerializer
)


@pytest.mark.django_db
class TestConfirmarRecuperacaoSerializer:

    # Deve validar um payload válido
    def test_should_validate_valid_payload(self):

        payload = {
            "email": "teste@email.com",
            "token": "123456",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "NovaSenha123"
        }

        serializer = ConfirmarRecuperacaoSerializer(
            data=payload
        )

        assert serializer.is_valid()
        assert serializer.errors == {}

    # Deve conter todos os campos esperados
    def test_should_contain_expected_fields(self):

        serializer = ConfirmarRecuperacaoSerializer()

        assert set(serializer.fields.keys()) == {
            "email",
            "token",
            "nova_senha",
            "confirmar_senha"
        }

    # Não deve validar email inválido
    def test_should_not_validate_invalid_email(self):

        payload = {
            "email": "email-invalido",
            "token": "123456",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "NovaSenha123"
        }

        serializer = ConfirmarRecuperacaoSerializer(
            data=payload
        )

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    # Não deve validar token vazio
    def test_should_not_validate_missing_token(self):

        payload = {
            "email": "teste@email.com",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "NovaSenha123"
        }

        serializer = ConfirmarRecuperacaoSerializer(
            data=payload
        )

        assert not serializer.is_valid()
        assert "token" in serializer.errors

    # Não deve validar quando as senhas forem diferentes
    def test_should_not_validate_different_passwords(self):

        payload = {
            "email": "teste@email.com",
            "token": "123456",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "OutraSenha123"
        }

        serializer = ConfirmarRecuperacaoSerializer(
            data=payload
        )

        assert not serializer.is_valid()

    # Não deve validar senha menor que 8 caracteres
    def test_should_not_validate_short_password(self):

        payload = {
            "email": "teste@email.com",
            "token": "123456",
            "nova_senha": "123456",
            "confirmar_senha": "123456"
        }

        serializer = ConfirmarRecuperacaoSerializer(
            data=payload
        )

        assert not serializer.is_valid()

    @pytest.mark.parametrize(
        "field",
        [
            "email",
            "token",
            "nova_senha",
            "confirmar_senha"
        ]
    )
    def test_should_not_validate_required_fields(
        self,
        field
    ):

        payload = {
            "email": "teste@email.com",
            "token": "123456",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "NovaSenha123"
        }

        payload.pop(field)

        serializer = ConfirmarRecuperacaoSerializer(
            data=payload
        )

        assert not serializer.is_valid()
        assert field in serializer.errors