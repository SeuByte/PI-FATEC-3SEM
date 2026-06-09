from src.api.models import Carrinho, Produtos
from bson import ObjectId



class CarrinhoService:
    
    @staticmethod
    def adicionar_produto_carrinho(cliente_id, produto_id, quantidade):
        try:
         produto = Produtos.objects.get(id=ObjectId(produto_id))
        except Produtos.DoesNotExist:
            print(f"DEBUG: O produto com ID {produto_id} não foi achado no banco.")
            raise ValueError("Produto não encontrado.")
        carrinho = Carrinho.objects(Cliente_id=cliente_id).first()
        
        preco_unitario = produto.Preco_100g
        preco_total_item = preco_unitario * quantidade

        if not carrinho:
            carrinho = Carrinho(
                Cliente_id=cliente_id,
                Itens=[]
                )

        #procura se os itens dentro do carrinho já existem ou ainda não
        item_existente = next((item for item in carrinho.Itens if item['produto_id'] == produto.id), None)

        #caso o cliente adicione o mesmo item, ele apenas junta
        if item_existente:
            item_existente['quantidade'] += quantidade
            item_existente['subtotal'] = item_existente['quantidade'] * produto.Preco_100g
        #Caso não exista, ele adiciona o novo item ao carrinho.
        else:
            novo_item = {
                "produto_id": produto.id,
                "quantidade": quantidade,
                "preco_unitario": preco_unitario,
                "subtotal": preco_total_item
            }
            carrinho.Itens.append(novo_item)
            
        carrinho.save()
        
        return carrinho