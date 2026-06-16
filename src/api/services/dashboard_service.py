from src.api.models import Produtos



class DashboardService():
    @staticmethod
    def get_contagem_por_grupo():
        pipeline = [
            {"$group": {"_id": "$Grupo", "total": {"$sum": 1}}},
            {"$sort": {"total": -1}}
        ]
        return list(Produtos.objects.aggregate(pipeline))
    
    
    @staticmethod
    def get_relatorio_estoque():
        # Busca produtos ordenados pela quantidade de forma crescente (do menor para o maior)
        baixo_estoque = list(Produtos.objects.all().order_by("Estoque")[:5])
        
        # Busca produtos ordenados pela quantidade de forma decrescente (do maior para o menor)
        alto_estoque = list(Produtos.objects.all().order_by("-Estoque")[:5])
        
        return {
            "baixo_estoque": [
                {"nome": p.Nome, "quantidade": p.Estoque} for p in baixo_estoque
            ],
            "alto_estoque": [
                {"nome": p.Nome, "quantidade": p.Estoque} for p in alto_estoque
            ]
        }