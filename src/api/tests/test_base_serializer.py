import pytest
from src.api.serializers.base_serializer import BaseSerializer

# Classe de teste para simular um Serializer real
class ConcreteSerializer(BaseSerializer):
    def to_representation(self):
        return {"id": 1}
    
    def validate_nome(self, value):
        if value == "erro":
            raise ValueError("Erro de nome")
        return value.upper()

@pytest.mark.django_db
class TestBaseSerializer:

    def test_is_valid_sem_dados(self):
        serializer = ConcreteSerializer(data=None)
        assert serializer.is_valid() is False
        assert 'non_fields_errors' in serializer.errors

    def test_is_valid_com_sucesso(self):
        serializer = ConcreteSerializer(data={"nome": "matheus"})
        assert serializer.is_valid() is True
        assert serializer.validated_data["nome"] == "MATHEUS"

    def test_is_valid_com_erro_no_metodo(self):
        serializer = ConcreteSerializer(data={"nome": "erro"})
        assert serializer.is_valid() is False
        assert "nome" in serializer.errors

    def test_save_com_erros_deve_falhar(self):
        serializer = ConcreteSerializer(data={"nome": "erro"})
        serializer.is_valid() # Preenche self.errors
        with pytest.raises(ValueError, match="Não é possivel salvar com erros"):
            # Usando um objeto mock para simular o model
            class MockModel:
                def save(self): pass
            serializer.save(MockModel)

    def test_to_representation_nao_implementado(self):
        # Testa a exceção se esquecer de implementar o método
        class Incompleto(BaseSerializer):
            pass
        
        s = Incompleto()
        with pytest.raises(NotImplementedError):
            s.to_representation()
            
    def test_to_representation_execucao(self):
        serializer = ConcreteSerializer()
        resultado = serializer.to_representation()
        
        assert resultado == {"id": 1}
        
    def test_fluxo_completo_sucesso(self):
        serializer = ConcreteSerializer(data={"nome": "Matheus", "idade": 22})
        
        assert serializer.is_valid() is True
        assert serializer.validated_data["nome"] == "MATHEUS" 
        assert serializer.validated_data["idade"] == 22
        
        # Cobre o método save()
        class MockModel:
            def __init__(self, **kwargs): pass
            def save(self): pass
            
        instance = serializer.save(MockModel)
        assert instance is not None

    def test_fluxo_completo_falha(self):
        serializer = ConcreteSerializer(data={"nome": "erro"})
        
        assert serializer.is_valid() is False # Cobre o 'except ValueError'
        
        with pytest.raises(ValueError, match="Não é possivel salvar com erros"):
            serializer.save(None) # Cobre o 'if self.errors' no save()