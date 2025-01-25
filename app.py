# App com streamlit para explorar dos dados do mercado atuarial
# Série temporal para prever os próximos 3 meses
# Por quê? Estava curioso

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from src.python.modulo.listas_filtros import *

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR  = os.path.join(BASE_DIR, 'src', 'sql')
DB_PATH  = os.path.join(DATA_DIR, 'dados.db')

@st.cache_resource
def load_db():
    engine = create_engine(f'sqlite:///{DB_PATH}')
    return engine.connect()

@st.cache_data
def load_data_geral():
    conn = load_db()
    
    with open(os.path.join(SQL_DIR, 'load_data.sql'), 'r', encoding= 'utf-8') as f:
        query = f.read()
    
    data = pd.read_sql_query(query, con = conn)
    return data

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

if __name__ == "__main__":
    st.title("Análise do mercado atuarial pós pandemia")
    conn = load_db()
    
    #Filtro lateral por região do país, UF, período da competência, raçacor, sexo, região, por tamanho de empresa
    st.sidebar.title("Filtros")
    
    # default filtros
    default_sexo = lista_filtros(SQL_DIR, conn, 'sexo')
    default_cor = lista_filtros(SQL_DIR, conn, 'raçacor')
    default_regiao = lista_filtros(SQL_DIR, conn, 'região')
    default_uf = lista_filtros(SQL_DIR, conn, 'uf')
    default_graudeinstrucao = lista_filtros(SQL_DIR, conn, 'graudeinstrução')
    default_tamanho = ['Zero','De 1 a 4','De 5 a 9','De 10 a 19','De 20 a 49','De 50 a 99','De 100 a 249','De 250 a 499','De 500 a 999','1000 ou Mais']
    default_secao = lista_filtros(SQL_DIR, conn, 'seção')
    default_subclasse = lista_filtros(SQL_DIR, conn, 'subclasse')
    default_categoria = lista_filtros(SQL_DIR, conn, 'categoria')
    default_tipomovimentacao = lista_filtros(SQL_DIR, conn, 'tipomovimentação')
    
    #Inicializar filtros na sessao
    if "sexo" not in st.session_state:
        st.session_state.sexo = default_sexo
    if "cor" not in st.session_state:
        st.session_state.cor = default_cor    
    if "regiao" not in st.session_state:
        st.session_state.regiao = default_regiao    
    if "uf" not in st.session_state:
        st.session_state.uf = default_uf    
    if "graudeinstrucao" not in st.session_state:
        st.session_state.graudeinstrucao = default_graudeinstrucao    
    if "secao" not in st.session_state:
        st.session_state.secao = default_secao    
    if "subclasse" not in st.session_state:
        st.session_state.subclasse = default_subclasse    
    if "categoria" not in st.session_state:
        st.session_state.categoria = default_categoria    
    if "tipomovimentacao" not in st.session_state:
        st.session_state.tipomovimentacao = default_tipomovimentacao
    if "tamanho" not in st.session_state:
        st.session_state.tamanho = default_tamanho
    
    if st.sidebar.button('Resetar Filtros'):
        st.session_state.sexo = default_sexo
        st.session_state.cor = default_cor
        st.session_state.regiao = default_regiao
        st.session_state.uf = default_uf
        st.session_state.graudeinstrucao = default_graudeinstrucao
        st.session_state.secao = default_secao
        st.session_state.subclasse = default_subclasse
        st.session_state.categoria = default_categoria
        st.session_state.tipomovimentacao = default_tipomovimentacao
        st.session_state.tamanho = default_tamanho
        st.rerun()
    
    #list_regioes = lista_regiao(SQL_DIR, conn)
    options_sexo            = st.sidebar.multiselect("Sexo Biológico",                  default_sexo,            default= st.session_state.sexo)
    options_cor             = st.sidebar.multiselect("raça/cor (IBGE)",                 default_cor,             default= st.session_state.cor)
    options_regiao          = st.sidebar.multiselect("Regiões",                         default_regiao,          default= st.session_state.regiao)
    options_uf              = st.sidebar.multiselect("UF",                              default_uf,              default= st.session_state.uf)
    options_graudeinstrucao = st.sidebar.multiselect("Instrução Formal",                default_graudeinstrucao, default= st.session_state.graudeinstrucao)
    options_tamanho         = st.sidebar.multiselect("Tamanho da empresa",              default_tamanho,         default= st.session_state.tamanho)
    options_secao           = st.sidebar.multiselect("Seção de atividade econômica",    default_secao,           default= st.session_state.secao)
    options_subclasse       = st.sidebar.multiselect("Subclasse de atividade econômica",default_subclasse,       default= st.session_state.subclasse)
    options_categoria       = st.sidebar.multiselect("Categoria",                       default_categoria,       default= st.session_state.categoria)
    options_mov             = st.sidebar.multiselect("Tipo de Movimentação",            default_tipomovimentacao,default= st.session_state.tipomovimentacao)

    st.session_state.sexo            = options_sexo
    st.session_state.cor             = options_cor             
    st.session_state.regiao          = options_regiao          
    st.session_state.uf              = options_uf              
    st.session_state.graudeinstrucao = options_graudeinstrucao 
    st.session_state.tamanho         = options_tamanho         
    st.session_state.secao           = options_secao           
    st.session_state.subclasse       = options_subclasse       
    st.session_state.categoria       = options_categoria       
    st.session_state.tipomovimentacao= options_mov             

    df = load_data_geral()
    
    df = df.query(f'sexo=={options_sexo} and raçacor=={options_cor} and regiao =={options_regiao} and uf =={options_uf} and graudeinstrução =={options_graudeinstrucao} and tamanho =={options_tamanho} and seção =={options_secao} and subclasse =={options_subclasse} and categoria =={options_categoria} and tipomovimentacao =={options_mov}')

    csv = df.to_csv(index=False, encoding='utf-8-sig', sep=';')
    st.download_button("Download Dados Filtrados | encoding = utf-8-sig | sep = ;", data = csv, file_name = "data.csv", mime = "text/csv")

    #Série Temporal do saldo acumulado do emprego formal
    st.subheader("Série Temporal do saldo acumulado do emprego formal")
    
    

    #Salário médio x mediano admitidos por competência por hora (dividir o salário por horas contratuais)
    #Excluir quem recebe por hora T23.Descrição ='Hora' unidadesalarariocodigo
    #Aba para ver tabela ou gráfico
    #Tabela
    #Gráfico

    #Salário médio x mediano demitidos por competência por hora (dividir o salário por horas contratuais)
    #Aba para ver tabela ou gráfico
    #Tabela
    #Gráfico

    #Idade média x mediana admitidos por competência por hora (dividir o salário por horas contratuais)
    #Aba para ver tabela ou gráfico
    #Tabela
    #Gráfico

    #Idade média x mediana demitidos por competência por hora (dividir o salário por horas contratuais)
    #Aba para ver tabela ou gráfico
    #Tabela
    #Gráfico

    #Por região do país e região

    #Sazonalidade do emprego

    #Ganho real nos salários ou perda pela inflação

    # tipoestabelecimento

    # tipoempregador

    # graudeinstrução
    
    #por tamanho de empresa
    
    
    