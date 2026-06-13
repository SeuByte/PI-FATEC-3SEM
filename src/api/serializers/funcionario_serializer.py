from rest_framework import serializers
from src.usuarios.models import FuncionarioModel


class FuncionarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = FuncionarioModel
        fields = [ "id_funcionario", "nome_completo", "email", "telefone", "senha", "cargo",]