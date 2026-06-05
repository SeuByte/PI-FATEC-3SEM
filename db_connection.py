import os
from mongoengine import connect

def get_db_connection():
  
    mongo_host = os.getenv('MONGO_HOST', 'localhost')
    
    # Se estiver rodando localmente (Windows), a porta é 27018.
    # Se estiver rodando dentro do container, a porta é 27017.
    mongo_port = 27018 if mongo_host == 'localhost' else 27017
    
    connect(
        db='testando',
        host=mongo_host,
        port=mongo_port
    )