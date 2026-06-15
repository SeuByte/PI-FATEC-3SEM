from src.usuarios.models import FuncionarioModel

from src.api.serializers.funcionario_serializer import FuncionarioSerializer


class FuncionarioService:

    @staticmethod
    def criar_funcionario(dados):

        FuncionarioModel.objects.create(**dados)

    @staticmethod
    def listar_funcionarios():

        funcionarios = FuncionarioModel.objects.all()

        serializer = FuncionarioSerializer(
            funcionarios,
            many=True
        )

        return serializer.data

    @staticmethod
    def buscar_funcionario(id_funcionario):

        try:

            funcionario = FuncionarioModel.objects.get(
                id_funcionario=id_funcionario
            )

            serializer = FuncionarioSerializer(
                funcionario
            )

            return serializer.data

        except FuncionarioModel.DoesNotExist:

            raise ValueError(
                "Funcionário não encontrado"
            )

    @staticmethod
    def atualizar_funcionario(
        id_funcionario,
        dados
    ):

        try:

            funcionario = FuncionarioModel.objects.get(
                id_funcionario=id_funcionario
            )

            for campo, valor in dados.items():

                setattr(
                    funcionario,
                    campo,
                    valor
                )

            funcionario.save()

        except FuncionarioModel.DoesNotExist:

            raise ValueError(
                "Funcionário não encontrado"
            )

    @staticmethod
    def deletar_funcionario(id_funcionario):

        try:

            funcionario = FuncionarioModel.objects.get(
                id_funcionario=id_funcionario
            )

            funcionario.delete()

        except FuncionarioModel.DoesNotExist:

            raise ValueError(
                "Funcionário não encontrado"
            )