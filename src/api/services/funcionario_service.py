from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from src.usuarios.models import FuncionarioModel
from src.api.serializers.funcionario_serializer import FuncionarioSerializer


class FuncionarioService:


    @staticmethod
    def criar_funcionario(dados):

        dados["senha"] = make_password(dados["senha"])

        funcionario = FuncionarioModel.objects.create(**dados)

        return funcionario



    @staticmethod
    def listar_funcionarios():

        funcionarios = FuncionarioModel.objects.all()

        serializer = FuncionarioSerializer(funcionarios, many=True)

        return serializer.data



    @staticmethod
    def buscar_funcionario(id_funcionario):

        try:

            funcionario = FuncionarioModel.objects.get(id_funcionario=id_funcionario)

            serializer = FuncionarioSerializer(funcionario)

            return serializer.data

        except FuncionarioModel.DoesNotExist:

            raise ValueError("Funcionário não encontrado")



    @staticmethod
    def atualizar_funcionario(id_funcionario, dados):


        try:

            funcionario = FuncionarioModel.objects.get(id_funcionario=id_funcionario)


            campos_permitidos = ["nome_completo", "email", "telefone", "senha", "cargo"]


            for campo, valor in dados.items():

                if campo in campos_permitidos:

                    if campo == "senha":

                        valor = make_password(valor)
                        
                    setattr(funcionario, campo, valor)


            funcionario.save()

            return funcionario

        except FuncionarioModel.DoesNotExist:

            raise ValueError("Funcionário não encontrado")



    @staticmethod
    def deletar_funcionario(id_funcionario):


        try:

            funcionario = FuncionarioModel.objects.get(id_funcionario=id_funcionario)

            funcionario.delete()
            
        except FuncionarioModel.DoesNotExist:

            raise ValueError("Funcionário não encontrado")