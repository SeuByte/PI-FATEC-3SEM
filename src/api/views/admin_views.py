
from rest_framework.decorators import api_view
from rest_framework.response import Response
from src.api.utils.auth_utils import admin_required, gerar_token, token_required
from src.api.services.admin_service import AdminService
from src.api.serializers.admin_serializer import AdminSerializer
from rest_framework import status

@api_view(["GET"])
@token_required
@admin_required
def painel_admin(request):
    return Response({"message": "Bem-vindo, Admin!"})


@api_view(["POST"])
def login_admin(request):
    serializer = AdminSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    email = request.data.get("Email")
    senha = request.data.get("Senha")
    try:
        # 1. Autentica o admin
        admin = AdminService.autenticar_admin(email, senha)
        
        # 2. Gera o token usando o e-mail (ou ID) do admin autenticado
        token = gerar_token(email)
        
       
        return Response({
            "message": "Bem vindo administrador!",
            "token": token,        
            "isAdmin": True        
        }, status=status.HTTP_200_OK)
        
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)