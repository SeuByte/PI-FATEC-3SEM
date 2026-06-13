import pytest
from django.urls import reverse

from src.usuarios.models import FuncionarioModel


@pytest.mark.django_db
class TestFuncionarioViews:

    # -------------------
    # CADASTRAR
    # -------------------
    def test_cadastrar_sucesso(self, client):

        payload = {
            "nome_completo": "Carlos",
            "email": "carlos@email.com",
            "telefone": "11999999999",
            "senha": "123456",
            "cargo": "Dev"
        }

        response = client.post(
            reverse("cadastro_funcionario"),
            data=payload,
            content_type="application/json"
        )

        assert response.status_code == 201
        assert response.json()["message"] == "Funcionário cadastrado com sucesso!"


    # -------------------
    # LISTAR
    # -------------------
    def test_listar_sucesso(self, client):

        FuncionarioModel.objects.create(
            nome_completo="Carlos",
            email="carlos@email.com",
            telefone="11999999999",
            senha="123456",
            cargo="Dev"
        )

        response = client.get(reverse("listar_funcionarios"))

        assert response.status_code == 200


    # -------------------
    # BUSCAR SUCESSO
    # -------------------
    def test_buscar_sucesso(self, client):

        funcionario = FuncionarioModel.objects.create(
            nome_completo="Carlos",
            email="carlos@email.com",
            telefone="11999999999",
            senha="123456",
            cargo="Dev"
        )

        response = client.get(
            reverse(
                "buscar_funcionario",
                kwargs={"id_funcionario": funcionario.id_funcionario}
            )
        )

        assert response.status_code == 200


    # -------------------
    # BUSCAR INEXISTENTE
    # -------------------
    def test_buscar_inexistente(self, client):

        response = client.get(
            reverse(
                "buscar_funcionario",
                kwargs={"id_funcionario": 999}
            )
        )

        assert response.status_code == 404


    # -------------------
    # ATUALIZAR SUCESSO
    # -------------------
    def test_atualizar_sucesso(self, client):

        funcionario = FuncionarioModel.objects.create(
            nome_completo="Carlos",
            email="carlos@email.com",
            telefone="11999999999",
            senha="123456",
            cargo="Dev"
        )

        response = client.put(
            reverse(
                "atualizar_funcionario",
                kwargs={"id_funcionario": funcionario.id_funcionario}
            ),
            data={"cargo": "Gerente"},
            content_type="application/json"
        )

        assert response.status_code == 200

        funcionario.refresh_from_db()
        assert funcionario.cargo == "Gerente"


    # -------------------
    # ATUALIZAR INEXISTENTE
    # -------------------
    def test_atualizar_inexistente(self, client):

        response = client.put(
            reverse(
                "atualizar_funcionario",
                kwargs={"id_funcionario": 999}
            ),
            data={"cargo": "Gerente"},
            content_type="application/json"
        )

        assert response.status_code == 404