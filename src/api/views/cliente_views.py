from rest_framework.decorators import api_view
from src.api.serializers.cliente_serializer import ClienteSerializer
from src.api.services.cliente_service import ClienteService
from src.api.utils.response import success, error

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
        
        return success(message="Login efetuado com sucesso!")

    except ValueError as e:
        # Aqui  captura o "Email ou senha incorretos" enviado pelo Service
        return error(message=str(e), status=400)

    except Exception as e:
        # Aqui  captura erros técnicos inesperados (500)
        return error(message="Erro interno no servidor.", status=500)

@api_view(["POST"])
def cadastrar_cliente(request):
    try:
        #Aplica as regras de negocio nos dados recebidos pelo cliente 
        serializer = ClienteSerializer(data=request.data)
        #Caso de erro ele não segue o codigo
        if serializer.is_valid():
            #Chama o service para criar
            ClienteService.criar_cliente(serializer.validated_data)
            return success(message="Cliente cadastrado com sucesso!", status=201)
        return error(message=serializer.errors, status=400)
    except Exception as e:
        return error(message="Erro interno no servidor.", status=500)