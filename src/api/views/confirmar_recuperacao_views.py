from rest_framework.views import APIView
from rest_framework.response import Response

from src.usuarios.models import (
    RecuperarSenhaModel
)

from src.api.models import (
    Clientes
)

from src.api.serializers.confirmar_recuperacao_serializer import (
    ConfirmarRecuperacaoSerializer
)


class ConfirmarRecuperacaoView(APIView):

    def post(self, request):

        serializer = ConfirmarRecuperacaoSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data[
            "email"
        ]

        token = serializer.validated_data[
            "token"
        ]

        nova_senha = serializer.validated_data[
            "nova_senha"
        ]

        registro = (
            RecuperarSenhaModel.objects.filter(
                email=email,
                token=token,
                utilizado=False
            ).first()
        )

        if not registro:

            return Response({"erro": "Token inválido"}, status=400)

        cliente = (
            Clientes.objects(
                Email=email
            ).first()
        )

        if not cliente:

            return Response({"erro": "Cliente não encontrado"}, status=404)

        cliente.Senha = nova_senha

        cliente.save()

        registro.utilizado = True

        registro.save()

        return Response({"mensagem": "Senha alterada com sucesso"})