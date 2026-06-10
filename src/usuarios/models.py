from django.db import models


class FuncionarioModel(models.Model):

    id_funcionario = models.AutoField(
        primary_key=True
    )

    nome_completo = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        unique=True
    )

    telefone = models.CharField(
        max_length=20
    )

    senha = models.CharField(
        max_length=255
    )

    cargo = models.CharField(
        max_length=100
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nome_completo


class RecuperarSenhaModel(models.Model):

    email = models.EmailField()

    token = models.CharField(
        max_length=6
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    utilizado = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.email