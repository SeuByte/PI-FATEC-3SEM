from decimal import Decimal, ROUND_HALF_UP
from src.api.models import Carrinho, Produtos, ItemCarrinho
from bson import ObjectId, Decimal128  
from src.api.models import Pedidos  

class CarrinhoService:
    
    # Calculo pra transformar os valores em decimais de duas casas depois da virgula para o calculo ser exato.
    @staticmethod
    def calcular_financeiro(preco_unitario, quantidade):
        """Helper para padronizar o cálculo financeiro."""
        p_dec = Decimal(str(preco_unitario)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        q_dec = Decimal(str(quantidade))
        subtotal = p_dec * q_dec
        return p_dec, subtotal

    @staticmethod
    def adicionar_produto_carrinho(cliente_id, produto_id, quantidade):
        try:
            produto = Produtos.objects.get(id=ObjectId(produto_id))
        except Produtos.DoesNotExist:
            raise ValueError("Produto não encontrado.")
            
        carrinho = Carrinho.objects(Cliente_id=cliente_id).first()
        
        # Cálculo usando a lógica segura
        preco_unit, preco_total_item = CarrinhoService.calcular_financeiro(produto.Preco_100g, quantidade)

        if not carrinho:
            carrinho = Carrinho(
                Cliente_id=cliente_id,
                Itens=[]
            )

        # Procura se os itens dentro do carrinho já existem usando a propriedade do objeto
        item_existente = next((item for item in carrinho.Itens if item.Produto_id == produto.id), None)

        if item_existente:
            # Atualiza quantidade e recalcula o subtotal com precisão Decimal e tipagem de objeto
            nova_quantidade = item_existente.Quantidade + quantidade
            _, novo_subtotal = CarrinhoService.calcular_financeiro(produto.Preco_100g, nova_quantidade)
            
            item_existente.Quantidade = nova_quantidade
            item_existente.Subtotal = Decimal128(novo_subtotal)
        else:
            # Adiciona novo item garantindo que os valores sejam decimais estruturados no objeto correto
            novo_item = ItemCarrinho(
                Produto_id=produto.id,
                Produto=produto.Nome,
                Quantidade=quantidade,
                Preco_unitario=Decimal128(preco_unit), 
                Subtotal=Decimal128(preco_total_item)
            )
            carrinho.Itens.append(novo_item)
            
        carrinho.save()
        return carrinho
    
    @staticmethod
    def listar_itens_carrinho(cliente_id):
        carrinho = Carrinho.objects(Cliente_id = cliente_id).first()
        
        if not carrinho:
            return {
                "itens": [],
                "valor_total": "0.00" 
            }
            
        # 1. Soma matemática exata dos totais
        valor_total = sum(Decimal(str(item.Subtotal)) for item in carrinho.Itens)
        valor_total_formatado = Decimal(str(valor_total)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        # 2. Converte apenas para a exibição na API (mantendo no banco como número)
        itens_formatados = []
        for item in carrinho.Itens:
            p_unit_fmt = Decimal(str(item.Preco_unitario)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            subtotal_fmt = Decimal(str(item.Subtotal)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            itens_formatados.append({
                "Produto_id": str(item.Produto_id),
                "Produto": item.Produto,
                "Quantidade": item.Quantidade,
                "Preco_unitario": str(p_unit_fmt), # Exibe "5.20"
                "Subtotal": str(subtotal_fmt)      # Exibe "104.00"
            })
            
        return {
            "itens": itens_formatados,
            "valor_total": str(valor_total_formatado) 
        }
        
        
    @staticmethod
    def atualizar_quantidade(cliente_id, produto_id, nova_quantidade):
        carrinho = Carrinho.objects(Cliente_id=cliente_id).first()
        
        if not carrinho:
            raise ValueError("Carrinho não encontrado.")
            
        item = next((i for i in carrinho.Itens if str(i.Produto_id) == str(produto_id)), None)
        if not item:
            raise ValueError("Item não encontrado no carrinho.")

        if nova_quantidade <= 0:
            return CarrinhoService.deletar_itens_carrinho(cliente_id, produto_id)

        # Atualiza a quantidade e o subtotal
        item.Quantidade = nova_quantidade
        _, item.Subtotal = CarrinhoService.calcular_financeiro(item.Preco_unitario, nova_quantidade)
        
        carrinho.save()
        return carrinho    
        
        
    @staticmethod
    def deletar_itens_carrinho(cliente_id, produto_id):
        # Não precisamos verificar se o carrinho existe aqui, pois assumimos 
        # que o decorador de autenticação ou a View já garantiram o cliente_id.
        carrinho = Carrinho.objects(Cliente_id = cliente_id).first()
        # Converte o ID recebido na rota para o formato nativo do MongoDB
        obj_produto_id = ObjectId(produto_id)
        
        
        # Busca o item na memória. Usamos next() para parar a busca 
        # assim que encontrar o primeiro match, otimizando a iteração.
        item_existente = next((item for item in carrinho.Itens if item.Produto_id == obj_produto_id), None)
        if not item_existente:
            raise ValueError("Produto não encontrado no carrinho.")
        
        # O remove() atua direto na lista em memória (EmbeddedDocumentList)
        carrinho.Itens.remove(item_existente)
        carrinho.save()
        return carrinho
    
    @staticmethod
    # Transforma o carrinho atual em um pedido e limpa o carrinho do cliente.
    def finalizar_carrinho(cliente_id, forma_pagamento, carrinho):
        
        if not carrinho or not hasattr(carrinho, 'Itens') or len(carrinho.Itens) == 0:
            raise ValueError("Carrinho vazio")
        
        carrinho = Carrinho.objects(Cliente_id=cliente_id).first()
        
        #  soma o subtotal acessando via propriedade .Subtotal
        valor_total = sum((Decimal(str(Item.Subtotal)) for Item in carrinho.Itens), Decimal("0"))
        valor_total_formatado = valor_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        # Cria o documento na coleção de Pedidos
        novo_pedido = Pedidos(
            Cliente_id=str(cliente_id),
            Carrinho_id=ObjectId(str(carrinho.id)),
            Itens=carrinho.Itens,                # Copia a lista de itens do carrinho
            Valor_total=Decimal128(valor_total_formatado),    # Envelopado com Decimal128
            Forma_pagamento=forma_pagamento,     # Ex: "Pix", "Cartao"
            Status="Pendente"                    # Todo pedido nasce aguardando aprovação
        )
        novo_pedido.save()
        
        # Esvazia o carrinho original do banco para o cliente poder usar de novo
        carrinho.Itens = []
        carrinho.save()
        
        return novo_pedido