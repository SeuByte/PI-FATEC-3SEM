from src.api.models import Clientes
from django.contrib.auth.hashers import check_password 
from src.api.serializers.cliente_serializer import ClienteSerializer

class ClienteService:
    @staticmethod
    def listar_cliente():
        clientes = Clientes.objects.all()
        data = [ClienteSerializer(obj=c).to_representation() for c in clientes]
        return data

    @staticmethod
    def autenticar(email, senha_digitada):
        # Busca o cliente pelo e-mail
        cliente = Clientes.objects.filter(Email=email).first()
        #Se o cliente existir e se a senha digita coincide com a do banco.
        if cliente:
            # DEBUG: Coloque o print ANTES da verificação
            print(f"\nDEBUG: Senha digitada: {senha_digitada}")
            print(f"DEBUG: Senha no banco: {cliente.Senha}")
            if cliente and check_password(senha_digitada, cliente.Senha):     
                
                return cliente
            else:
                print("DEBUG: A verificação check_password FALHOU!")
        raise ValueError("Email ou senha incorretos") 
        
       

    @staticmethod
    def criar_cliente(data):
        # Aqui o serializer já foi validado na View, então é salvo
        novo_cliente = Clientes(**data)
        novo_cliente.save()
        return novo_cliente