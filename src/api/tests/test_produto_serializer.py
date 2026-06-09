import pytest
from datetime import date
from src.api.models import Produtos
from src.api.serializers.produto_serializer import ProdutoSerializer
from decimal import Decimal
from bson.decimal128 import Decimal128

# --- TESTE DE SUCESSO ---

def test_to_representation_sucesso():
    # 1. Cria um produto com valores específicos
    p = Produtos.objects.create(
        Nome="Monitor", 
        Estoque=10, 
        Unidade="UN", 
        Valor_venda=500.0, 
        Grupo="Eletrônicos", 
        Preco_100g=12.567
    )
    s = ProdutoSerializer()
    s.obj = p
    
    # 3. Chama o método
    resultado = s.to_representation()
    
    # 4. Verifica se cada campo está formatado corretamente
    assert resultado["Nome"] == "Monitor"
    assert resultado["Estoque"] == 10
    assert resultado["Valor_venda"] == "500.00"
    assert resultado["Preco_100g"] == "12.57"
    assert resultado["Grupo"] == "Eletrônicos"
    assert resultado["id"] == str(p.id)

def test_valor_venda_sucesso():
    s = ProdutoSerializer()
    resultado = s.validate_Valor_venda("150.50")
    assert isinstance(resultado, Decimal)
    assert resultado == Decimal("150.50")
    assert s.validate_Valor_venda(100) == Decimal("100.00")
    
def test_preco_100g_sucesso():
    s = ProdutoSerializer()
    resultado = s.validate_Preco_100g("150.50")
    assert isinstance(resultado, Decimal)
    assert resultado == Decimal("150.50")
    assert s.validate_Preco_100g(100) == Decimal("100.00")
    
def test_save_sucesso():
    s = ProdutoSerializer()
    Produtos.objects.delete()
    p = Produtos.objects.create(
        Estoque=Decimal128("10.09"),
        Nome="Arroz integral",
        Unidade="KG",
        Valor_venda=Decimal128("500.00"),
        Grupo="Graos",
        Preco_100g=Decimal128("12.50")
    )
    s.obj = p
    s.save()
    
    produto_salvo = Produtos.objects(Nome="Arroz integral").first()
    assert produto_salvo is not None
            
def test_nome_sucesso():
    s = ProdutoSerializer()
    assert s.validate_Nome("Monitor") == "Monitor"
    
def test_estoque_sucesso():
    s = ProdutoSerializer()
    assert s.validate_Estoque("50.50") == 50.50

def test_campos_sucesso():
    s = ProdutoSerializer()
    assert s.validate_Grupo("Informatica") == "Informatica"
    assert s.validate_Unidade("KG") == "KG"

# --- UPDATE ---
def test_nome_duplicado_no_update_sucesso():
    s = ProdutoSerializer()
    p1 = Produtos.objects.create(Nome="Monitor", Estoque=1, Unidade="UN", Valor_venda=10, Grupo="G1", Preco_100g=1)
    s.obj = p1
    assert s.validate_Nome("Monitor") == "Monitor"

# --- TESTE DE FALHA ---
def test_nome_obrigatorio_e_tamanho_falha():
    s = ProdutoSerializer()
    with pytest.raises(ValueError, match="O nome é obrigatório"): s.validate_Nome("")
    with pytest.raises(ValueError, match="3 caracteres"): s.validate_Nome("Ab")
    with pytest.raises(ValueError, match="muito grande"): s.validate_Nome("a" * 101)

def test_nome_duplicado_falha():
    s = ProdutoSerializer()
    Produtos.objects.create(Nome="Monitor", Estoque=1, Unidade="UN", Valor_venda=10, Grupo="G1", Preco_100g=1)
    with pytest.raises(ValueError, match="Já existe"): s.validate_Nome("Monitor")

def test_estoque_invalido_falha():
    s = ProdutoSerializer()
    with pytest.raises(ValueError, match="O produto deve conter estoque a cima de zero !"): s.validate_Estoque("")
    with pytest.raises(ValueError, match="O estoque deve conter um número decimal válido"): s.validate_Estoque("abc")
    with pytest.raises(ValueError, match="O estoque deve conter um número decimal válido"): s.validate_Estoque("-10")

def test_valor_venda_invalido_falha():
    s = ProdutoSerializer()
    with pytest.raises(ValueError, match="O valor venda é necessario"): s.validate_Valor_venda("")
    with pytest.raises(ValueError, match="O valor venda não pode ser negativo"): s.validate_Valor_venda("-5.90")
    with pytest.raises(ValueError, match="O valor de venda deve ser um numero decimal válido"): s.validate_Valor_venda("abc")

def test_preco_100g_invalido_falha():
    s = ProdutoSerializer()
    with pytest.raises(ValueError, match="O preço de 100g é necessario."): s.validate_Preco_100g("")
    with pytest.raises(ValueError, match="O valor deve ser um numero decimal válido"): s.validate_Preco_100g("abc")
    with pytest.raises(ValueError, match="O preço de 100g não pode ser negativo !"): s.validate_Preco_100g("-5")

def test_campos_obrigatorios_simples():
    s = ProdutoSerializer()
    with pytest.raises(ValueError, match="grupo"): s.validate_Grupo("")
    with pytest.raises(ValueError, match="Unidade"): s.validate_Unidade("")

def test_save_sem_objeto_falha():
    s = ProdutoSerializer()
    if hasattr(s, 'obj'):
        del s.obj
    with pytest.raises(ValueError, match="Nenhum objeto para salvar."):
        s.save()