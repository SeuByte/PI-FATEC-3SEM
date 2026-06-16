from django.apps import AppConfig
from mongoengine import connect

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.api'

    def ready(self):
        print("CONEXAO SUCEDIDA")
        connect(
            db="Teste",
            host="mongodb://localhost:27017/"
        )

