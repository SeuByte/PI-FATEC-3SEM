import pytest
from src.api.serializers.recuperacao_senha_serializer import RecuperarSenhaSerializer



@pytest.mark.django_db
class TestRecuperarSenhaSerializer:

    # Deve validar um payload válido
    def test_should_validate_valid_payload(self):

        payload = {
            "email": "teste@email.com"
        }

        serializer = RecuperarSenhaSerializer(
            data=payload
        )

        assert serializer.is_valid()
        assert serializer.errors == {}

    # Deve conter apenas o campo email
    def test_should_contain_expected_fields(self):

        serializer = RecuperarSenhaSerializer()

        assert set(serializer.fields.keys()) == {
            "email"
        }

    # Não deve validar email inválido
    def test_should_not_validate_invalid_email(self):

        payload = {
            "email": "email-invalido"
        }

        serializer = RecuperarSenhaSerializer(
            data=payload
        )

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    # Não deve validar quando email não for enviado
    def test_should_not_validate_missing_email(self):

        payload = {}

        serializer = RecuperarSenhaSerializer(
            data=payload
        )

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    # Não deve validar email vazio
    def test_should_not_validate_empty_email(self):

        payload = {
            "email": ""
        }

        serializer = RecuperarSenhaSerializer(
            data=payload
        )

        assert not serializer.is_valid()
        assert "email" in serializer.errors