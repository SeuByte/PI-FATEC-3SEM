from src.core.models import Produtos
from decimal import Decimal


class ProdutosService:
    
    @staticmethod
    def listar():
        return Produtos.objects()
    
    @staticmethod
    def listar_por_id(id):
        return Produtos.objects(id=id).first()
    
    @staticmethod
    def criar(data):
        
            produto = Produtos(**data)
            produto.save()
            return produto
        

    @staticmethod
    def atualizar(id, data):
        produto = Produtos.objects.get(id=id)

        for campo, valor in data.items():
            if campo in ["Valor_venda", "Estoque", "Preco_100g"]:
                valor = Decimal(str(valor))

            setattr(produto, campo, valor)

        produto.save()
        return produto


    @staticmethod
    def deletar(id):
        produto = Produtos.objects(id=id).first()
        
        if not produto:
            return False
        
        produto.delete()
        return True