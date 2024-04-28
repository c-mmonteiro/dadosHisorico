import pandas as pd
import requests

from datetime import datetime, timedelta

## TEMPLATE PARA O CODIGO DE IA

class organizar_lag:
    def __init__(self, arquivo_pandas_ativo, num_dias_lag, num_dias_previsao):
        dados_selic = pd.read_csv(arquivo_pandas_ativo + "_selic.csv")
        dados_selic.drop(['Unnamed: 0'], axis=1, inplace=True)
        print(dados_selic)


        dados_acoes = pd.read_csv(arquivo_pandas_ativo + ".csv")
        dados_acoes.drop(['Unnamed: 0'], axis=1, inplace=True)
        dados_copia = dados_acoes.copy()  
        print(dados_acoes)

        for idx in range(0, num_dias_lag):
            dados_copia['time -' + str(idx + 1)] = dados_copia['time'].shift(idx + 1)
            dados_copia['open -' + str(idx + 1)] = dados_copia['open'].shift(idx + 1)
            dados_copia['close -' + str(idx + 1)] = dados_copia['close'].shift(idx + 1)
            dados_copia['call OTM A1 -' + str(idx + 1)] = dados_copia['call OTM A1'].shift(idx + 1)
            dados_copia['call ITM A1 -' + str(idx + 1)] = dados_copia['call ITM A1'].shift(idx + 1)
            dados_copia['call OTM A2 -' + str(idx + 1)] = dados_copia['call OTM A2'].shift(idx + 1)
            dados_copia['call ITM A2 -' + str(idx + 1)] = dados_copia['call ITM A2'].shift(idx + 1)
            dados_copia['call OTM B1 -' + str(idx + 1)] = dados_copia['call OTM B1'].shift(idx + 1)
            dados_copia['call ITM B1 -' + str(idx + 1)] = dados_copia['call ITM B1'].shift(idx + 1)
            dados_copia['strike COA1 -' + str(idx + 1)] = dados_copia['strike COA1'].shift(idx + 1)
            dados_copia['strike CIA1 -' + str(idx + 1)] = dados_copia['strike CIA1'].shift(idx + 1)
            dados_copia['strike COA2 -' + str(idx + 1)] = dados_copia['strike COA2'].shift(idx + 1)
            dados_copia['strike CIA2 -' + str(idx + 1)] = dados_copia['strike CIA2'].shift(idx + 1)
            dados_copia['strike COB1 -' + str(idx + 1)] = dados_copia['strike COB1'].shift(idx + 1)
            dados_copia['strike CIB1 -' + str(idx + 1)] = dados_copia['strike CIB1'].shift(idx + 1)
            dados_copia['vencimento A -' + str(idx + 1)] = dados_copia['vencimento A'].shift(idx + 1)
            dados_copia['vencimento B -' + str(idx + 1)] = dados_copia['vencimento B'].shift(idx + 1)
            dados_copia['std 15 -' + str(idx + 1)] = dados_copia['std 15'].shift(idx + 1)
            dados_copia['std 30 -' + str(idx + 1)] = dados_copia['std 30'].shift(idx + 1)
            dados_copia['std 45 -' + str(idx + 1)] = dados_copia['std 45'].shift(idx + 1)

        dados_copia['selic'] = dados_selic['selic'].to_list()

        dados_copia['close +' + str(num_dias_previsao)] = dados_copia['close'].shift(-num_dias_previsao)

        dados_copia = dados_copia.dropna().reset_index(drop=True)
        
        print(dados_copia)
        #dados_copia.to_csv(arquivo_pandas_ativo + '_porDia.csv')


organizar_lag('PETR4_2014_2023_porDia', 5, 1)
