import pandas as pd 
data = pd.read_csv("../demo/sales.csv",sep=';') 
print(data['toko'])
print(data.groupby(['toko','tanggal'])['total'].mean())
pv=data.pivot(index='toko',columns='tanggal',values='total')
print(pv.to_json(orient='records'))
print(pv.to_html())
