from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from usuarios.model import FuncionarioModel
from src.api.serializers.funcionario_serializer import FuncionarioSerializer

class CadastroFuncionarioView(APIView):
    def post(self, request):
        serializer = FuncionarioSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save
            
            return Response({"mensagem": "Funcionario Cadastra com sucesso!"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)