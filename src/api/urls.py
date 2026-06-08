from django.urls import path
from src.api.views.produto_views import listar_produtos, listar_produto_id, deletar_produto, editar_produto, criar_produto
from src.api.views.cliente_views import ListarCliente, RegistroView, LoginCliente, ResetarSenha
from src.api.views.confirmar_recuperacao_views import ConfirmarRecuperacaoView
from src.api.views.listar_senha_views import ListarSenhaViews
from src.api.views.funcionario_views import CadastroFuncionarioView

urlpatterns = [
 path('produtos/', listar_produtos),#Funcionando
 path('produtos/<str:id>/', listar_produto_id),#Funcionando
 path('deletar_produto/<str:id>/', deletar_produto), #Funcionando
 path('editar_produto/<str:id>/', editar_produto),#Funcionando
 path('criar_produto/', criar_produto),#Funcionando
 path('cadastro_api/', RegistroView.as_view(), name='api_cadastro'),
 path('listar_cliente/', ListarCliente.as_view(), name='api-listar_clientes'),
 path('login_cliente/', LoginCliente.as_view(), name= 'api_Login_Cliente'),
 path('resetar_senha_cliente/', ResetarSenha.as_view(), name='api_Resetar_senha_cliente'),
 path('recuperar_senha/', ListarSenhaViews.as_view()),
 path('confirmar-recuperacao/', ConfirmarRecuperacaoView.as_view()),
 path('cadastro_funcionario/', CadastroFuncionarioView.as_view(), name='api_cadastro_funcionario')
]