from rest_framework.views import APIView
from rest_framework.response import Response
from src.usuarios.models import (
    RecuperarSenhaModel)
from rest_framework.decorators import api_view

from src.api.serializers.confirmar_recuperacao_serializer import (
    ConfirmarRecuperacaoSerializer
)

from src.api.services.recuperacao_senha_service import (
    RecuperarSenhaService
)

from src.api.utils.response import (
    success,
    error
)


@api_view(["POST"])
def confirmar_recuperacao(request):

    serializer = ConfirmarRecuperacaoSerializer(
        data=request.data
    )

    if serializer.is_valid():

        try:

            # Recupera os dados validados
            dados = serializer.validated_data

            # Chama a service corretamente
            RecuperarSenhaService.confirmar_recuperacao(
                email=dados["email"],
                token=dados["token"],
                nova_senha=dados["nova_senha"]
            )

            return success(
                message="Senha alterada com sucesso."
            )

        except ValueError as e:

            return error(
                message=str(e),
                status=400
            )

        except Exception:

            return error(
                message="Erro interno no servidor.",
                status=500
            )

    return error(
        message=serializer.errors,
        status=400
    )