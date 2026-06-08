import pytest
from usuarios.models import FuncionarioModel
from usuarios.serializers import FuncionarioSerializer


@pytest.mark.django_db
def test_funcionario_serializer_create():
    data = {
        "nome_completo": "Pedro Souza",
        "email": "pedro@email.com",
        "telefone": "11999999999",
        "senha": "123456",
        "cargo": "dev"
    }

    serializer = FuncionarioSerializer(data=data)

    assert serializer.is_valid() is True

    funcionario = serializer.save()

    assert funcionario.id_funcionario is not None
    assert funcionario.nome_completo == "Pedro Souza"
    assert funcionario.email == "pedro@email.com"
    assert funcionario.telefone == "11999999999"
    assert funcionario.senha == "123456"
    assert funcionario.cargo == "dev"