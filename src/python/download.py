# [OK] vê as competências faltantes e baixa as mais novas
# [OK] sql no banco para determinar as competências que existem
# [OK] verificar competência da última e o dia atual

import ftplib
import os
import py7zr
import pandas as pd
from sqlalchemy import create_engine
import logging
import sqlite3
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname((__file__)))))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR  = os.path.join(BASE_DIR, 'src', 'sql')

# Configurações do FTP
FTP_HOST = 'ftp.mtps.gov.br'
FTP_BASE_PATH = 'pdet/microdados/NOVO CAGED/{ano}/{ano}{mes}/'
LOCAL_FILE_DIR  = TEMP_DIR
DB_PATH = os.path.join(DATA_DIR, 'dados.db')
TABLE_NAME = 'CAGEDMOV'

# Criar diretório de downloads se não existir
os.makedirs(LOCAL_FILE_DIR, exist_ok=True)

# Configuração do logging
log_file = 'processamento.log'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'  # Modo de abertura: 'a' para anexar ao arquivo de log
)

def log_and_print(message, level='INFO'):
    """Função para registrar a mensagem no log e também exibir no console."""
    if level == 'INFO':
        logging.info(message)
        print(message)
    elif level == 'ERROR':
        logging.error(message)
        print(message)
    elif level == 'WARNING':
        logging.warning(message)
        print(message)

def download_file_from_ftp(ano, mes):
    """Baixa o arquivo .7z que contém 'CAGEDMOV' do servidor FTP para o ano e mês especificados."""
    ftp_path = FTP_BASE_PATH.format(ano=ano, mes=f'{mes}')
    local_file_path = os.path.join(LOCAL_FILE_DIR, f'CAGED_{ano}_{mes}.7z')
    
    try:
        with ftplib.FTP(FTP_HOST) as ftp:
            ftp.login()
            ftp.cwd(ftp_path)
            files = ftp.nlst()
            
            # Filtrar apenas arquivos .7z que contenham "CAGEDMOV" no nome
            cagedmov_files = [file for file in files if file.endswith('.7z') and 'CAGEDMOV' in file.upper()]
            
            if not cagedmov_files:
                raise FileNotFoundError(f"Nenhum arquivo contendo 'CAGEDMOV' encontrado em {ftp_path}")
            
            # Baixa o primeiro arquivo correspondente
            file = cagedmov_files[0]
            with open(local_file_path, 'wb') as local_file:
                ftp.retrbinary(f'RETR {file}', local_file.write)
            log_and_print(f"Arquivo {file} baixado com sucesso.")
            return local_file_path
    except Exception as e:
        log_and_print(f"Erro ao baixar arquivo de {ano}/{mes}: {e}")
        return None
    
def extract_7z_file(file_path):
    """Extrai o arquivo .txt do arquivo .7z baixado."""
    try:
        with py7zr.SevenZipFile(file_path, mode='r') as archive:
            archive.extractall(LOCAL_FILE_DIR)
            extracted_files = archive.getnames()
        
        # Verificar se há arquivos .txt extraídos
        for file in extracted_files:
            if file.endswith('.txt'):
                extracted_file_path = os.path.join(LOCAL_FILE_DIR, file)
                log_and_print(f"Arquivo {file} extraído para {extracted_file_path}")
                return extracted_file_path
        raise FileNotFoundError("Nenhum arquivo .txt encontrado no .7z extraído.")
    except Exception as e:
        log_and_print(f"Erro ao extrair {file_path}: {e}")
        return None

def process_txt_and_save_to_db(file_path):
    """Lê o arquivo .txt e salva os dados em um banco SQLite."""
    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')  # Ajuste o separador conforme necessário
        df.columns = df.columns.str.strip().str.lower()
        
        if 'cbo2002ocupação' not in df.columns:
            raise KeyError(f"Coluna 'cbo2002ocupação' não encontrada no arquivo {file_path}. Colunas disponíveis: {df.columns.tolist()}")      
        
        df = df.query("cbo2002ocupação == 211105")
        
        if df.empty:
            log_and_print(f"Nenhum registro encontrado com cbo2002ocupacao=211105 no arquivo {file_path}.")
            return        
        
        db_directory = os.path.dirname(DB_PATH)
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)
        engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)
        
        df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
        log_and_print(f"Dados do arquivo {file_path} salvos na tabela '{TABLE_NAME}' do banco de dados SQLite.")
    except Exception as e:
        log_and_print(f"Erro ao processar {file_path}: {e}")

def cleanup_files(*files):
    """Remove arquivos locais após o processamento."""
    for file in files:
        if file and os.path.exists(file):
            os.remove(file)
            log_and_print(f"Arquivo {file} removido com sucesso.")
            
def get_competencias_processadas():
    # Conectar ao banco de dados SQLite e executar a consulta
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Consulta SQL que retorna as competências já processadas
    cursor.execute("select competênciamov from CAGEDMOV group by competênciamov")
    competencias_processadas = [row[0] for row in cursor.fetchall()]

    conn.close()
    return competencias_processadas            

def main(ano, mes):
    log_and_print(f"Processando {ano}/{mes}...")
    zip_file = None
    txt_file = None

    try:
        zip_file = download_file_from_ftp(ano, mes)
        txt_file = extract_7z_file(zip_file)
        process_txt_and_save_to_db(txt_file)
        
    except Exception as e:
        log_and_print(f"Erro durante o processamento de {ano}/{mes}: {e}")
    
    finally:
        # Garantir a remoção dos arquivos, independentemente do sucesso
        cleanup_files(zip_file, txt_file)
    
    log_and_print("Processo concluído.")

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
        mes = int(competencia) % 100  # Extrai o mês
        mes = f'{mes:02d}'
        main(ano, mes)