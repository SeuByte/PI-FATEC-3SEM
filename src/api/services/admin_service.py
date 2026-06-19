from src.api.models import Admin
from django.contrib.auth.hashers import check_password

class AdminService:
    
    # Defina aqui quais e-mails têm permissão de administrador
    EMAILS_ADMINS = ["admin@exemplo.com", "chefe@empresa.com"]

    @staticmethod
    def autenticar_admin(email, senha_digitada):
        print(f"DEBUG: O e-mail recebido é: '{email}'")
        # 1. Verifica se o e-mail está na lista de permitidos
        if email not in AdminService.EMAILS_ADMINS:
            raise ValueError("Acesso negado: E-mail não autorizado para a área administrativa.")

        # 2. Busca o usuário no banco
        admin = Admin.objects.filter(Email=email).first()
        
        # 3. Verifica se existe e se a senha está correta
        if admin and check_password(senha_digitada, admin.Senha):
            return admin
            
        raise ValueError("Credenciais inválidas.")