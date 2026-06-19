from decimal import Decimal

from src.api.models import Produtos, Pedidos, StatusPedido


class DashboardService:


    @staticmethod
    def converter_decimal(valor):

        if valor is None:
            return 0.0

        if isinstance(valor, Decimal):
            return float(valor)

        try:
            return float(
                valor.to_decimal()
            )

        except AttributeError:

            return float(valor)


    @staticmethod
    def get_contagem_por_grupo():

        pipeline = [

            {

                "$group": {

                    "_id": "$Grupo",

                    "total": {

                        "$sum": 1

                    }

                }

            },

            {

                "$sort": {

                    "total": -1

                }

            }

        ]

        return list(

            Produtos.objects.aggregate(

                pipeline

            )

        )


    @staticmethod
    def get_relatorio_estoque():

        baixo_estoque = list(

            Produtos.objects.order_by(

                "Estoque"

            )[:5]

        )


        alto_estoque = list(

            Produtos.objects.order_by(

                "-Estoque"

            )[:5]

        )


        return {


            "baixo_estoque": [

                {

                    "nome": produto.Nome,

                    "quantidade":

                        DashboardService.converter_decimal(

                            produto.Estoque

                        )

                }

                for produto in baixo_estoque

            ],



            "alto_estoque": [

                {

                    "nome": produto.Nome,

                    "quantidade":

                        DashboardService.converter_decimal(

                            produto.Estoque

                        )

                }

                for produto in alto_estoque

            ]

        }



    @staticmethod
    def get_produtos():

        produtos = Produtos.objects.order_by(

            "Nome"

        )


        return [

            {

                "id": str(

                    produto.id

                ),

                "nome":

                    produto.Nome,


                "grupo":

                    produto.Grupo,


                "estoque":

                    DashboardService.converter_decimal(

                        produto.Estoque

                    ),


                "valor":

                    DashboardService.converter_decimal(

                        produto.Valor_venda

                    )

            }

            for produto in produtos

        ]



    @staticmethod
    def get_resumo_pedidos():


        return {


            "total_pedidos":

                Pedidos.objects.count(),



            "pendentes":

                Pedidos.objects(

                    Status=StatusPedido.PENDENTE

                ).count(),



            "aprovados":

                Pedidos.objects(

                    Status=StatusPedido.APROVADO

                ).count(),



            "cancelados":

                Pedidos.objects(

                    Status=StatusPedido.Cancelado

                ).count()

        }