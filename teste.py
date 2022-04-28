
from datetime import datetime, timedelta


data_pregao = datetime.strptime('20200317', '%Y%m%d')
print(data_pregao)
dia = datetime.strptime('17/03/2021', '%d/%m/%Y')
print(dia)

if data_pregao != dia:
    print("ok")

else:
    print("NOK")