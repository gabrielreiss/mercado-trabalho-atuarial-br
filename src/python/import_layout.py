# Coloque o excel do layout na pasta data e rode o código

import pandas as pd
import os
from sqlalchemy import create_engine

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname((__file__)))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH  = os.path.join(DATA_DIR, 'dados.db')
EXCEL_FILE = os.path.join(DATA_DIR, 'Layout.xlsx')

xls = pd.ExcelFile(EXCEL_FILE)
engine = create_engine(f'sqlite:///{DB_PATH}')

for sheet_name in xls.sheet_names[1:]:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    df.to_sql(sheet_name, con = engine, if_exists='replace', index=False)
    print(f"Tabela '{sheet_name}' adicionada ao banco de dados.")

engine.dispose()
