import os
from datetime import datetime
import sqlite3

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname((__file__)))))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR  = os.path.join(BASE_DIR, 'src', 'sql')
DB_PATH = os.path.join(DATA_DIR, 'dados.db')

def get_competencias_processadas():
    # Conectar ao banco de dados SQLite e executar a consulta
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Consulta SQL que retorna as competências já processadas
    cursor.execute("select competênciamov from CAGEDMOV group by competênciamov")
    competencias_processadas = [row[0] for row in cursor.fetchall()]

    conn.close()
    return competencias_processadas

if __name__ == "__main__":       
    # Obtendo o ano e mês atual
    ano_atual = datetime.now().year
    mes_atual = datetime.now().month   
       
    competencias_a_processar = [
    f"{ano:04d}{mes:02d}" 
    for ano in range(2020, ano_atual + 1) 
    for mes in range(1, 13)
    if (ano < ano_atual or (ano == ano_atual and mes <= mes_atual))
    ]
        
    # Obtém as competências que já foram processadas
    competencias_processadas = get_competencias_processadas()
    competencias_processadas = [str(x) for x in competencias_processadas]

    # Filtra as competências que ainda não foram processadas
    competencias_nao_processadas = [
        competencia for competencia in competencias_a_processar
        if competencia not in competencias_processadas
    ]

 # Processa apenas as competências não processadas
    for competencia in competencias_nao_processadas:
        ano = str(int(competencia) // 100)  # Extrai o ano
        mes = str(int(competencia) % 100)  # Extrai o mês
        #print(f'{ano}{mes}')

    print(competencias_nao_processadas)