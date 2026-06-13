from src.usuarios.models import FuncionarioModel

from src.api.serializers.funcionario_serializer import FuncionarioSerializer

class FuncionarioService:

    @staticmethod
    def criar_funcionario(dados):

        # Cria um novo funcionário
        FuncionarioModel.objects.create(
            **dados
        )


    @staticmethod
    def listar_funcionarios():

        # Busca todos os funcionários
        funcionarios = (
            FuncionarioModel.objects.all()
        )

        # Serializa os dados
        serializer = (
            FuncionarioSerializer(
                funcionarios,
                many=True
            )
        )

        return serializer.data


    @staticmethod
    def buscar_funcionario(
        id_funcionario
    ):

        try:

            # Busca funcionário pelo ID
            funcionario = (
                FuncionarioModel.objects.get(
                    id_funcionario=id_funcionario
                )
            )

            serializer = (
                FuncionarioSerializer(
                    funcionario
                )
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

            # Busca funcionário pelo ID
            funcionario = (
                FuncionarioModel.objects.get(
                    id_funcionario=id_funcionario
                )
            )

            # Atualiza somente os campos recebidos
            for campo, valor in dados.items():

                setattr(
                    funcionario,
                    campo,
                    valor
                )

            # Salva as alterações
            funcionario.save()

        except FuncionarioModel.DoesNotExist:

            raise ValueError(
                "Funcionário não encontrado"
            )