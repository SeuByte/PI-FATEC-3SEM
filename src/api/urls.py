from django.urls import path
from src.api.views.produto_views import listar_produtos, listar_produto_id, deletar_produto, editar_produto, criar_produto
from src.api.views.cliente_views import listar_clientes, cadastrar_cliente, login_cliente, pagina_protegida, editar_cliente, deletar_cliente
from src.api.views.carrinho_views import adicionar_ao_carrinho, listar_carrinho, remover_item_carrinho, finalizar_carrinho, atualizar_quantidade_view
urlpatterns = [
    
    path('produtos/', listar_produtos, name='listar_produtos'),#Funcionando
    path('produtos/<str:id>/', listar_produto_id, name='listar_produto_id'),#Funcionando
    path('deletar_produto/<str:id>/', deletar_produto, name='deletar_produto'),#Funcionando
    path('editar_produto/<str:id>/', editar_produto, name='editar_produto'),#Funcionando
    path('criar_produto/', criar_produto, name='criar_produto'),#Funcionando
    
    path('cadastrar_cliente/', cadastrar_cliente, name='cadastrar_cliente'),#Funcionando
    path('editar_cliente/<str:cliente_id>/', editar_cliente, name='editar_cliente'),#Funcionando
    path('deletar_cliente/<str:cliente_id>/', deletar_cliente, name='deletar_cliente'),
    path('listar_cliente/', listar_clientes, name='listar_clientes'),#Funcionando
    path('login_cliente/', login_cliente, name='login_cliente'),#Funcionando
    path('rota-de-teste/', pagina_protegida, name='rota-de-teste'),#Pagina que apenas é possivel acessar após ter efeutado o login cliente(pagina de teste)
   
   path('adicionar_carrinho/', adicionar_ao_carrinho, name='adicionar_carrinho'),#Funcionando
   path('editar_carrinho/', atualizar_quantidade_view, name='editar_carrinho'),#Funcionando
   path('listar_carrinho/', listar_carrinho, name='adicionar_carrinho'),#Funcionando
   path('remover_item_carrinho/', remover_item_carrinho, name='remover_item_carrinho' ),#Funcionando
   path('finalizar_carrinho/', finalizar_carrinho, name='finalizar_carrinho')#Funcionando
]