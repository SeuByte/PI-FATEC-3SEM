from src.api.models import Clientes, Pedidos
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime



@api_view(["GET"])
def dashboard_stats(request):
    # Exemplo simples de agregação
    total_clientes = Clientes.objects.count()
    total_pedidos = Pedidos.objects.count()
    
    # Soma de receita (usando um pipeline de agregação do MongoDB)
    pipeline = [
        {"$match": {"Status": "Concluido"}}, 
        {"$group": {"_id": None, "total": {"$sum": "$Valor_total"}}}
    ]
    receita_obj = list(Pedidos.objects.aggregate(pipeline))
    receita = receita_obj[0]['total'] if receita_obj else 0

    return Response({
        "total_clientes": total_clientes,
        "receita_total": float(receita),
        "pedidos_pendentes": Pedidos.objects(Status="Pendente").count(),
        "ticket_medio": float(receita / total_pedidos) if total_pedidos > 0 else 0,
        "data_atual": datetime.now().strftime("%d/%m/%Y")
    })