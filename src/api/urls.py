from django.urls import path
from src.api.views.produto_views import listar_produtos, listar_produto_id, deletar_produto, editar_produto, criar_produto
from src.api.views.cliente_views import listar_clientes, cadastrar_cliente, login_cliente

urlpatterns = [
<<<<<<< HEAD
path('produtos/', listar_produtos, name='listar_produtos'),#Funcionando
    path('produtos/<str:id>/', listar_produto_id, name='listar_produto_id'),#Funcionando
    path('deletar_produto/<str:id>/', deletar_produto, name='deletar_produto'),#Funcionando
    path('editar_produto/<str:id>/', editar_produto, name='editar_produto'),#Funcionando
    path('criar_produto/', criar_produto, name='criar_produto'),#Funcionando
    
    path('cadastrar_cliente/', cadastrar_cliente, name='cadastrar_cliente'),#Funcionando
    path('listar_cliente/', listar_clientes, name='listar_clientes'),#Funcionando
    path('login_cliente/', login_cliente, name='login_cliente'),#Funcionando
=======
 path('produtos/', listar_produtos),#Funcionando
 path('produtos/<str:id>/', listar_produto_id),#Funcionando
 path('deletar_produto/<str:id>/', deletar_produto), #Funcionando
 path('editar_produto/<str:id>/', editar_produto),#Funcionando
 path('criar_produto/', criar_produto),#Funcionando
 path('cadastrar_cliente/', cadastrar_cliente),#Funcionando
 path('listar_cliente/', listar_clientes),#Funcionando
 path('login_cliente/', login_cliente),#Funcionando
>>>>>>> 871f635e9a99a5a3647a49efef64b3faeffe5960

]