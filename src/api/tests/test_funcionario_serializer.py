import pytest

from src.usuarios.models import FuncionarioModel
from src.api.serializers.funcionario_serializer import FuncionarioSerializer


@pytest.mark.django_db
class TestFuncionarioSerializer:

    def test_should_serialize_funcionario(self):
        funcionario = FuncionarioModel.objects.create(
            nome_completo="João Silva",
            email="joao@email.com",
            telefone="11999999999",
            senha="123456",
            cargo="Analista"
        )

        serializer = FuncionarioSerializer(funcionario)

        assert serializer.data == {
            "id_funcionario": funcionario.id_funcionario,
            "nome_completo": "João Silva",
            "email": "joao@email.com",
            "telefone": "11999999999",
            "senha": "123456",
            "cargo": "Analista",
        }

    def test_should_contain_expected_fields(self):
        serializer = FuncionarioSerializer()

        assert set(serializer.fields.keys()) == {
            "id_funcionario",
            "nome_completo",
            "email",
            "telefone",
            "senha",
            "cargo",
        }

    def test_should_validate_valid_payload(self):
        payload = {
            "nome_completo": "Maria Souza",
            "email": "maria@email.com",
            "telefone": "11888888888",
            "senha": "123456",
            "cargo": "Gerente",
        }

        serializer = FuncionarioSerializer(data=payload)

        assert serializer.is_valid()
        assert serializer.errors == {}

    def test_should_not_validate_invalid_email(self):
        payload = {
            "nome_completo": "Maria Souza",
            "email": "email-invalido",
            "telefone": "11888888888",
            "senha": "123456",
            "cargo": "Gerente",
        }

        serializer = FuncionarioSerializer(data=payload)

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_should_not_validate_duplicate_email(self):
        FuncionarioModel.objects.create(
            nome_completo="João Silva",
            email="joao@email.com",
            telefone="11999999999",
            senha="123456",
            cargo="Analista"
        )

        payload = {
            "nome_completo": "Maria Souza",
            "email": "joao@email.com",
            "telefone": "11888888888",
            "senha": "654321",
            "cargo": "Gerente",
        }

        serializer = FuncionarioSerializer(data=payload)

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    @pytest.mark.parametrize(
        "field",
        [
            "nome_completo",
            "email",
            "telefone",
            "senha",
            "cargo",
        ]
    )
    def test_should_not_validate_required_fields(self, field):
        payload = {
            "nome_completo": "Maria Souza",
            "email": "maria@email.com",
            "telefone": "11888888888",
            "senha": "123456",
            "cargo": "Gerente",
        }

        payload.pop(field)

        serializer = FuncionarioSerializer(data=payload)

        assert not serializer.is_valid()
        assert field in serializer.errors