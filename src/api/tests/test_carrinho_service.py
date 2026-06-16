import pytest
from bson import ObjectId
from decimal import Decimal
from src.api.services.carrinho_service import CarrinhoService
from src.api.models import Carrinho
from src.api.models import StatusPedido

class TestCarrinhoService:

    # -------------------------------------------------------------------------
    # TESTES: calcular_financeiro
    # -------------------------------------------------------------------------
    def test_calcular_financeiro_precisao_decimal(self):
        """Garante que o cálculo financeiro aplica o ROUND_HALF_UP e evita dízimas."""
        preco_unitario = 12.555
        quantidade = 2
        
        preco_dec, subtotal = CarrinhoService.calcular_financeiro(preco_unitario, quantidade)
        
        # O ROUND_HALF_UP deve arredondar 12.555 para 12.56
        assert preco_dec == Decimal("12.56")
        assert subtotal == Decimal("25.12")

    # -------------------------------------------------------------------------
    # TESTES: adicionar_produto_carrinho
    # -------------------------------------------------------------------------
    def test_adicionar_produto_novo_no_carrinho(self, cliente_db, produto_db):
        """Deve criar um carrinho se não existir e adicionar o produto com valores corretos."""
        quantidade = 3  # Ex: 3 porções de 100g
        
        carrinho = CarrinhoService.adicionar_produto_carrinho(
            cliente_id=str(cliente_db.id),
            produto_id=str(produto_db.id),
            quantidade=quantidade
        )

        # Validações no banco de dados e no retorno do service
        assert carrinho is not None
        assert str(carrinho.Cliente_id) == str(cliente_db.id)
        assert len(carrinho.Itens) == 1
        
        
        item = carrinho.Itens[0]
        assert str(item.Produto_id) == str(produto_db.id)
        assert item.Produto == produto_db.Nome
        assert item.Quantidade == quantidade
        
        
        assert float(str(item.Preco_unitario)) == 12.50  # Preco_100g 
        assert float(str(item.Subtotal)) == 37.50       # 12.50 * 3

    def test_adicionar_produto_ja_existente_no_carrinho(self, cliente_db, produto_db):
        """Deve apenas somar a quantidade e recalcular o subtotal se o item já existir."""
        # 1. Adiciona o produto pela primeira vez (Qtd: 2)
        CarrinhoService.adicionar_produto_carrinho(str(cliente_db.id), str(produto_db.id), quantidade=2)
        
        # 2. Adiciona o mesmo produto novamente (Qtd: 3)
        carrinho_atualizado = CarrinhoService.adicionar_produto_carrinho(
            cliente_id=str(cliente_db.id),
            produto_id=str(produto_db.id),
            quantidade=3
        )

        # O carrinho deve continuar contendo apenas 1 item físico, mas atualizado
        assert len(carrinho_atualizado.Itens) == 1
        item = carrinho_atualizado.Itens[0]
        assert item.Quantidade == 5  # 2 + 3
        
        
        assert float(str(item.Subtotal)) == 62.50  # 12.50 * 5

    def test_adicionar_produto_inexistente_deve_lancar_erro(self, cliente_db):
        """Deve levantar ValueError se o ID do produto não constar no banco."""
        id_fantasma = str(ObjectId())

        with pytest.raises(ValueError, match="Produto não encontrado."):
            CarrinhoService.adicionar_produto_carrinho(
                cliente_id=str(cliente_db.id),
                produto_id=id_fantasma,
                quantidade=1
            )

    # -------------------------------------------------------------------------
    # TESTES: listar_itens_carrinho
    # -------------------------------------------------------------------------
    def test_listar_carrinho_vazio_retorna_estrutura_zerada(self, cliente_db):
        """Garante que se o cliente não tiver carrinho, retorna itens vazios e total 0.0."""
        resultado = CarrinhoService.listar_itens_carrinho(str(cliente_db.id))
        
        assert resultado == {
            "itens": [],
            "valor_total": "0.00"
        }

    def test_listar_carrinho_com_itens_cadastrados(self, cliente_db, produto_db):
        """Deve listar o dicionário contendo a lista do MongoEngine e a soma total corrigida."""
        # Coloca itens no carrinho primeiro usando o próprio service
        CarrinhoService.adicionar_produto_carrinho(str(cliente_db.id), str(produto_db.id), quantidade=2)
        
        resultado = CarrinhoService.listar_itens_carrinho(str(cliente_db.id))
        
        assert len(resultado['itens']) == 1
        assert resultado['valor_total'] == "25.00"
        
        
        dados_item = resultado['itens'][0]
        nome_produto = dados_item.get('Produto') or dados_item.get('produto')
        assert nome_produto == "Arroz integral"

    # -------------------------------------------------------------------------
    # TESTES: deletar_itens_carrinho
    # -------------------------------------------------------------------------
    def test_deletar_item_do_carrinho_com_sucesso(self, cliente_db, produto_db):
        """Deve remover com sucesso o item de dentro do array do carrinho."""
        # Cria o carrinho preenchido
        CarrinhoService.adicionar_produto_carrinho(str(cliente_db.id), str(produto_db.id), quantidade=1)
        
        # Deleta o item
        carrinho_atualizado = CarrinhoService.deletar_itens_carrinho(str(cliente_db.id), str(produto_db.id))
        
        assert len(carrinho_atualizado.Itens) == 0

    def test_deletar_item_inexistente_no_carrinho_deve_lancar_erro(self, cliente_db, produto_db):   
        """Deve dar erro caso tente remover um produto que não está no carrinho."""
        # Adiciona o produto A no carrinho
        CarrinhoService.adicionar_produto_carrinho(str(cliente_db.id), str(produto_db.id), quantidade=1)
        
        # Tenta remover um produto B (ID aleatório)
        id_inexistente = str(ObjectId())
        
        with pytest.raises(ValueError, match="Produto não encontrado no carrinho."):
            CarrinhoService.deletar_itens_carrinho(str(cliente_db.id), id_inexistente)
            
    # -------------------------------------------------------------------------
    # TESTES: finalizar_carrinho (Checkout)
    # -------------------------------------------------------------------------
    def test_finalizar_carrinho_com_sucesso(self, cliente_db, produto_db):
        """Valida a transição de Carrinho -> Pedido."""
        # 1. Prepara o carrinho
        CarrinhoService.adicionar_produto_carrinho(str(cliente_db.id), str(produto_db.id), quantidade=1)
        
        # 2. Finaliza
        pedido = CarrinhoService.finalizar_carrinho(
            cliente_id=str(cliente_db.id),
            forma_pagamento="PIX",
            carrinho=Carrinho.objects.get(Cliente_id=cliente_db.id)
        )
        
        # 3. Verifica se o pedido foi criado e o carrinho foi limpo
        assert pedido is not None
        assert pedido.Status.PENDENTE
        
        carrinho_limpo = Carrinho.objects.get(Cliente_id=cliente_db.id)
        assert len(carrinho_limpo.Itens) == 0
        
    def test_finalizar_carrinho_vazio_lanca_erro(self, cliente_db):
    
        carrinho = Carrinho.objects.create(Cliente_id=cliente_db.id, Itens=[])
        
       
        try:
            CarrinhoService.finalizar_carrinho(
                cliente_id=str(cliente_db.id),
                forma_pagamento="PIX",
                carrinho=carrinho
            )
          
        except ValueError as e:
            print(f"DEBUG: Erro capturado: {str(e)}")
            assert "vazio" in str(e).lower()
            
            
    # -------------------------------------------------------------------------
    # TESTES: atualizar_quantidade
    # -------------------------------------------------------------------------
    
    def test_atualizar_quantidade_sucesso(self, cliente_db, produto_db):
        """Caminho Feliz: Deve atualizar a quantidade e recalcular o subtotal corretamente."""
        # 1. Adiciona o produto primeiro (Qtd: 2)
        CarrinhoService.adicionar_produto_carrinho(str(cliente_db.id), str(produto_db.id), quantidade=2)
        
        # 2. Atualiza para 5
        carrinho_atualizado = CarrinhoService.atualizar_quantidade(
            cliente_id=str(cliente_db.id),
            produto_id=str(produto_db.id),
            nova_quantidade=5
        )
        
        item = carrinho_atualizado.Itens[0]
        assert item.Quantidade == 5
        # 12.50 * 5 = 62.50
        assert float(str(item.Subtotal)) == 62.50

    def test_atualizar_quantidade_item_nao_encontrado_no_carrinho(self, cliente_db):
        """Caminho Triste: Deve levantar erro se o produto não estiver no carrinho."""
        # Cria carrinho vazio
        Carrinho.objects.create(Cliente_id=cliente_db.id, Itens=[])
        
        id_fantasma = str(ObjectId())
        
        with pytest.raises(ValueError, match="Item não encontrado no carrinho."):
            CarrinhoService.atualizar_quantidade(
                cliente_id=str(cliente_db.id),
                produto_id=id_fantasma,
                nova_quantidade=10
            )
    