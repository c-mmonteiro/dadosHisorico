import pandas as pd
from datetime import datetime, timedelta

import numpy as np

import time

import bisect

import matplotlib.pyplot as plt


class separar_por_dia:
    def __init__(self, arquivo_pandas_ativo, ativo):

        dados_acoes = pd.read_csv(arquivo_pandas_ativo + ".csv")

        dados_acoes['data_pregao'] = pd.to_datetime(dados_acoes['data_pregao'])
        

        dias_list = dados_acoes['data_pregao'].unique()

        dados = pd.DataFrame(columns=['time', 'open', 'close',
                                       'call OTM A1', 'call ITM A1', 'call OTM A2', 'call ITM A2', 'call OTM B1', 'call ITM B1',
                                       'strike COA1', 'strike CIA1', 'strike COA2', 'strike CIA2', 'strike COB1', 'strike CIB1',
                                       'vencimento A', 'vencimento B',
                                       'std 15', 'std 30', 'std 45'])
            
        std_lista_15 = []
        std_lista_30 = []
        std_lista_45 = []
        for idx, dia in enumerate(dias_list):
            dados_dia_lista = dados_acoes[dados_acoes['data_pregao'] == dia]
            dados_ativo = dados_dia_lista[dados_dia_lista['cod_negociacao'] == ativo]
            
            
            if idx > 14:
                del(std_lista_15[14])
            std_lista_15.insert(0, dados_ativo['preco_ultimo_negocio'].item())

            if idx > 29:
                del(std_lista_30[29])
            std_lista_30.insert(0, dados_ativo['preco_ultimo_negocio'].item())

            if idx > 44:
                del(std_lista_45[44])
            std_lista_45.insert(0, dados_ativo['preco_ultimo_negocio'].item())

            if idx > 44:
                vencimentos_list = dados_dia_lista['data_vencimento'].unique()
                vencimentos_list = sorted(vencimentos_list)
                if pd.to_datetime(vencimentos_list[0]) == dia:
                    vencimentos_list.pop(0)

                call_strik_A_list = dados_dia_lista[((dados_dia_lista['data_vencimento'] == vencimentos_list[0]) & 
                                                    (dados_dia_lista['volume_total_negociado'] > 0) & 
                                                    (dados_dia_lista['tipo_mercado'] == 70) &
                                                    (dados_dia_lista['especificacao_papel'].str.contains('PN')))]
                call_strik_A_list = call_strik_A_list['preco_exercicio'].unique()
                call_strik_A_list = sorted(call_strik_A_list)
                indice = bisect.bisect_right(call_strik_A_list, dados_ativo['preco_ultimo_negocio'].item())

                call_OA1 = dados_dia_lista[((dados_dia_lista['data_vencimento'] == vencimentos_list[0]) & 
                                            (dados_dia_lista['volume_total_negociado'] > 0) & 
                                            (dados_dia_lista['tipo_mercado'] == 70) &
                                            (dados_dia_lista['preco_exercicio'] == call_strik_A_list[indice + 1]) &
                                            (dados_dia_lista['especificacao_papel'].str.contains('PN')))]           
                call_IA1 = dados_dia_lista[((dados_dia_lista['data_vencimento'] == vencimentos_list[0]) & 
                                            (dados_dia_lista['volume_total_negociado'] > 0) & 
                                            (dados_dia_lista['tipo_mercado'] == 70) &
                                            (dados_dia_lista['preco_exercicio'] == call_strik_A_list[indice]) &
                                            (dados_dia_lista['especificacao_papel'].str.contains('PN')))]
                call_OA2 = dados_dia_lista[((dados_dia_lista['data_vencimento'] == vencimentos_list[0]) & 
                                            (dados_dia_lista['volume_total_negociado'] > 0) & 
                                            (dados_dia_lista['tipo_mercado'] == 70) &
                                            (dados_dia_lista['preco_exercicio'] == call_strik_A_list[indice + 2]) &
                                            (dados_dia_lista['especificacao_papel'].str.contains('PN')))]
                call_IA2 = dados_dia_lista[((dados_dia_lista['data_vencimento'] == vencimentos_list[0]) & 
                                            (dados_dia_lista['volume_total_negociado'] > 0) & 
                                            (dados_dia_lista['tipo_mercado'] == 70) &
                                            (dados_dia_lista['preco_exercicio'] == call_strik_A_list[indice - 1]) &
                                            (dados_dia_lista['especificacao_papel'].str.contains('PN')))]
                
                call_strik_B_list = dados_dia_lista[((dados_dia_lista['data_vencimento'] == vencimentos_list[1]) & 
                                                    (dados_dia_lista['volume_total_negociado'] > 0) & 
                                                    (dados_dia_lista['tipo_mercado'] == 70) &
                                                    (dados_dia_lista['especificacao_papel'].str.contains('PN')))]
                call_strik_B_list = call_strik_B_list['preco_exercicio'].unique()
                call_strik_B_list = sorted(call_strik_B_list)
                indice = bisect.bisect_right(call_strik_B_list, dados_ativo['preco_ultimo_negocio'].item())

                call_OB1 = dados_dia_lista[((dados_dia_lista['data_vencimento'] == vencimentos_list[1]) & 
                                            (dados_dia_lista['volume_total_negociado'] > 0) & 
                                            (dados_dia_lista['tipo_mercado'] == 70) &
                                            (dados_dia_lista['preco_exercicio'] == call_strik_B_list[indice + 1]) &
                                            (dados_dia_lista['especificacao_papel'].str.contains('PN')))]           
                call_IB1 = dados_dia_lista[((dados_dia_lista['data_vencimento'] == vencimentos_list[1]) & 
                                            (dados_dia_lista['volume_total_negociado'] > 0) & 
                                            (dados_dia_lista['tipo_mercado'] == 70) &
                                            (dados_dia_lista['preco_exercicio'] == call_strik_B_list[indice]) &
                                            (dados_dia_lista['especificacao_papel'].str.contains('PN')))]      
        

                dados = pd.concat([dados, pd.DataFrame(
                        data={"time": [dia], 'open': [dados_ativo['preco_abertura'].item()], 'close': [dados_ativo['preco_ultimo_negocio'].item()],
                        'call OTM A1': [call_OA1['preco_ultimo_negocio'].item()], 'call ITM A1': [call_IA1['preco_ultimo_negocio'].item()], 
                        'call OTM A2': [call_OA2['preco_ultimo_negocio'].item()], 'call ITM A2': [call_IA2['preco_ultimo_negocio'].item()],
                        'call OTM B1': [call_OB1['preco_ultimo_negocio'].item()], 'call ITM B1': [call_IB1['preco_ultimo_negocio'].item()],
                        'strike COA1': [call_OA1['preco_exercicio'].item()], 'strike CIA1': [call_IA1['preco_exercicio'].item()], 
                        'strike COA2': [call_OA2['preco_exercicio'].item()], 'strike CIA2': [call_IA2['preco_exercicio'].item()], 
                        'strike COB1': [call_OB1['preco_exercicio'].item()], 'strike CIB1': [call_IB1['preco_exercicio'].item()],
                        'vencimento A': [(pd.to_datetime(vencimentos_list[0]) - dia).days], 'vencimento B': [(pd.to_datetime(vencimentos_list[1]) - dia).days],
                        'std 15': [np.std(std_lista_15)], 'std 30': [np.std(std_lista_30)], 'std 45': [np.std(std_lista_45)]}
                        )], ignore_index=True)
        
        print(dados)

        dados.to_csv(arquivo_pandas_ativo + '_porDia.csv')

        plt.plot(dados['time'], dados['close'])
        plt.show()


separar_por_dia('PETR4_2014_2023', 'PETR4')

#separa_ativo('COTAHIST_A2023_pandas_PETR4.csv', 'PETR4')