from src.api.models import Produtos
from src.api.serializers.produto_serializer import ProdutoSerializer
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
        produto = Produtos.objects(id=id).first()
        if not produto:
            return {"status": "erro", "message": "Produto não encontrado", "code": 404}
        
        serializer = ProdutoSerializer(data=data)
        serializer.obj = produto 
        
        if not serializer.is_valid():
            return {"status": "erro", "message": serializer.errors, "code": 400}
        
        validated_data = serializer.validated_data 
        
        produto.Nome = validated_data.get('Nome', produto.Nome)
        produto.Estoque = validated_data.get('Estoque', produto.Estoque)
        produto.Unidade = validated_data.get('Unidade', produto.Unidade)
        produto.Valor_venda = validated_data.get('Valor_venda', produto.Valor_venda)
        produto.Grupo = validated_data.get('Grupo', produto.Grupo)
        produto.Preco_100g = validated_data.get('Preco_100g', produto.Preco_100g)
        
        produto.save()
        
        return {"status": "sucesso", "message": "Produto editado com sucesso!"}


    @staticmethod
    def deletar(id):
        produto = Produtos.objects(id=id).first()
        
        if not produto:
            return False
        
        produto.delete()
        return True