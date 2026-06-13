from rest_framework.views import APIView
from rest_framework.response import Response
from src.api.services.recuperacao_senha_service import (RecuperarSenhaService)
from src.api.models import Clientes

class ListarSenhaViews(APIView):
    
    def post(self, request):
        
        try:
            
            email = request.data.get("email")            
            cliente = Clientes.objects(Email=email).first()
            
            if not cliente:

                return Response({"erro": "Cliente não encontrado"}, status=404)

            token = RecuperarSenhaService.gerar_token(email)

            return Response({"mensagem": "Token enviado para o email."})

        except Exception as e:

            return Response({"erro": str(e)}, status=500)