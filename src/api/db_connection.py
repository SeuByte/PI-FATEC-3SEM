from mongoengine import connect


def conectar():

    connect(
        db="Teste",
        host="mongodb://root:123@localhost:27017/"
    )