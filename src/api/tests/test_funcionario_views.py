from rest_framework.test import APITestCase
from rest_framework import status

class CadastroFuncionarioViewTest(APITestCase):

    def test_cadastrar_funcionario_com_sucesso(self):
        payload = {
            "nome": "Pedro Benevides",
            "email": "pedro@email.com",
            "senha": "123456"
        }

        response = self.client.post(
            "/api/funcionarios/cadastro/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["mensagem"],
            "Funcionario Cadastra com sucesso!"
        )

    def test_cadastrar_funcionario_dados_invalidos(self):
        payload = {
            "nome": "",
            "email": "email_invalido",
            "senha": ""
        }

        response = self.client.post(
            "/api/funcionarios/cadastro/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)