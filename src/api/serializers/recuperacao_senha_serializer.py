from rest_framework import serializers

class RecuperarSenhaSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True, max_length=6)
    nova_senha = serializers.CharField(required=True, write_only=True)
    confirmar_senha = serializers.CharField(required=True, write_only=True)
    
    def validate(self, datas):
        senha = datas.get("nova_senha")
        confirmacao = datas.get("confirmar_senha")
        
        if senha != confirmacao:
            raise serializers.ValidationError("As Senhas Nao sao iguais")
        
        if len(senha) < 8:
            raise serializers.ValidationError("A senha precisa ter pelo menos 8 caracteres")
        
        return datas