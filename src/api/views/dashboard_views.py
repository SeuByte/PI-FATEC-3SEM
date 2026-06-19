from rest_framework.decorators import api_view

from src.api.models import (
    Clientes,
    Produtos,
    Pedidos,
    StatusPedido
)

from src.api.services.dashboard_service import DashboardService
from src.api.utils.response import success


@api_view(["GET"])
def dashboard_stats(request):

    total_clientes = Clientes.objects.count()

    total_produtos = Produtos.objects.count()

    total_pedidos = Pedidos.objects.count()

    pedidos_pendentes = Pedidos.objects(
        Status=StatusPedido.PENDENTE
    ).count()

    pedidos_aprovados = Pedidos.objects(
        Status=StatusPedido.APROVADO
    ).count()

    pedidos_cancelados = Pedidos.objects(
        Status=StatusPedido.Cancelado
    ).count()

    receita_total = sum(
        float(pedido.Valor_total)
        for pedido in Pedidos.objects(
            Status=StatusPedido.APROVADO
        )
    )

    ticket_medio = (
        receita_total / total_pedidos
        if total_pedidos > 0
        else 0
    )

    return success({

        "total_clientes":
            total_clientes,

        "total_produtos":
            total_produtos,

        "total_pedidos":
            total_pedidos,

        "pedidos_pendentes":
            pedidos_pendentes,

        "pedidos_aprovados":
            pedidos_aprovados,

        "pedidos_cancelados":
            pedidos_cancelados,

        "receita_total":
            receita_total,

        "ticket_medio":
            round(ticket_medio, 2),

        "contagem_por_grupo":
            DashboardService.get_contagem_por_grupo(),

        "relatorio estoque":
            DashboardService.get_relatorio_estoque(),
            
        "produtos":
            DashboardService.get_produtos(),

    })