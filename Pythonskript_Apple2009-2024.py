import pandas as pd
import sqlite3

df = pd.read_csv('/Users/AliceNguyen/Documents/Data Manager - TUC/(År 1.4) Data Science/Apple2009-2024.csv', index_col=False)

df.info()

columns_with_currency = [
    'EBITDA (millions)', 'Revenue (millions)', 'Gross Profit (millions)', 
    'Op Income (millions)', 'Net Income (millions)', 'EPS', 'Total Assets (millions)', 
    'Cash on Hand (millions)', 'Long Term Debt (millions)', 'Total Liabilities (millions)'
]

for col in columns_with_currency:
    df[col] = df[col].replace(r'[\$,]', '', regex=True).replace(',', '', regex=True).astype(float)

columns_with_percent = ['Gross Margin']
for col in columns_with_percent:
    df[col] = df[col].str.replace('%', '').astype(float) / 100
    df[col] = df[col].round(4)

df['Shares Outstanding'] = df['Shares Outstanding'].str.replace(',', '').astype(float)

df['Employees'] = df['Employees'].str.replace(',', '').astype(int)

df.info()

con = sqlite3.connect('/Users/AliceNguyen/Documents/Data Manager - TUC/(År 1.4) Data Science/Apple2009-2024.csv.db')

df.to_sql('Appledata2009-2024', con, if_exists='replace')