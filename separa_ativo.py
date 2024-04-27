import pandas as pd
from datetime import datetime, timedelta

import time



class separa_ativo:
    def __init__(self, arquivo_pandas, ativo):

        inicio = time.time()

        dados_acoes = pd.read_csv(arquivo_pandas + '.csv')

        fim = time.time()
        print(f'Abriu arquivo {fim-inicio}')

        lista_ativo = dados_acoes[dados_acoes['cod_negociacao'].str.contains(ativo[0:4])]

        lista_ativo.to_csv(arquivo_pandas + '_' + ativo + '.csv')

        fim = time.time()
        print(f'Salvou {fim-inicio}')

        fim = time.time()
        print(f'Tempo {fim-inicio}')

separa_ativo('COTAHIST_A2022_pandas', "PETR4")
