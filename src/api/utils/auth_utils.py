import jwt
from datetime import datetime, timedelta
from functools import wraps
from rest_framework.response import Response
from src.janete.settings import SECRET_KEY

# Utilizamos autenticação stateless (JWT) para não depender de sessões do django, tendo em vista que as bibliotecas para tal não conversam com o Mongo.

# 1. Gera o token
def gerar_token(email):
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# 2. Valida o token
def token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization') or request.META.get('HTTP_AUTHORIZATION')
        
        # 1. Verifica se o header existe e se começa com "Bearer "
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"error": "Token não fornecido ou formato incorreto"}, status=401)
        
        try:
            # 2. Pega a segunda parte (o token em si)
            token = auth_header.split(" ")[1]
            if not token:
                return Response({"error": "Token vazio"}, status=401)
                
            # 3. Decodifica
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            
            # Injeção no request para reconhecer o email do usuário
            request.user_email = payload['email']
            
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expirado"}, status=401)
        except jwt.InvalidTokenError:
            return Response({"error": "Token inválido"}, status=401)
        except Exception:
            # Captura qualquer outro erro de formatação/acesso
            return Response({"error": "Erro na validação do token"}, status=401)
            
        return view_func(request, *args, **kwargs)
    return wrapper