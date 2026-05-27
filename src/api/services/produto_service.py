from src.core.models import Produtos


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
      pass


    @staticmethod
    def deletar(id):
        produto = Produtos.objects(id=id).first()
        
        if not produto:
            return False
        
        produto.delete()
        return True