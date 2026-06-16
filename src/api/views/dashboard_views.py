from src.api.models import Clientes, Pedidos, Produtos
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from src.api.services.dashboard_service import DashboardService



@api_view(["GET"])
def dashboard_stats(request):
    # Exemplo simples de agregação
    total_clientes = Clientes.objects.count()
    total_pedidos = Pedidos.objects.count()
    total_produtos = Produtos.objects.count()
    
    # Soma de receita (usando um pipeline de agregação do MongoDB)
    pipeline = [
        {"$match": {"Status": "Concluido"}}, 
        {"$group": {"_id": None, "total": {"$sum": "$Valor_total"}}}
    ]
    receita_obj = list(Pedidos.objects.aggregate(pipeline))
    receita = receita_obj[0]['total'] if receita_obj else 0
    
    contagem_por_grupo = DashboardService.get_contagem_por_grupo()
    
    relatorio_estoque = DashboardService.get_relatorio_estoque()

    return Response({
        "total_clientes": total_clientes,
        "total_produtos": total_produtos,
        "receita_total": float(receita),
        "pedidos_pendentes": Pedidos.objects(Status="Pendente").count(),
        "pedidos_enviados": Pedidos.objects(Status="Enviado").count(),
        "contagem_por_grupo": contagem_por_grupo,
        "ticket_medio": float(receita / total_pedidos) if total_pedidos > 0 else 0,
        "relatorio estoque": relatorio_estoque,
        "data_atual": datetime.now().strftime("%d/%m/%Y")
    })