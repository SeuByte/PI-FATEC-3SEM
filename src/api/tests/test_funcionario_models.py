import pytest
from src.usuarios.models import FuncionarioModel, RecuperarSenhaModel

# Sucesso

@pytest.mark.django_db
class TestFuncionarioModels:

    def test_funcionario_str(self):

        funcionario = FuncionarioModel.objects.create(
            nome_completo="João Silva",
            email="joao@email.com",
            telefone="11999999999",
            senha="123456",
            cargo="Analista"
        )

        assert str(funcionario) == "João Silva"

    def test_recuperar_senha_str(self):

        token = RecuperarSenhaModel.objects.create(
            email="teste@email.com",
            token="123456"
        )

        assert str(token) == "teste@email.com"