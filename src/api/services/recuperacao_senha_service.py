import random
from django.conf import settings
from django.core.mail import send_mail
from src.api.models import Clientes
from src.usuarios.models import (
    RecuperarSenhaModel
)


class RecuperarSenhaService:

    @staticmethod
    def gerar_token(email):

        cliente = (
            Clientes.objects(
                Email=email
            ).first()
        )

        if not cliente:

            raise ValueError(
                "Cliente não encontrado"
            )

        token = str(
            random.randint(
                100000,
                999999
            )
        )

        RecuperarSenhaModel.objects.create(
            email=email,
            token=token
        )

        send_mail(
            subject='Recuperação de Senha',
            message=f''' Seu código é: {token} Caso não tenha solicitado, verifique sua conta. ''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        return token


    @staticmethod
    def confirmar_recuperacao(
        email,
        token,
        nova_senha
    ):

        registro = (
            RecuperarSenhaModel.objects.filter(
                email=email,
                token=token,
                utilizado=False
            ).first()
        )

        if not registro:

            raise ValueError(
                "Token inválido"
            )

        cliente = (
            Clientes.objects(
                Email=email
            ).first()
        )

        if not cliente:

            raise ValueError(
                "Cliente não encontrado"
            )

        cliente.Senha = nova_senha

        cliente.save()

        registro.utilizado = True

        registro.save()