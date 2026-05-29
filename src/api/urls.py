from django.urls import path
from src.api.views.produto_views import listar_produtos, listar_produto_id, deletar_produto, editar_produto, criar_produto
from src.api.views.cliente_views import ListarCliente, RegistroView, LoginCliente, ResetarSenha

urlpatterns = [
 path('produtos/', listar_produtos),
 path('produtos/<str:id>/', listar_produto_id),
 path('deletar_produto/<str:id>/', deletar_produto), #Já está funcionando
 path('editar_produto/<str:id>/', editar_produto),#Ainda não está funcionando
 path('criar_produto/', criar_produto),
 path('cadastro_api/', RegistroView.as_view(), name='api_cadastro'),
 path('listar_cliente/', ListarCliente.as_view(), name='api-listar_clientes'),
 path('login_cliente/', LoginCliente.as_view(), name= 'api_Login_Cliente'),
 path('resetar_senha_cliente/', ResetarSenha.as_view(), name='api_Resetar_senha_cliente')
]