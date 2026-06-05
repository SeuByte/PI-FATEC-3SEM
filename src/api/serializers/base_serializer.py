#Aqui em BaseSerializer, é onde será estabelecido o contrato de como os dados serão validados, "normas" vazias e os proprios serializers irão preencher essas normas.


class BaseSerializer:
    def __init__(self, obj=None, data=None):
        self.obj = obj
        self.data_input = data
        self.validated_data = {}
        self.errors = {}
        
        
    def to_representation(self):
        raise NotImplementedError()
    
    def is_valid(self):
        print(f"DEBUG: Dados recebidos no serializer: {self.data_input}")
        self.errors = {}
        self.validated_data = {}
        
        if self.data_input is None:
            self.errors['non_fields_errors'] = "Nenhum dado foi fornecido para validação."
            return False
        
        for campo, valor in self.data_input.items():
            nome_do_metodo =f"validate_{campo}"
            
            if hasattr(self, nome_do_metodo):
                metodo_de_validacao = getattr(self,nome_do_metodo)
                try:
                    valor_limpo = metodo_de_validacao(valor)
                    self.validated_data[campo] = valor_limpo
                except ValueError as e:
                    self.errors[campo] = str(e)
            else:
                self.validated_data[campo] = valor
            
        return len(self.errors) == 0
                    
                    
                    
    def save(self, model_class):
        if self.errors:
            raise ValueError(f"Não é possivel salvar com erros de validação: {self.errors}")
        instance = model_class(**self.validated_data)
        instance.save()
        self.obj = instance
        return instance