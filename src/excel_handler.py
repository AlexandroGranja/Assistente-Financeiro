import pandas as pd

EXCEL_FILE = 'gastos.xlsx'

def initialize_excel():
    try:
        pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Data', 'Descrição', 'Valor', 'Categoria'])
        df.to_excel(EXCEL_FILE, index=False)

def add_expense(data, descricao, valor, categoria):
    initialize_excel()
    df = pd.read_excel(EXCEL_FILE)
    new_expense = pd.DataFrame([{'Data': data, 'Descrição': descricao, 'Valor': valor, 'Categoria': categoria}])
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

def get_total_expenses():
    initialize_excel()
    df = pd.read_excel(EXCEL_FILE)
    return df['Valor'].sum()

def get_all_expenses():
    initialize_excel()
    df = pd.read_excel(EXCEL_FILE)
    return df.to_dict(orient='records')


