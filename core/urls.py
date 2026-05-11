from django.urls import path
from . import views
from .views import lista_cliente, lista_produtos, login_cliente, cadastro_cliente

urlpatterns = [
 path('', views.index),
 path('clientes/', lista_cliente),
 path('produtos/', lista_produtos),
 path('login/', login_cliente),
 path('cadastro/cadastro_cliente', cadastro_cliente)
 
]