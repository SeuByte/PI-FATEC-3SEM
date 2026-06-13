from rest_framework.decorators import api_view

from src.api.services.recuperacao_senha_service import (
    RecuperarSenhaService
)

from src.api.utils.response import (
    success,
    error
)


@api_view(["POST"])
def recuperar_senha(request):

    try:

        email = request.data.get(
            "email"
        )

        RecuperarSenhaService.gerar_token(
            email
        )

        return success(
            message="Token enviado para o email."
        )

    except ValueError as e:

        return error(
            message=str(e),
            status=404
        )

    except Exception:

        return error(
            message="Erro interno no servidor.",
            status=500
        )