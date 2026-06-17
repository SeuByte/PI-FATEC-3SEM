from rest_framework.decorators import api_view
from src.api.models import Produtos, Pedidos, StatusPedido
from src.api.services.dashboard_service import DashboardService
from src.api.utils.response import success


@api_view(["GET"])
def dashboard_stats(request):
    total_produtos = Produtos.objects.count()
    resumo_pedidos = DashboardService.get_resumo_pedidos()
    receita_total = sum(float(pedido.Valor_total) for pedido in Pedidos.objects(
            Status=StatusPedido.APROVADO
        )
    )

    ticket_medio = (receita_total /
        resumo_pedidos["total_pedidos"]
        if resumo_pedidos["total_pedidos"] > 0
        else 0
    )

    return success({

        "total_produtos":
            total_produtos,

        "total_pedidos":
            resumo_pedidos["total_pedidos"],

        "pedidos_pendentes":
            resumo_pedidos["pendentes"],

        "pedidos_aprovados":
            resumo_pedidos["aprovados"],

        "pedidos_cancelados":
            resumo_pedidos["cancelados"],

        "receita_total":
            receita_total,

        "ticket_medio":
            round(ticket_medio, 2),

        "contagem_por_grupo":
            DashboardService.get_contagem_por_grupo(),

        "relatorio estoque":
            DashboardService.get_relatorio_estoque()

    })