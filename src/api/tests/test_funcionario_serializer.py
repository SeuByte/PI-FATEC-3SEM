import pytest

from src.usuarios.models import FuncionarioModel
from src.api.serializers.funcionario_serializer import FuncionarioSerializer

# Sucesso

# Testes do serializer de Funcionário
@pytest.mark.django_db
class TestFuncionarioSerializer:

    # Verifica se o serializer retorna corretamente os dados do funcionário
    def test_should_serialize_funcionario(self):

        funcionario = FuncionarioModel.objects.create(
            nome_completo="João Silva",
            email="joao_serializer@email.com",
            telefone="11999999999",
            senha="123456",
            cargo="Analista",
        )

        serializer = FuncionarioSerializer(funcionario)

        assert serializer.data == {
            "id_funcionario": funcionario.id_funcionario,
            "nome_completo": "João Silva",
            "email": "joao_serializer@email.com",
            "telefone": "11999999999",
            "senha": "123456",
            "cargo": "Analista",
        }

    # Verifica se todos os campos esperados estão presentes
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

    # Verifica se um payload válido é aceito
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

    # Verifica se um email inválido é rejeitado
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

    # Verifica se emails duplicados são rejeitados
    def test_should_not_validate_duplicate_email(self):

        email = "joao_duplicado@email.com"

        FuncionarioModel.objects.create(
            nome_completo="João Silva",
            email=email,
            telefone="11999999999",
            senha="123456",
            cargo="Analista",
        )

        payload = {
            "nome_completo": "Maria Souza",
            "email": email,
            "telefone": "11888888888",
            "senha": "654321",
            "cargo": "Gerente",
        }

        serializer = FuncionarioSerializer(data=payload)

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    # Verifica se os campos obrigatórios são validados
    @pytest.mark.parametrize(
        "field",
        [
            "nome_completo",
            "email",
            "telefone",
            "senha",
            "cargo",
        ],
    )
    def test_should_not_validate_required_fields(self, field):

        payload = {
            "nome_completo": "Maria Souza",
            "email": "maria@email.com",
            "telefone": "11888888888",
            "senha": "123456",
            "cargo": "Gerente",
        }

        # Remove o campo que será testado
        payload.pop(field)

        serializer = FuncionarioSerializer(data=payload)

        assert not serializer.is_valid()
        assert field in serializer.errors
