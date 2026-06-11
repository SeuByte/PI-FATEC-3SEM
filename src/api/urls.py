from django.urls import path
from src.api.views.produto_views import listar_produtos, listar_produto_id, deletar_produto, editar_produto, criar_produto
from src.api.views.confirmar_recuperacao_views import ConfirmarRecuperacaoView
from src.api.views.listar_senha_views import ListarSenhaViews
from src.api.views.funcionario_views import CadastroFuncionarioView, ListarFuncionariosView, BuscarFuncionarioView
from src.api.views.cliente_views import listar_clientes, cadastrar_cliente, login_cliente, pagina_protegida, editar_cliente, deletar_cliente

urlpatterns = [
    # Produtos
    path('produtos/', listar_produtos, name='listar_produtos'),#Funcionando
    path('produtos/<str:id>/', listar_produto_id, name='listar_produto_id'),#Funcionando
    path('deletar_produto/<str:id>/', deletar_produto, name='deletar_produto'),#Funcionando
    path('editar_produto/<str:id>/', editar_produto, name='editar_produto'),#Funcionando
    path('criar_produto/', criar_produto, name='criar_produto'),#Funcionando

    # Clientes
    
    path('cadastrar_cliente/', cadastrar_cliente, name='cadastrar_cliente'),#Funcionando
    path('editar_cliente/<str:cliente_id>/', editar_cliente, name='editar-cliente'),#Funcionando
    path('deletar_cliente/<str:cliente_id>/', deletar_cliente, name='deletar_cliente'),
    path('listar_cliente/', listar_clientes, name='listar_clientes'),#Funcionando
    path('login_cliente/', login_cliente, name='login_cliente'),#Funcionando
    path('rota-de-teste/', pagina_protegida, name='rota-de-teste'),

    #Funcionarios e Recuperação de Senha
    path('recuperar_senha/', ListarSenhaViews.as_view()),
    path('confirmar-recuperacao/', ConfirmarRecuperacaoView.as_view()),
    path('cadastro_funcionario/', CadastroFuncionarioView.as_view(), name='cadastro_funcionario')
    path('funcionarios/', ListarFuncionariosView.as_view(), name='listar_funcionarios')
    path('funcionarios/<int:id_funcionario>/', BuscarFuncionarioView.as_view(), name='buscar_funcionario')
]