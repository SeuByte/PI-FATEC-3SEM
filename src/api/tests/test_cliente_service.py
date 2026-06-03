import pytest
from django.contrib.auth.hashers import make_password
from src.api.services.cliente_service import ClienteService
from src.api.models import Clientes




class TestClienteService:
    def test_criar_cliente(self):
        dados = {
            "Nome": "Matheus",
            "Email": "matheus@email.com",
            "Senha": "123",
            "Telefone": "11999999999",
            "Data_nasc": "01/01/2000",
            "CPF": "12345678900",
            "CEP": "12345678",
            "Endereco": "Rua X",
            "Bairro": "Bairro Y",
            "Numero": 10,
            "Cidade": "Cidade Z",
            "Estado": "SP"
        }
        novo = ClienteService.criar_cliente(dados)
        assert novo.Nome == "Matheus"


    def test_listar_clientes_vazio(self):
        # Testa se listar clientes retorna uma lista vazia quando não há dados
        resultado = ClienteService.listar_cliente()
        assert resultado == []

    @pytest.mark.django_db
    def test_autenticar_sucesso(self):
        # Cria um cliente de teste com senha criptografada
        senha_original = "senha123"
        cliente = Clientes.objects.create(
            Email="teste@email.com",
            Senha=make_password(senha_original)
        )
        
        # Testa a autenticação
        resultado = ClienteService.autenticar("teste@email.com", senha_original)
        assert resultado.Email == cliente.Email

    @pytest.mark.django_db
    def test_autenticar_falha_senha(self):
        # Cria o cliente
        Clientes.objects.create(Email="teste@email.com", Senha=make_password("senha123"))
        
        # Tenta autenticar com senha errada
        with pytest.raises(ValueError, match="Email ou senha incorretos"):
            ClienteService.autenticar("teste@email.com", "senha_errada")

    @pytest.mark.django_db
    def test_criar_cliente(self):
        dados = {
            "Nome": "Matheus",
            "Email": "matheus@email.com",
            "Senha": "123" # Em um cenário real, você passaria o hash aqui
        }
        novo = ClienteService.criar_cliente(dados)
        
        assert Clientes.objects.count() == 1
        assert novo.Nome == "Matheus"