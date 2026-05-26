from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from src.api.serializers.cliente_serializer import ClienteSerializer
from src.core.models import Clientes

class ListarCliente(APIView):
    def get(self, request):
        clientes = Clientes.objects.all()
        data = [ClienteSerializer(obj=c).to_representation() for c in clientes]
        return Response(data)
    
class LoginCliente(APIView):
    def post(self, request):
        Email = request.data.get('Email')
        Senha = request.data.get('Senha')
        cliente = Clientes.objects.filter(Email=Email, Senha=Senha).first()
        if cliente:
           return Response({"msg": "Login feito com sucesso!"})

        return Response({"msg": "Conta não encontrada :("}, status=400)


class RegistroView(APIView):
    def post(self, request):
        serializer = ClienteSerializer(data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response({"mensagem": "Cliente cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ResetarSenha(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        email = data.get('email')
        new_password = data.get('new_password')
        try:
            user = Clientes.objects.get(Email=email)
            user.Senha = new_password
            user.save()
            return Response({"mensagem": "Senha alterada com sucesso!"}, status=status.HTTP_200_OK)
        except Clientes.DoesNotExist:
            return Response({"mensagem": "Usuário não encontrado."}, status=status.HTTP_400_BAD_REQUEST)