from rest_framework.decorators import api_view
from rest_framework.response import Response
from src.api.serializers.cliente_serializer import ClienteSerializer
from src.api.services.cliente_service import ClienteService
from src.api.utils.response import success, error
from django.core.exceptions import ValidationError
from src.api.utils.auth_utils import gerar_token, token_required


@api_view(["GET"])
@token_required  # <--- O "porteiro" está aqui!
def pagina_protegida(request):
    print("--- ACESSANDO A VIEW PROTEGIDA ---")
    return Response({"message": "Você está logado e pode ver este dado secreto!"})





@api_view(["GET"])
def listar_clientes(request):
    try:
        data = ClienteService.listar_cliente()
        return success(data)
    except Exception as e:
        return error(message="Erro interno no servidor", status=500)

@api_view(["POST"])
def login_cliente(request):
    try:
        email = request.data.get('Email')
        senha = request.data.get('Senha')
        
        ClienteService.autenticar(email, senha)
       
        token = gerar_token(email)
        return success(message="Login efetuado com sucesso!", data={"token": token})

    except ValueError as e:
        # Aqui  captura o "Email ou senha incorretos" enviado pelo Service
        return error(message=str(e), status=400)

    except Exception as e:
        # Aqui  captura erros técnicos inesperados (500)
        return error(message="Erro interno no servidor.", status=500)

@api_view(["POST"])
def cadastrar_cliente(request):
    #Chama o serializer
    serializer = ClienteSerializer(data=request.data)
    #Caso o serializer valide todos os dados enviados com sucesso, segue o codigo
    if serializer.is_valid():
        try:
            #Chama o service para criar
            ClienteService.criar_cliente(serializer.validated_data)
            #Caso o construtor não dê nenhum problema, a view retorna sucesso
            return success(message="Cliente cadastrado com sucesso!", status=201)
        #Erros como email ou senha errados são registrados aqui
        except ValidationError as e:
            return error(message=str(e), status=400)
        #Erros que fogem do escopo do serializer são registrados aqui
        except Exception as e:
            return error(message="Erro interno do sistema.", status=500)
    #Qualquer campo que o usuário digitar não passar das regras de negocio, é registrado aqui
    return error(message=serializer.errors, status=400)
