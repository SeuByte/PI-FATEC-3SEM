from rest_framework.decorators import api_view
from api.services.produtos_service import Produtos
from api.utils.response import success, error

@api_view(["GET"])
def listar_produtos(request):
    produtos = Produtos()

    try:

        data = produtos.listar()

        return success(data)
    except Exception as e:

        return error(message=str(e), status=500)
    
@api_view(["GET"])
def listar_produto_id(request, id):

    try:

        data = Produtos.listar_por_id(id)

        return success(data)

    except Exception as e:

        return error(
            message="Erro ao buscar produto",
            error=e,
            status_code=500
        )