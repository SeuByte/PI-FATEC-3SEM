from rest_framework.decorators import api_view
from src.api.services.carrinho_service import CarrinhoService
from src.api.serializers.carrinho_serializer import CarrinhoSerializer
from src.api.models import Clientes
from src.api.utils.auth_utils import token_required
from src.api.utils.response import success, error
from rest_framework.response import Response
from bson.errors import InvalidId
import traceback

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
            return error(message="Cliente não encontrado.", status=404)
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


@api_view(["GET"])
@token_required
def listar_carrinho(request):
    try:
        email_cliente = request.user_email
        cliente = Clientes.objects(Email=email_cliente).first()
        if not cliente:
            return Response({"error": "Cliente não encontrado"}, status=404)
        resultado = CarrinhoService.listar_itens_carrinho(str(cliente.id))
        return Response(resultado, status=200)
    except Exception as e:
        return Response({"error": f"Erro ao listar carrinho: {str(e)}"}, status=500)
    

@api_view(["DELETE"])    
@token_required
def remover_item_carrinho(request):
    try:
        email_cliente = request.user_email
        cliente = Clientes.objects(Email=email_cliente).first()
        
        if not cliente:
            return Response({"error": "Cliente não encontrado"}, status=404)
        produto_id = request.data.get('produto_id')
        if not produto_id:
            return Response({'error': "O campo 'produto_id é obrigatorio no corpo da requisição"}, status=400)
        carrinho_atualizado = CarrinhoService.deletar_itens_carrinho(str(cliente.id), produto_id)
        return Response({"message": "Item removido com sucesso!"}, status=200)
    except ValueError as e:
        # Captura o "Produto não encontrado no carrinho" ou "Carrinho não encontrado" do Service
        return Response({"error": str(e)}, status=404)
    
    except InvalidId:
        return Response({"error": "O ID do produto enviado é invalido."}, status=400)
    except Exception as e:
        return Response({"error": f"Erro interno ao remover item: {str(e)}"}, status=500)
    
    
@api_view(["POST"])
@token_required
def finalizar_carrinho(request):
    try:
        email_cliente = request.user_email
        cliente = Clientes.objects(Email=email_cliente).first()
        
        if not cliente:
            return error(message="Cliente não encontrado.", status=404)
        
        forma_pagamento = request.data.get("forma_pagamento")
        if not forma_pagamento:
            return error(message="O campo 'forma_pagamento' é obrigatório", status=400)
        
        serializer = CarrinhoSerializer(data=request.data, context={'cliente_id': cliente.id})
        
        if serializer.is_valid():
            
        
            carrinho_validado = serializer.context.get('carrinho_validado')
            
            novo_pedido = CarrinhoService.finalizar_carrinho(
                cliente_id = cliente.id,
                forma_pagamento = forma_pagamento,
                carrinho = carrinho_validado
            )
            return success(message="Pedido finalizado com sucesso!", data={"pedido_id": str(novo_pedido.id), "status": novo_pedido.Status.value}, 
                status=201)
        else:
            return error(message=serializer.errors, status=400)
    except ValueError as e:
        return error(message=str(e), status=400)
    except Exception as e:
        print(f"--- ERRO DETALHADO NO FECHAMENTO: {str(e)} ---")
        traceback.print_exc()
        return error(message="Erro interno ao finalizar o carrinho", status=500)