from rest_framework import serializers


class ConfirmarRecuperacaoSerializer(
    serializers.Serializer
):

    email = serializers.EmailField(
        required=True
    )

    token = serializers.CharField(
        required=True
    )

    nova_senha = serializers.CharField(
        required=True
    )

    confirmar_senha = serializers.CharField(
        required=True
    )

    def validate(self, data):

        if (
            data["nova_senha"]
            !=
            data["confirmar_senha"]
        ):

            raise serializers.ValidationError(
                "As senhas não coincidem."
            )

        if len(data["nova_senha"]) < 8:

            raise serializers.ValidationError(
                "A senha deve ter pelo menos 8 caracteres."
            )

        return data