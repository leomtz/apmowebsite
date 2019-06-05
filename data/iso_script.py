import pandas as pd

codes=pd.read_csv('iso.csv',quotechar='"')[['alpha-3','name']]
codes.columns=['code','country']
codes.to_csv('iso-alpha-3.csv',index=False)