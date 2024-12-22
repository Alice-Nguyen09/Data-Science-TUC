import pandas as pd
import sqlite3

def read_data():
    df = pd.read_csv('/Users/AliceNguyen/Documents/Data Manager - TUC/(År 1.4) Data Science/Apple2009-2024.csv', index_col=False)
    #df.info()
    return df

df = read_data()

columns_with_currency = [
    'EBITDA (millions)', 'Revenue (millions)', 'Gross Profit (millions)', 
    'Op Income (millions)', 'Net Income (millions)', 'EPS', 'Total Assets (millions)', 
    'Cash on Hand (millions)', 'Long Term Debt (millions)', 'Total Liabilities (millions)'
]

def currency_replacer(df, columns_with_currency):
    for col in columns_with_currency:
        df[col] = df[col].replace(r'[\$,]', '', regex=True).replace(',', '', regex=True).astype(float)


columns_with_percent = ['Gross Margin']
for col in columns_with_percent:
    df[col] = df[col].str.replace('%', '').astype(float) / 100
    df[col] = df[col].round(4)

df['Shares Outstanding'] = df['Shares Outstanding'].str.replace(',', '').astype(float)

df['Employees'] = df['Employees'].str.replace(',', '').astype(int)



con = sqlite3.connect('/Users/AliceNguyen/Documents/Data Manager - TUC/(År 1.4) Data Science/Apple2009-2024.csv.db')
df.to_sql('Appledata2009-2024', con, if_exists='replace')

currency_replacer(df, columns_with_currency)

def test_currency():
    df = pd.DataFrame(data={"test_column": ["$4567,765", "56"]})
    columns_with_currency = ["test_column"]
    currency_replacer(df, columns_with_currency)
    assert df.test_column.dtype == float

test_currency()

def process_currency_column(df, col):
    return df[col].replace(r'[\$,]', '', regex=True).astype(float)

def test_currency_conversion():
    data = {'Revenue (millions)': ['$1,000', '$2,000']}
    df = pd.DataFrame(data)
    df['Revenue (millions)'] = process_currency_column(df, 'Revenue (millions)')



def test_percentage_conversion():
    data = {'Gross Margin': ['50%', '25%']}
    df = pd.DataFrame(data)

    df['Gross Margin'] = df['Gross Margin'].str.replace('%', '').astype(float) / 100
    assert np.allclose(df['Gross Margin'].values, [0.5, 0.25])


print("Bearbetning är klar!")