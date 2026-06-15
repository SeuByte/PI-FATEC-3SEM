import random
from src.usuarios.models import RecuperarSenhaModel
from django.core.mail import send_mail
from django.conf import settings

class RecuperarSenhaService:
    
    @staticmethod
    def gerar_token(email):
        token = str(random.randint(100000, 999999))
        RecuperarSenhaModel.objects.create(email=email, token=token)
        
        send_mail(subject='Recuperação de Senha', message=f''' 
                  seu codigo é: {token} Caso nao tenha solicitado, Verifique sua conta urgente.''',
                  from_email=settings.EMAIL_HOST_USER, recipient_list=[email],
                  fail_silently=False
                  )
        return token