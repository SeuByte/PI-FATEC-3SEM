from django.urls import path
from api.views.produto_views import listar_produtos, listar_produto_id, apagar_produto
from api.views.cliente_views import ListarCliente, RegistroView, LoginCliente

urlpatterns = [
 path('produtos/', listar_produtos),
 path('produtos/<int:id>/', listar_produto_id),
 path('produtos/apagar/<str:id>',apagar_produto),
 path('cadastro_api/', RegistroView.as_view(), name='api_cadastro'),
 path('listar_cliente/', ListarCliente.as_view(), name='api-listar_clientes'),
 path('login_cliente/', LoginCliente.as_view(), name= 'api_Login_Cliente')
]