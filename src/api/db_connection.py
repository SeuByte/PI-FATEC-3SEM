from mongoengine import connect


def conectar():

    connect(
        db="Teste",
        host="mongodb://localhost:27017/" #mudar depois para mongodb://root:123@localhost:27017/ 
    )