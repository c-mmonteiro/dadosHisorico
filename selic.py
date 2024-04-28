import pandas as pd
import requests

from datetime import datetime, timedelta

## TEMPLATE PARA O CODIGO DE IA

class selic:
    def __init__(self, arquivo_pandas_ativo):
        dados_acoes = pd.read_csv(arquivo_pandas_ativo + ".csv")
        dados_acoes.drop(['Unnamed: 0'], axis=1, inplace=True)

#####################################################3
################    SELIC
#####################################################
        # Definir o URL da API do BCB para a Taxa Selic
        dia_inicio = datetime.strptime(dados_acoes['time'][0], '%Y-%m-%d').strftime('%d/%m/%Y')
        dia_final = datetime.strptime(dados_acoes['time'][len(dados_acoes)-1], '%Y-%m-%d').strftime('%d/%m/%Y')

        url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial=' + dia_inicio + '&dataFinal=' + dia_final

        # Enviar uma solicitação HTTP GET para obter os dados
        response = requests.get(url)

        # Verificar se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Converter os dados JSON em um DataFrame do Pandas
            data = response.json()
            df = pd.DataFrame(data)
            
            # Converter a coluna 'data' para o formato de data
            df['data'] = pd.to_datetime(df['data'], dayfirst=True)
            
            # Renomear a coluna 'valor' para 'Taxa Selic'
            df.rename(columns={'valor': 'Selic'}, inplace=True)
        else:
            print('Erro ao obter os dados. Código de status:', response.status_code)


        selic_df = pd.DataFrame(columns=['time', 'selic'])
        for idx, d in enumerate(dados_acoes['time']):
            dados_selic = df[df['data'] == datetime.strptime(d, '%Y-%m-%d')]

            selic_df = pd.concat([selic_df, pd.DataFrame(
                        data={"time": [d], 'selic': [dados_selic['Selic'].values[0]],}
                        )], ignore_index=True)

#####################################################
#####################################################
        
        print(selic_df)
        selic_df.to_csv(arquivo_pandas_ativo + '_selic.csv')


selic('PETR4_2014_2023_porDia')
