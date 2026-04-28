import pandas as pd

data = pd.read_csv('Book1.csv', index_col=0)
symbols = pd.DataFrame(data.index)
print(symbols)

symbols.to_csv('symbols.csv', index=False)