import pandas as pd
from datetime import datetime, timedelta

import time

import matplotlib.pyplot as plt



class junta_anos:
    def __init__(self, arquivo_inicio, arquivo_final, ano_inicio, ano_final):

        dados_acoes = pd.read_csv(arquivo_inicio + str(ano_inicio) + arquivo_final + '.csv')

        for i in range(ano_inicio+1, ano_final + 1):

            dados_acoes_novo = pd.read_csv(arquivo_inicio + str(i) + arquivo_final + '.csv')

            dados_acoes = pd.concat([dados_acoes, dados_acoes_novo], ignore_index=True)
        
        
        dados_acoes = dados_acoes.sort_values(by="data_pregao")
        dados_acoes = dados_acoes.reset_index()
        
        dados_acoes.to_csv('PETR4_2016_2023.csv')


junta_anos('COTAHIST_A20', '_pandas_PETR4', 16, 23)

