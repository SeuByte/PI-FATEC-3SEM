from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from src.usuarios.models import FuncionarioModel
from src.api.serializers.funcionario_serializer import FuncionarioSerializer


class CadastroFuncionarioView(APIView):
    def post(self, request):
        serializer = FuncionarioSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({"mensagem": "Funcionario Cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarFuncionariosView(APIView):

    def get(self, request):

        funcionarios = (FuncionarioModel.objects.all())

        serializer = (FuncionarioSerializer(funcionarios,many=True))

        return Response(serializer.data)

        
class BuscarFuncionarioView(APIView):

    def get(self, request, id_funcionario):
        
        try:

            funcionario = (FuncionarioModel.objects.get(id_funcionario=id_funcionario))

            serializer = (FuncionarioSerializer(funcionario))

            return Response(serializer.data)

        except FuncionarioModel.DoesNotExist:

            return Response({"erro": "Funcionário não encontrado"}, status=404)

class AtualizarFuncionarioView(APIView):
    
    def put (self, request, id_funcionario):
        
        try:
            funcionario = FuncionarioModel.objects.get(id_funcionario=id_funcionario)
            serializer = FuncionarioSerializer(funcionario, data=request.data, partial=True) 
            
            if serializer.is_valid():
                return Response({"mensagem": "Funcionario Atualizado com Sucesso!"})
            
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except FuncionarioModel.DoesNotExist:
            return Response({"mensagem": "Funcionario Não Encontrado"}, status=400)
        
        except Exception as e:
            return Response({"erro": {e}}, status=500)