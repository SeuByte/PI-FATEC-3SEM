from django.urls import path
from .views import buscar_produtos_views

urlpatterns = [
 path('/api/listar-produtos', buscar_produtos_views.api),
]