import pytest
from src.api.models import Produtos
from src.api.serializers.produto_serializer import ProdutoSerializer
from decimal import Decimal
from bson.decimal128 import Decimal128


class TestProdutoSerializer:


    def test_to_representation_sucesso(self):   
        # 1. Cria um produto com valores específicos
        p = Produtos.objects.create(
            Nome="Monitor", 
            Estoque=10, 
            Unidade="UN", 
            Valor_venda=500.0, 
            Grupo="Eletrônicos", 
            Preco_100g=12.567
        )
        
        # 2. Atribui o objeto ao serializer
        self.s.obj = p
        
        # 3. Chama o método
        resultado = self.s.to_representation()
        
        # 4. Verifica se cada campo está formatado corretamente
        assert resultado["Nome"] == "Monitor"
        assert resultado["Estoque"] == 10
        assert resultado["Valor_venda"] == "500.00"  # Deve estar formatado
        assert resultado["Preco_100g"] == "12.57"    # Deve estar arredondado/formatado
        assert resultado["Grupo"] == "Eletrônicos"
        assert resultado["id"] == str(p.id)

    def setup_method(self):
        self.s = ProdutoSerializer()
        Produtos.objects.delete() # Limpa o banco antes de cada teste
        
        
        
    # --- TESTE DE SUCESSO ---
    def test_valor_venda_sucesso(self):
        # Captura o retorno do método
        resultado = self.s.validate_Valor_venda("150.50")
            
        # Valida se o tipo é Decimal e se o valor é o esperado
        assert isinstance(resultado, Decimal)
        assert resultado == Decimal("150.50")
        
        # Teste com valor inteiro para garantir que ele converte bem
        assert self.s.validate_Valor_venda(100) == Decimal("100.00")
        
    def test_preco_100g_sucesso(self):
        resultado = self.s.validate_Preco_100g("150.50")
            
        # Valida se o tipo é Decimal e se o valor é o esperado
        assert isinstance(resultado, Decimal)
        assert resultado == Decimal("150.50")
        
        # Teste com valor inteiro para garantir que ele converte bem
        assert self.s.validate_Preco_100g(100) == Decimal("100.00")
        
    def test_save_sucesso(self):
    # Usei Decimal128 para garantir que o MongoEngine aceite o valor
        p = Produtos.objects.create(
            Estoque=Decimal128("10.09"),
            Nome="Arroz integral",
            Unidade="KG",
            Valor_venda=Decimal128("500.00"),
            Grupo="Graos",
            Preco_100g=Decimal128("12.50")
        )
        
        self.s.obj = p
        self.s.save()
        
        
        produto_salvo = Produtos.objects(Nome="Arroz integral").first()
        assert produto_salvo is not None
        
        print(f"\nSUCESSO: Produto encontrado no banco: {produto_salvo.Nome}")
        
            
    def test_nome_sucesso(self):
        assert self.s.validate_Nome("Monitor") == "Monitor"
        
    def test_estoque_sucesso(self):
        assert self.s.validate_Estoque("50.50") == 50.50
     
    def test_campos_sucesso(self):
        assert self.s.validate_Grupo("Informatica") == "Informatica"
        assert self.s.validate_Unidade("KG") == "KG"
    
    # --- UPDATE (Lógica de exclusão do ID) ---
    def test_nome_duplicado_no_update_sucesso(self):
        p1 = Produtos.objects.create(Nome="Monitor", Estoque=1, Unidade="UN", Valor_venda=10, Grupo="G1", Preco_100g=1)
        # O serializer simula o obj sendo editado
        self.s.obj = p1
        # Não deve falhar ao manter o próprio nome
        assert self.s.validate_Nome("Monitor") == "Monitor"
    
    
    
    
    # --- TESTE DE FALHA ---    
    # --- NOME ---
    def test_nome_obrigatorio_e_tamanho_falha(self):
        with pytest.raises(ValueError, match="O nome é obrigatório"): self.s.validate_Nome("")
        with pytest.raises(ValueError, match="3 caracteres"): self.s.validate_Nome("Ab")
        with pytest.raises(ValueError, match="muito grande"): self.s.validate_Nome("a" * 101)

    def test_nome_duplicado_falha(self):
        Produtos.objects.create(Nome="Monitor", Estoque=1, Unidade="UN", Valor_venda=10, Grupo="G1", Preco_100g=1)
        with pytest.raises(ValueError, match="Já existe"): self.s.validate_Nome("Monitor")

    

    # --- ESTOQUE E PREÇOS ---
    def test_estoque_invalido_falha(self):
        with pytest.raises(ValueError, match="O produto deve conter estoque a cima de zero !"): self.s.validate_Estoque("")
        with pytest.raises(ValueError, match="O estoque deve conter um número decimal válido, exemplo: 50.00"): self.s.validate_Estoque("abc")
        with pytest.raises(ValueError, match="O estoque deve conter um número decimal válido, exemplo: 50.00"): self.s.validate_Estoque("-10")

    

    def test_valor_venda_invalido_falha(self):
        with pytest.raises(ValueError, match="O valor venda é necessario"): self.s.validate_Valor_venda("")
        with pytest.raises(ValueError, match= "O valor venda não pode ser negativo"): self.s.validate_Valor_venda("-5.90")
        with pytest.raises(ValueError, match = "O valor de venda deve ser um numero decimal válido"): self.s.validate_Valor_venda("abc")


    def test_preco_100g_invalido_falha(self):
        with pytest.raises(ValueError, match= "O preço de 100g é necessario."): self.s.validate_Preco_100g("")
        with pytest.raises(ValueError, match="O valor deve ser um numero decimal válido"): self.s.validate_Preco_100g("abc")
        with pytest.raises(ValueError, match="O preço de 100g não pode ser negativo !"): self.s.validate_Preco_100g("-5")

    # --- GRUPO E UNIDADE ---
    def test_campos_obrigatorios_simples(self):
        with pytest.raises(ValueError, match="grupo"): self.s.validate_Grupo("")
        with pytest.raises(ValueError, match="Unidade"): self.s.validate_Unidade("")

    # --- Objeto vazio --- 
    def test_save_sem_objeto_falha(self):
            # 1. Garante que self.s não tenha um 'obj'
            if hasattr(self.s, 'obj'):
                del self.s.obj
                
            # 2. Testa se o raise ocorre quando o save é chamado()
            with pytest.raises(ValueError, match="Nenhum objeto para salvar."):
                self.s.save()
    

    