#Caso queira importar os dados do excel por qualquer motivo: 
#1- python manage.py shell
#2- from api.importers.excel_importer import importa_excel
#3 -importa_excel(r"C:\Users\macro\Downloads\PRODUTOS LOJA 27-4.xlsx")

import pandas as pd
from core.models import Produtos


def importa_excel(file_path):
    df = pd.read_excel(file_path)
    
   
    print("ARQUIVO ATUAL SENDO EXECUTADO:", __file__)
    print("testando arquivo")
    print("COLUNAS:", df.columns)
    print("PRIMEIRAS LINHAS:\n", df.head())
    
    for _, row in df.iterrows():
        Produtos(
            Nome=row["Descrição"],
            Estoque=row["Estoque"],
            Unidade=row["Unidade"],
            Valor_venda=row["Valor venda"],
            Grupo=row["Grupo"],
            Preco_100g=row["Preço 100g"]
        ).save()
        
        
        
        print("Importação finalizada!")

       
if __name__ == "__main__":
    file_path = r"C:\Users\macro\Downloads\PRODUTOS LOJA 27-4.xlsx"
    importa_excel(file_path)
    print("Importação concluída!")