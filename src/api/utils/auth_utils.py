import jwt
from datetime import datetime, timedelta
from functools import wraps
from rest_framework.response import Response
from src.janete.settings import SECRET_KEY

#Utilizamos autenticação stateless (JWT) para não depender de sessões do django, tendo em vista que as bibliotecas para tal não conversam com o Mongo.

# 1. A Fábrica: Gera o token
def gerar_token(email):
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# 2. O Porteiro: Valida o token
def token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization') or request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return Response({"error": "Token não fornecido"}, status=401)
        try:
            token = auth_header.split(" ")[1]
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return Response({"error": "Token inválido ou expirado"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper