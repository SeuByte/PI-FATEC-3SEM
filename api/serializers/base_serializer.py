#Aqui em BaseSerializer, é onde será estabelecido o contrato de como os dados serão validados, "normas" vazias e os proprios serializers irão preencher essas normas.


class BaseSerializer:
    def __init__(self, obj=None, data=None):
        self.obj = obj
        self.data_input = data
        
        
    def to_representation(self):
        raise NotImplementedError()
    
    def is_valid(self):
        return True
    
    def save(self, model_class):
        instance = model_class(**self.data_input)
        instance.save()
        return instance