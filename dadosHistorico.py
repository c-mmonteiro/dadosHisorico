import pandas as pd
from datetime import datetime, timedelta


class dadosHistorico:
    def __init__(self, arquivo_bovespa, dia, ativo):
        ## Vídeo Explicativo
        ## https://www.youtube.com/watch?v=vUMr1lpzm4Q
        ## Séries históricas disponíveis em
        ## http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/
        ## Estrutura do arquivo disponível em
        ## http://www.b3.com.br/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf
        tamanho_campos=[2,8,2,12,3,12,10,3,4,13,13,13,13,13,13,13,5,18,18,13,1,8,7,13,12,3]

        dados_acoes=pd.read_fwf(arquivo_bovespa, widths=tamanho_campos, header=0)

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

        # Eliminar a última linha
        linha=len(dados_acoes["data_pregao"])
        dados_acoes=dados_acoes.drop(linha-1)

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

        dados_acoes['data_pregao'] = [datetime.strptime(str(int(i)), '%Y%m%d') for i in dados_acoes['data_pregao']]
        dados_acoes['data_vencimento'] = [datetime.strptime(str(int(i)), '%Y%m%d') for i in dados_acoes['data_vencimento']]


        lista_dia = dados_acoes[(dados_acoes['data_pregao'] == dia)]
        lista_dia_ativo = lista_dia[lista_dia['cod_negociacao'].str.contains(ativo[0:4])]
        print(lista_dia_ativo)
        print(lista_dia_ativo['data_vencimento'].unique())
        

dia = datetime.strptime('17/03/2020', '%d/%m/%Y')
dadosHistorico("COTAHIST_A2020.TXT", dia, "BOVA11")



