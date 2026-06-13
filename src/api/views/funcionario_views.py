from rest_framework.decorators import api_view
from src.api.serializers.funcionario_serializer import FuncionarioSerializer
from src.api.services.funcionario_service import FuncionarioService
from src.api.utils.response import success, error



@api_view(["POST"])
def cadastrar_funcionario(request):

    # Valida os dados recebidos
    serializer = FuncionarioSerializer(
        data=request.data
    )

    # Se os dados forem válidos
    if serializer.is_valid():

        try:

            # Chama a service para criar o funcionário
            FuncionarioService.criar_funcionario(
                serializer.validated_data
            )

            return success(
                message="Funcionário cadastrado com sucesso!",
                status=201
            )

        # Captura erros inesperados
        except Exception:

            return error(
                message="Erro interno do sistema.",
                status=500
            )

    # Retorna erros do serializer
    return error(
        message=serializer.errors,
        status=400
    )


@api_view(["GET"])
def listar_funcionarios(request):

    try:

        # Busca todos os funcionários
        data = (
            FuncionarioService.listar_funcionarios()
        )

        return success(data=data)

    # Captura erros inesperados
    except Exception:

        return error(
            message="Erro interno no servidor",
            status=500
        )


@api_view(["GET"])
def buscar_funcionario(
    request,
    id_funcionario
):

    try:

        # Busca funcionário pelo ID
        data = (
            FuncionarioService.buscar_funcionario(
                id_funcionario
            )
        )

        return success(data=data)

    # Funcionário não encontrado
    except ValueError as e:

        return error(
            message=str(e),
            status=404
        )

    # Captura erros inesperados
    except Exception:

        return error(
            message="Erro interno no servidor",
            status=500
        )


@api_view(["PUT"])
def atualizar_funcionario(
    request,
    id_funcionario
):

    # Permite atualizar apenas os campos enviados
    serializer = FuncionarioSerializer(
        data=request.data,
        partial=True
    )

    # Valida os dados recebidos
    if serializer.is_valid():

        try:

            # Chama a service para atualizar o funcionário
            FuncionarioService.atualizar_funcionario(
                id_funcionario,
                serializer.validated_data
            )

            return success(
                message="Funcionário atualizado com sucesso!"
            )

        # Funcionário não encontrado
        except ValueError as e:

            return error(
                message=str(e),
                status=404
            )

        # Captura erros inesperados
        except Exception:

            return error(
                message="Erro interno no servidor",
                status=500
            )

    # Retorna erros do serializer
    return error(
        message=serializer.errors,
        status=400
    )