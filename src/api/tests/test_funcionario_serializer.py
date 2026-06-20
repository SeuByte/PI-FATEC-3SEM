from src.api.serializers.recuperacao_senha_serializer import RecuperarSenhaSerializer



class TestRecuperarSenhaSerializer:

 def test_should_validate_valid_payload(self):

    print("ARQUIVO NOVO CARREGADO")

    payload = {
        "email": "teste@email.com",
        "token": "123456",
        "nova_senha": "Senha1234",
        "confirmar_senha": "Senha1234"
    }

    serializer = RecuperarSenhaSerializer(data=payload)

    assert serializer.is_valid(), serializer.errors

    def test_should_contain_expected_fields(self):

        serializer = RecuperarSenhaSerializer()

        assert set(serializer.fields.keys()) == {
            "email",
            "token",
            "nova_senha",
            "confirmar_senha"
        }