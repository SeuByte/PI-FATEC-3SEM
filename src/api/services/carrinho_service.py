from decimal import Decimal, ROUND_HALF_UP
from src.api.models import Carrinho, Produtos
from bson import ObjectId
import json
class CarrinhoService:
    
    #Calculo pra transformar os valores, em decimais de duas casas depois da virgula para o calculo ser exato.
    @staticmethod
    def calcular_financeiro(preco_unitario, quantidade):
        """Helper para padronizar o cálculo financeiro."""
        p_dec = Decimal(str(preco_unitario)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        q_dec = Decimal(str(quantidade))
        subtotal = p_dec * q_dec
        return p_dec, subtotal

    @staticmethod
    def adicionar_produto_carrinho(cliente_id, produto_id, quantidade):
        #Evita erros inesperados.
        try:
            produto = Produtos.objects.get(id=ObjectId(produto_id))
        except Produtos.DoesNotExist:
            # print(f"DEBUG: O produto com ID {produto_id} não foi achado no banco.")
            raise ValueError("Produto não encontrado.")
            
        carrinho = Carrinho.objects(Cliente_id=cliente_id).first()
        
        # Cálculo usando a lógica segura
        preco_unit, preco_total_item = CarrinhoService.calcular_financeiro(produto.Preco_100g, quantidade)

        if not carrinho:
            carrinho = Carrinho(
                Cliente_id=cliente_id,
                Itens=[]
            )

        # Procura se os itens dentro do carrinho já existem
        item_existente = next((item for item in carrinho.Itens if item['produto_id'] == produto.id), None)

        if item_existente:
            # Atualiza quantidade e recalcula o subtotal com precisão Decimal
            nova_quantidade = item_existente['quantidade'] + quantidade
            _, novo_subtotal = CarrinhoService.calcular_financeiro(produto.Preco_100g, nova_quantidade)
            
            item_existente['quantidade'] = nova_quantidade
            item_existente['subtotal'] = float(novo_subtotal) 
        else:
            # Adiciona novo item garantindo que os valores sejam decimais/formatados
            novo_item = {
                "produto_id": produto.id,
                "produto": produto.Nome,
                "quantidade": quantidade,
                "preco_unitario": float(preco_unit),
                "subtotal": float(preco_total_item)
            }
            carrinho.Itens.append(novo_item)
            
        carrinho.save()
        
        return carrinho
    
    
    @staticmethod
    def listar_itens_carrinho(cliente_id):
        carrinho = Carrinho.objects(Cliente_id = cliente_id).first()
        
        #Evita erros quando o cliente abre a lista do carrinho e não tem nada.
        if not carrinho:
            return{
                "itens": [],
                "valor_total": 0.0
            }
        carrinho_json_string = carrinho.to_json()
        carrinho_dados = json.loads(carrinho_json_string)
        valor_total = sum(item['subtotal'] for item in carrinho.Itens)
        return{
            "itens": carrinho_dados.get('Itens', []),
            "valor_total": float(Decimal(str(valor_total)).quantize(Decimal("0.01"), rounding = ROUND_HALF_UP))
        }
        
    @staticmethod
    def deletar_itens_carrinho(cliente_id, produto_id):
        carrinho = Carrinho.objects(Cliente_id = cliente_id).first()
        obj_produto_id = ObjectId(produto_id)
        item_existente = next((item for item in carrinho.Itens if item['produto_id'] == obj_produto_id), None)
        if not item_existente:
            raise ValueError("Produto não encontrado no carrinho.")
        
        carrinho.Itens.remove(item_existente)
        carrinho.save()
        return carrinho
        
    