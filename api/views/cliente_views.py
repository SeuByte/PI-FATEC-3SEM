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
    
class RegistroView(APIView):
    def post(self, request):
        serializer = ClienteSerializer(data=request.data)
        try:
            
            if serializer.is_valid():
                serializer.save()
                return Response({"mensagem": "Cliente cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
         return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)