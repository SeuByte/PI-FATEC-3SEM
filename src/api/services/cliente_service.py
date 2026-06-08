from src.api.models import Clientes
from django.contrib.auth.hashers import check_password, make_password
from src.api.serializers.cliente_serializer import ClienteSerializer
from bson import ObjectId
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
    
    
    
    @staticmethod
    def editar_cliente(cliente_id, novos_dados):
        # 1. Busca o cliente pelo ID
        try:
            cliente = Clientes.objects.get(id=ObjectId(cliente_id))
        except Clientes.DoesNotExist:
            raise ValueError("Cliente não encontrado.")

        # 2. Se a senha estiver sendo alterada, hasheie a nova senha
        if 'Senha' in novos_dados and novos_dados['Senha']:
            # Só hasheia se for uma senha nova (opcional: comparar com a atual)
            novos_dados['Senha'] = make_password(novos_dados['Senha'])

        # 3. Atualiza os campos do objeto com os novos dados
        for campo, valor in novos_dados.items():
            if hasattr(cliente, campo):
                setattr(cliente, campo, valor)

        # 4. Salva no banco
        cliente.save()
        return cliente
    
    @staticmethod
    def deletar_cliente(cliente_id):
        try:
            cliente = Clientes.objects.get(id=ObjectId(cliente_id))
            cliente.delete()
            return True
        except Clientes.DoesNotExist:
            raise ValueError("Cliente não encontrado.")
        except Exception as e:
            raise ValueError(f"Erro ao tentar deletar: {str(e)}")
        
        