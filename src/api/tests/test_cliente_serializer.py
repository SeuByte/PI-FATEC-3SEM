import pytest
from datetime import date
from unittest.mock import patch
from src.api.serializers.cliente_serializer import ClienteSerializer
from src.api.models import Clientes

# --- SENHA ---
def test_senha_curta_falha():
    s = ClienteSerializer()
    with pytest.raises(ValueError, match="8 digitos"): s.validate_Senha("123")

# --- CPF ---
def test_cpf_invalido_falha():
    s = ClienteSerializer()
    with pytest.raises(ValueError, match="O CPF deve conter exatamente 11 dígitos."): s.validate_CPF("123")

def test_serializer_cpf_valido():
    dados = {"CPF": "123.456.789-09"} # CPF matemático válido
    serializer = ClienteSerializer(data=dados)
    assert serializer.is_valid() is True
    assert serializer.validated_data["CPF"] == "12345678909"

def test_cpf_sucesso():
    dados = {"CPF": "123.456.789-09"} 
    serializer = ClienteSerializer(data=dados)

# --- NOME, ENDERECO, BAIRRO, NUMERO ---
def test_campos_obrigatorios_falha():
    #Chama o serializer
    s = ClienteSerializer()
    #Valida todos os possiveis erros
    with pytest.raises(ValueError, match="obrigatório"): s.validate_Nome("   ")
    with pytest.raises(ValueError, match="obrigatório"): s.validate_Endereco("")
    with pytest.raises(ValueError, match="obrigatório"): s.validate_Bairro(None)
    with pytest.raises(ValueError, match="obrigatório"): s.validate_Numero("  ")
    
def test_campos_obrigatorios_sucesso():
    s = ClienteSerializer()
    assert s.validate_Nome("Matheus") == "Matheus"
    assert s.validate_Endereco("Rua A") == "Rua A"

# --- EMAIL ---
def test_email_invalido_falha():
    s = ClienteSerializer()
    with pytest.raises(ValueError, match="@"): s.validate_Email("teste.com")
    
def test_email_duplicado_falha():
    dados_padrao = {
        "Nome": "Teste",
        "Email": "teste@teste.com",
        "CPF": "12345678900",
        "Senha": "senha",
        "Endereco": "Rua A",
        "Bairro": "Bairro",
        "Numero": "1",
        "CEP": "12345678",
        "Cidade": "Cidade",
        "Estado": "SP",
        "Telefone": "11999999999",
        "Data_nasc": "2000-01-01"
    }
    Clientes.objects.create(**dados_padrao)
    serializer = ClienteSerializer()
    with pytest.raises(ValueError, match="já existe"):
        serializer.validate_Email("teste@teste.com")

# --- CEP, CELULAR, TELEFONE ---
def test_contatos_invalido_falha():
    s = ClienteSerializer()
    
    with pytest.raises(ValueError, match="O celular deve conter 11 digitos"): s.validate_Celular("123")
    with pytest.raises(ValueError, match="O telefone deve conter 10 digitos"): s.validate_Telefone("123")

def test_validate_cep_com_sucesso():
    # Instancia o serializer
    s = ClienteSerializer()
    
    # Simula uma resposta de sucesso da API dos Correios
    mock_sucesso = {"cep": "01310-000", "logradouro": "Av Paulista"}
    
    # Patch intercepta o requests.get dentro do seu arquivo de serializer
    with patch('src.api.serializers.cliente_serializer.requests.get') as mock_request:
        mock_request.return_value.json.return_value = mock_sucesso
        
    
    resultado = s.validate_CEP("01310-000")
    assert resultado == "01310000"
def test_validate_cep_invalido_formato():
    s = ClienteSerializer()
    # Testa se dispara ValueError para CEP com tamanho errado
    with pytest.raises(ValueError, match="O CEP deve conter 8 dígitos"):
        s.validate_CEP("123")

def test_validate_cep_nao_encontrado_na_api():
    s = ClienteSerializer()
    # Simula uma resposta de erro da API (conforme a documentação do ViaCEP)
    mock_erro = {"erro": "true"}
    
    with patch('src.api.serializers.cliente_serializer.requests.get') as mock_request:
        mock_request.return_value.json.return_value = mock_erro
        
        with pytest.raises(ValueError, match="CEP não encontrado na base dos Correios."):
            s.validate_CEP("99999999")
    
def test_contatos_sucesso():
    s = ClienteSerializer()
    assert s.validate_Celular("(11)99999-9999") == "11999999999"
    assert s.validate_Telefone("1133334444") == "1133334444"

# --- DATA NASCIMENTO ---
def test_data_nasc_futura_falha():
    s = ClienteSerializer()
    with pytest.raises(ValueError, match="Formato de data inválido. Use DD/MM/AAAA ou AAAA-MM-DD."): 
        s.validate_Data_nasc("30/05/2099")
    
def test_data_nasc_invalida_falha():
    s = ClienteSerializer()
    with pytest.raises(ValueError, match="Formato"): s.validate_Data_nasc("abc-def")
    
def test_data_nasc_sucesso():
    s = ClienteSerializer()
    assert isinstance(s.validate_Data_nasc("30/05/2020"), date)
    assert isinstance(s.validate_Data_nasc(date(2000, 1, 1)), date)