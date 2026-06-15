import pytest
from src.api.services.funcionario_service import FuncionarioService
from src.usuarios.models import FuncionarioModel

# Sucesso

@pytest.mark.django_db
def test_criar_funcionario_sucesso():

    dados = {
        "nome_completo": "Carlos Souza",
        "email": "carlos@email.com",
        "telefone": "11999999999",
        "senha": "123456",
        "cargo": "Administrador"
    }

    FuncionarioService.criar_funcionario(
        dados
    )

    funcionario = (
        FuncionarioModel.objects.get(
            email="carlos@email.com"
        )
    )

    assert funcionario.nome_completo == "Carlos Souza"


@pytest.mark.django_db
def test_listar_funcionarios_sucesso():

    FuncionarioModel.objects.create(
        nome_completo="Carlos Souza",
        email="carlos@email.com",
        telefone="11999999999",
        senha="123456",
        cargo="Administrador"
    )

    funcionarios = (
        FuncionarioService.listar_funcionarios()
    )

    assert len(funcionarios) == 1


@pytest.mark.django_db
def test_buscar_funcionario_sucesso():

    funcionario = (
        FuncionarioModel.objects.create(
            nome_completo="Carlos Souza",
            email="carlos@email.com",
            telefone="11999999999",
            senha="123456",
            cargo="Administrador"
        )
    )

    resultado = (
        FuncionarioService.buscar_funcionario(
            funcionario.id_funcionario
        )
    )

    assert resultado["nome_completo"] == "Carlos Souza"


@pytest.mark.django_db
def test_atualizar_funcionario_sucesso():

    funcionario = (
        FuncionarioModel.objects.create(
            nome_completo="Carlos Souza",
            email="carlos@email.com",
            telefone="11999999999",
            senha="123456",
            cargo="Administrador"
        )
    )

    FuncionarioService.atualizar_funcionario(
        funcionario.id_funcionario,
        {
            "cargo": "Gerente"
        }
    )

    funcionario.refresh_from_db()

    assert funcionario.cargo == "Gerente"
    
    # Verifica se um funcionário pode ser deletado
@pytest.mark.django_db
def test_deletar_funcionario_sucesso(funcionario_db):

    FuncionarioService.deletar_funcionario(
        funcionario_db.id_funcionario
    )

    assert (
        FuncionarioModel.objects.filter(
            id_funcionario=funcionario_db.id_funcionario
        ).exists()
        is False
    )

# Falhas

# Verifica se retorna erro ao tentar deletar funcionário inexistente
@pytest.mark.django_db
def test_deletar_funcionario_inexistente():

    with pytest.raises(ValueError):

        FuncionarioService.deletar_funcionario(
            999
        )
        
        