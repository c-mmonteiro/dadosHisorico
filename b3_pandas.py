import pandas as pd
from datetime import datetime, timedelta

import time


class b3_pandas:
    def __init__(self, arquivo_bovespa):
        ## Vídeo Explicativo
        ## https://www.youtube.com/watch?v=vUMr1lpzm4Q
        ## Séries históricas disponíveis em
        ## http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/
        ## Estrutura do arquivo disponível em
        ## http://www.b3.com.br/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf
        tamanho_campos=[2,8,2,12,3,12,10,3,4,13,13,13,13,13,13,13,5,18,18,13,1,8,7,13,12,3]

        inicio = time.time()

        dados_acoes=pd.read_fwf(arquivo_bovespa + '.TXT', widths=tamanho_campos, header=0)#, encoding = "ISO-8859-1")
        fim = time.time()
        print(f'Abriu {fim-inicio}')

        ## Nomear as colunas
        dados_acoes.columns = [
        "tipo_registro",
        "data_pregao",
        "cod_bdi",
        "cod_negociacao",
        "tipo_mercado",
        "noma_empresa",
        "especificacao_papel",
        "prazo_dias_merc_termo",
        "moeda_referencia",
        "preco_abertura",
        "preco_maximo",
        "preco_minimo",
        "preco_medio",
        "preco_ultimo_negocio",
        "preco_melhor_oferta_compra",
        "preco_melhor_oferta_venda",
        "numero_negocios",
        "quantidade_papeis_negociados",
        "volume_total_negociado",
        "preco_exercicio",
        "ìndicador_correcao_precos",
        "data_vencimento" ,
        "fator_cotacao",
        "preco_exercicio_pontos",
        "codigo_isin",
        "num_distribuicao_papel"]

        fim = time.time()

        print(f'Nomeou as colunas {fim-inicio}')

        # Eliminar a última linha
        linha=len(dados_acoes["data_pregao"])
        dados_acoes=dados_acoes.drop(linha-1)

        fim = time.time()
        print(f'Tirou a ultima linha {fim-inicio}')

        # Ajustar valores com virgula (dividir os valores dessas colunas por 100)
        listaVirgula=[
        "preco_abertura",
        "preco_maximo",
        "preco_minimo",
        "preco_medio",
        "preco_ultimo_negocio",
        "preco_melhor_oferta_compra",
        "preco_melhor_oferta_venda",
        "volume_total_negociado",
        "preco_exercicio",
        "preco_exercicio_pontos"
        ]
        for coluna in listaVirgula:
            dados_acoes[coluna] = [i/100. for i in dados_acoes[coluna]]

        fim = time.time()
        print(f'Ajustou os valores com virgula {fim-inicio}') 

        dados_acoes['data_pregao'] = [datetime.strptime(str(int(i)), '%Y%m%d') for i in dados_acoes['data_pregao']]

        fim = time.time()
        print(f'Ajustou o dia {fim-inicio}')

        dados_acoes['data_vencimento'] = [datetime.strptime(str(int(i)), '%Y%m%d') for i in dados_acoes['data_vencimento']]

        fim = time.time()
        print(f'Ajustou o vencimento {fim-inicio}')

        dados_acoes.to_csv(arquivo_bovespa + '_pandas.csv')

        fim = time.time()
        print(f'Salvou {fim-inicio}')
        


b3_pandas("COTAHIST_A2014")



#Abriu 280.7998728752136
#Nomeou as colunas 281.36535716056824
#Tirou a ultima linha 283.5374348163605
#Ajustou os valores com virgula 289.13902711868286
#Ajustou o dia 313.49535727500916
#Ajustou o vencimento 337.7134177684784
#Salvou 389.8781883716583

#[781 rows x 26 columns]
#Tempo 392.21089458465576



