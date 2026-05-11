from django.urls import path
from api.views.produtos_views import listar_produtos, listar_produto_id

urlpatterns = [
 path('listar_produtos/', listar_produtos),
 path('listar_produtos/<int:id>/', listar_produto_id),
]