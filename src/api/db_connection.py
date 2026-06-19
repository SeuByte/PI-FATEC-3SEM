from mongoengine import connect


def conectar():

    connect(
        db="Teste",
        host="mongodb://localhost:27017/"
    )