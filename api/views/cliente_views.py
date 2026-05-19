from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from api.serializers.cliente_serializer import ClienteSerializer
from core.models import Clientes

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