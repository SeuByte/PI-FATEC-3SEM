from rest_framework.decorators import api_view
from src.api.services.carrinho_service import CarrinhoService
from src.api.serializers.carrinho_serializer import CarrinhoSerializer
from src.api.models import Clientes
from src.api.utils.auth_utils import token_required
from src.api.utils.response import success, error


@api_view(["POST"])
@token_required
def adicionar_ao_carrinho(request):
    serializer = CarrinhoSerializer(data=request.data)
    
    if serializer.is_valid():
        print(f"DEBUG: validated_data completo: {serializer.validated_data}")
        try:
            cliente = Clientes.objects.get(Email=request.user_email)
            CarrinhoService.adicionar_produto_carrinho(
                cliente_id=cliente.id,
                produto_id=serializer.validated_data['produto_id'],
                quantidade=serializer.validated_data['quantidade']
                )
            return success(message="Produto adicionado ao carrinho com sucesso !", status=201)
        except Clientes.DoesNotExist:
            return error(message="Cliente não encontrado.", stauts=404)
        except ValueError as e:
            #Captura erros de logica(ex: produto não encontrado)
            return error(message=str(e), status=400)
        except Exception as e:
            print(f"--- ERRO DETALHADO: {str(e)} ---")
            import traceback
            traceback.print_exc()
            #Erros fora do escopo da logica(ex: queda do banco de dados)
            return error(message=str(e), status=500)
    #Caso a validação do serializer encontre algum erro.
    return error(message=serializer.errors, status=400)