from rest_framework import serializers
from src.usuarios.models import FuncionarioModel


class FuncionarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = FuncionarioModel

        fields = ["id_funcionario", "nome_completo", "email", "telefone", "senha", "cargo",]

        extra_kwargs = {
            "senha": {"write_only": True}
        }

    def validate_email(self, value):

        funcionario_id = None

        if self.instance:
            funcionario_id = self.instance.id_funcionario


        existe = FuncionarioModel.objects.filter(email=value).exclude(id_funcionario=funcionario_id).exists()

        if existe:

            raise serializers.ValidationError("Este email já está cadastrado.")

        return value