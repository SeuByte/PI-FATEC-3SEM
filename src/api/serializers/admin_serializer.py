from .base_serializer import BaseSerializer




class AdminSerializer(BaseSerializer):
    
    # Validação do campo Email
    def validate_Email(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("O campo E-mail é obrigatório.")
        if "@" not in str(valor):
            raise ValueError("Insira um e-mail válido.")
        return str(valor).strip()

    # Validação do campo Senha
    def validate_Senha(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("O campo Senha é obrigatório.")
        return str(valor).strip()

    # Validação geral (opcional, para verificar se os dois campos existem)
    def validate(self, data):
        if 'Email' not in data or 'Senha' not in data:
            raise ValueError("Dados incompletos para login.")
        return data