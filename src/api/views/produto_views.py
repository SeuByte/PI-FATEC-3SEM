from rest_framework.decorators import api_view
from src.api.services.produto_service import ProdutosService
from src.api.utils.response import success, error
from src.api.serializers.produto_serializer import ProdutoSerializer
from src.core.models import Produtos




@api_view(["GET"])
def listar_produtos(request):
    try:
        produtos = ProdutosService.listar()
        data=[
            ProdutoSerializer(obj=p).to_representation()
            for p in produtos
        ]
        return success(data)
    
    except Exception as e:
        return error(message=str(e), status = 500)
    
@api_view(["GET"])
def listar_produto_id(request, id):

    try:
        produto = ProdutosService.listar_por_id(id)
    
        if not produto:
            return error(message="Produto não encontrado", status = 404)
        serializer = ProdutoSerializer(obj=produto)
        
        return success(serializer.to_representation())
    
    except Exception as e:
        return error(message=str(e), status = 500)
    
    
@api_view(["DELETE"])
def deletar_produto(request, id):
    try:
        produto = ProdutosService.deletar(id)
        
        if not produto:
            return error(message="Produto não encontrado.", status = 404)
        serializer = ProdutoSerializer(obj=produto)
        return success(message="Produto deletado com sucesso !", status = 200)
    

       
    except Exception as e:
        return error(message=str(e), status = 500)
    
    
@api_view(["PUT"])
def editar_produto(request, id):
    data = request.data
    try:
        produto = ProdutosService.atualizar(id, data)
        
        if not produto:
            return error(message="Produto não existe ou não pode ser editado.", status = 404)
        serializer = ProdutoSerializer( data=request.data, obj=produto)
        if not serializer.is_valid():
            return error(serializer.errors, status = 400)
        produto_atualizado = ProdutosService.atualizar(id, serializer.validated_data)
        return success(message="Produto editado com sucesso!", status= 200)
            
        
    except Exception as e:
        return error(message=str(e), status = 500)
    
    
    