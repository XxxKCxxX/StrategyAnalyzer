import pandas as pd

data = pd.read_csv('FEDFUNDS.csv')
#the format should be MM-YYYY
data['MONTH'] = pd.to_datetime(data['MONTH']).dt.strftime('%m.%Y')

#data['UNRATE'] = data['UNRATE'] * 100000
data.to_csv('fedfunds.csv', index=False)