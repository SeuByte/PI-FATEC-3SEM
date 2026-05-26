from rest_framework.decorators import api_view
from src.api.services.produto_service import ProdutosService
from src.api.utils.response import success, error
from src.api.serializers.produto_serializer import ProdutoSerializer




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
        return error(message=str(e), status=500)
    
@api_view(["GET"])
def listar_produto_id(request, id):

    try:
        produto = ProdutosService.listar_por_id(id)
    
        if not produto:
            return error(message="Produto não encontrado", status_code = 404)
        serializer = ProdutoSerializer(obj=produto)
        
        return success(serializer.to_representation())
    
    except Exception as e:
        return error(message=str(e), status_code=500)