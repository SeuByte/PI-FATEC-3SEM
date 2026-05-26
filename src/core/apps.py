from django.apps import AppConfig
from mongoengine import connect


class CoreConfig(AppConfig):
    name = 'src.core'
    
    def ready(self):
        connect(
            db="Teste",
            host="mongodb://localhost:27017/"
        )



   