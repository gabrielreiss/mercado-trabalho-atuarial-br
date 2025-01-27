# App com streamlit para explorar dos dados do mercado atuarial
# Série temporal para prever os próximos 3 meses
# Por quê? Estava curioso

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import plotly.express as px
import numpy as np
from src.python.modulo.listas_filtros import *
from datetime import timedelta

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
    st.write("Criado por: Gabriel Reiss de Castro MIBA 4120 https://www.linkedin.com/in/gabrielreissdecastro/")
    st.write("Os dados foram obtidos do Novo Caged, baixados do servidor FTP do MTPS: ftp://ftp.mtps.gov.br/pdet/microdados/. Os dados foram filtrados pelo CBO 211105 Atuário, foram realizados algumas limpezas sobre alguns dados divergentes e podem ser baixados no botão abaixo.")
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

    if df.empty:
        st.write("Sem dados com esses filtros")
    else:
        #Organizar os dados
        df['competencia'] = pd.to_datetime(df['competencia'].astype(str), format='%Y%m')
        df['salario'] = df['salario'].str.replace(',', '.').astype(float)
        
        df['competencia2'] = df['competencia'].dt.to_period('M')
        competencia_min = df['competencia'].min()
        competencia_max = df['competencia'].max()
        
        competencia = st.slider(
            "Selecione um intervalo de meses",
            min_value=competencia_min.date(),
            max_value=competencia_max.date(),
            value=(competencia_min.date(), competencia_max.date()),
            format="YYYY-MM"
        )

        df = df[(df['competencia2'] >= pd.Period(competencia[0], 'M')) & (df['competencia2'] <= pd.Period(competencia[1], 'M'))]
        
        csv = df.to_csv(index=False, encoding='utf-8-sig', sep=';')
        st.download_button("Download Dados Filtrados | encoding = utf-8-sig | sep = ;", data = csv, file_name = "data.csv", mime = "text/csv")
        del(csv)
        admitidos = df.query('saldomovimentacao == 1')
        demissoes = df.query('saldomovimentacao == -1')      
        
        st.subheader("Resumo do período:")
        # x admissões no período, x demissões no período, saldo de x
        
        st.write(f'{len(admitidos)} admissões | {len(demissoes)} demissões | saldo: {len(admitidos) - len(demissoes)}')
        
        #Série Temporal do saldo acumulado do emprego formal
        st.subheader("Movimentações do emprego formal em Atuária")
        #Colocar o saldo dos últimos 12 meses, 6 meses e 3 meses
        
        
        df_admitidos_mensal = admitidos.resample('ME', on='competencia')['saldomovimentacao'].sum().reset_index()
        df_demissoes_mensal = demissoes.resample('ME', on='competencia')['saldomovimentacao'].sum().reset_index()
        df_saldo_mensal = df.resample('ME', on='competencia')['saldomovimentacao'].sum().reset_index()

        guias_titulo = ["Saldo", "Admitidos e Demitidos"]
        guia_saldo, guia_ad = st.tabs(guias_titulo)
        
        with guia_saldo:
            #Série temporal do saldo
            df_saldo_mensal['cor'] = df_saldo_mensal['saldomovimentacao'].apply(lambda x: 'positivo' if x > 0 else 'negativo')
            fig = px.bar(x=df_saldo_mensal['competencia'], y=df_saldo_mensal['saldomovimentacao'], color = df_saldo_mensal['cor'], color_discrete_map={'positivo': 'green', 'negativo': 'red'})
            
            fig.update_layout(
                title="Saldo do emprego formal em atuária",
                xaxis_title="Mês",
                yaxis_title="Saldo",
                barmode ='stack'
            )
            st.plotly_chart(fig)
        
        with guia_ad:
            #Admissões e demissões individuais
            fig = px.bar()
            #fig.add_scatter(x=df_admitidos_mensal['competencia'], y=df_admitidos_mensal['saldomovimentacao'], mode='lines', name='Admissões')
            #fig.add_scatter(x=df_demissoes_mensal['competencia'], y=df_demissoes_mensal['saldomovimentacao'], mode='lines', name='Demissões')
            fig.add_bar(x=df_admitidos_mensal['competencia'], y=df_admitidos_mensal['saldomovimentacao'], name='Admissões', marker_color = 'green')
            fig.add_bar(x=df_demissoes_mensal['competencia'], y=df_demissoes_mensal['saldomovimentacao'], name='Demissões', marker_color = 'red')

            fig.update_layout(
                title="Admitidos e Demitidos em atuária",
                xaxis_title="Mês",
                yaxis_title="Quantidade"
            )
            st.plotly_chart(fig)
        del(df_admitidos_mensal);del(df_demissoes_mensal);del(df_saldo_mensal);#del(admitidos);del(demissoes)


        #Salário médio x mediano admitidos por competência por hora (dividir o salário por horas contratuais)
        #Salário médio x mediano demitidos por competência por hora (dividir o salário por horas contratuais)
        #Excluir quem recebe por hora T23.Descrição ='Hora' unidadesalarariocodigo OK
        st.subheader("Salário médio x mediano admitidos por competência por hora")
        sal_admitidos = df.query('unidadesalarariocodigo == "Mês" and saldomovimentacao == 1')
        
        a_media = sal_admitidos[sal_admitidos['competencia'] > sal_admitidos['competencia'].max() - pd.DateOffset(months=12)]['salario'].mean()
        a_mediana = sal_admitidos[sal_admitidos['competencia'] > sal_admitidos['competencia'].max() - pd.DateOffset(months=12)]['salario'].median()
        st.write(f'O salário médio dos admitidos dos últimos 12 meses foi: {a_media:.2f} e a mediana foi {a_mediana:.2f}')
        
        sal_demitidos = df.query('unidadesalarariocodigo == "Mês" and saldomovimentacao == -1')
        d_media = sal_demitidos[sal_demitidos['competencia'] > sal_demitidos['competencia'].max() - pd.DateOffset(months=12)]['salario'].mean()
        d_mediana = sal_demitidos[sal_demitidos['competencia'] > sal_demitidos['competencia'].max() - pd.DateOffset(months=12)]['salario'].median()
        st.write(f'O salário médio dos demitidos dos últimos 12 meses foi: {d_media:.2f} e a mediana foi {d_mediana:.2f}')
        st.write(f'Os admitidos receberam um salário médio {((a_media / d_media - 1) * 100):.2f}% em relação aos demitidos')
        st.write(f'Os admitidos receberam um salário mediano {((a_mediana / d_mediana - 1) * 100):.2f}% em relação aos demitidos')
        del(d_media);del(d_mediana);del(a_media);del(a_mediana)
        
        guias_titulo = ["Admitidos", "Demitidos"]
        guia_ad, guia_de = st.tabs(guias_titulo)
        
        with guia_ad:
            #Boxplot dos salários por competência admitidos
            fig = px.box(sal_admitidos,
                        x='competencia',
                        y='salario',
                        title='Boxplot dos salários dos admitidos por competência'
            )
            st.plotly_chart(fig)
            #['salario', 'horascontratuais', 'idade', 'graudeinstrução', 'subclasse', 'uf', 'regiao', 'competencia']
        
        with guia_de:
            #Boxplot dos salários por competência demitidos
            fig = px.box(sal_demitidos,
                        x='competencia',
                        y='salario',
                        title="Boxplot dos salários dos demitidos por competência"
            )
            st.plotly_chart(fig)
        #del(sal_admitidos)
        #del(sal_demitidos)
        
        
        #boxplot da escolaridade
        #df_escolaridade = df.query('unidadesalarariocodigo == "Mês"')
        st.subheader("Salários por escolaridade")
        guias_titulo = ["Admitidos", "Demitidos"]
        guia_ad, guia_de = st.tabs(guias_titulo)
        
        ordem_escolaridade = ['Médio Completo','Superior Incompleto','Superior Completo','Pós-Graduação completa','Mestrado','Doutorado']
        
        with guia_ad:
            fig = px.box(sal_admitidos,
                    x='graudeinstrução',
                    y='salario',
                    title="Boxplot dos salários por escolaridade admitidos",
                    category_orders={'graudeinstrução': ordem_escolaridade}
            )
            st.plotly_chart(fig)
            st.write("Observando os dados até novembro de 2024, mostravam que ter pós graduação ou mestrado têm uma mediana superior em relação ao superior completo.")

        with guia_de:
            fig = px.box(sal_demitidos,
                    x='graudeinstrução',
                    y='salario',
                    title="Boxplot dos salários por escolaridade demitidos",
                    category_orders={'graudeinstrução': ordem_escolaridade}
            )
            st.plotly_chart(fig)


        #Idade média x mediana admitidos por competência por hora (dividir o salário por horas contratuais)
        st.subheader("Por idade")
        guias_titulo = ["Idade Admitidos", "Idade Demitido", "Salários Admitidos", "Salários Demitidos"]
        guia_idade_a, guia_idade_d, guia_ad, guia_de = st.tabs(guias_titulo)
        
        with guia_idade_a:
            fig = px.box(sal_admitidos,
            x='competencia',
            y='idade',
            title="Boxplot de idade admitidos por competência",
            category_orders={'graudeinstrução': ordem_escolaridade}
            )
            st.plotly_chart(fig)        
        
        with guia_idade_d:
            fig = px.box(sal_demitidos,
            x='competencia',
            y='idade',
            title="Boxplot de idade demitidos por competência",
            category_orders={'graudeinstrução': ordem_escolaridade}
            )
            st.plotly_chart(fig)     
                    
        with guia_ad:
            fig = px.box(sal_admitidos,
            x='idade',
            y='salario',
            title="Boxplot dos salários por idade admitidos",
            category_orders={'graudeinstrução': ordem_escolaridade}
            )
            st.plotly_chart(fig)
        
        with guia_de:
            fig = px.box(sal_demitidos,
            x='idade',
            y='salario',
            title="Boxplot dos salários por idade demitidos",
            category_orders={'graudeinstrução': ordem_escolaridade}
            )
            st.plotly_chart(fig)

        #Por região do país e região
        st.subheader("Por Região ou Cidade")
        groupby_regiao = df.groupby('regiao').size().sort_values(ascending=False); ordem_regiao = groupby_regiao.index.tolist(); del(groupby_regiao)
        groupby_municipio = df.groupby('municipio').size().sort_values(ascending=False); ordem_municipio = groupby_municipio.index.tolist(); del(groupby_municipio)
        guias_titulo = ["Mapa Movimento","Movimento por Região", "Movimento por Cidade"]
        guia_mapa, guia_regiao, guia_municipio = st.tabs(guias_titulo)
                
        with guia_regiao:
            fig = px.bar()
            fig.add_bar(x=sal_admitidos['regiao'], y=sal_admitidos['saldomovimentacao'], name='Admissões', marker_color = 'green')
            fig.add_bar(x=sal_demitidos['regiao'], y=sal_demitidos['saldomovimentacao'], name='Demissões', marker_color = 'red')

            fig.update_layout(
                title="Admitidos e Demitidos em atuária",
                xaxis_title="Mês",
                yaxis_title="Quantidade",
                xaxis={'categoryorder': 'array', 'categoryarray': ordem_regiao}
            )
            st.plotly_chart(fig)
              
        with guia_municipio:
            fig = px.bar()
            fig.add_bar(x=sal_admitidos['municipio'], y=sal_admitidos['saldomovimentacao'], name='Admissões', marker_color = 'green')
            fig.add_bar(x=sal_demitidos['municipio'], y=sal_demitidos['saldomovimentacao'], name='Demissões', marker_color = 'red')

            fig.update_layout(
                title="Admitidos e Demitidos em atuária",
                xaxis_title="Mês",
                yaxis_title="Quantidade",
                xaxis={'categoryorder': 'array', 'categoryarray': ordem_municipio}
            )
            st.plotly_chart(fig)
          
        with guia_mapa:
            df_mapa = admitidos.groupby(by='uf')['saldomovimentacao'].sum().reset_index()
            
            estado_para_sigla = {
                "Acre": "AC",
                "Alagoas": "AL",
                "Amapá": "AP",
                "Amazonas": "AM",
                "Bahia": "BA",
                "Ceará": "CE",
                "Distrito Federal": "DF",
                "Espírito Santo": "ES",
                "Goiás": "GO",
                "Maranhão": "MA",
                "Mato Grosso": "MT",
                "Mato Grosso do Sul": "MS",
                "Minas gerais": "MG",
                "Pará": "PA",
                "Paraíba": "PB",
                "Paraná": "PR",
                "Pernambuco": "PE",
                "Piauí": "PI",
                "Rio de Janeiro": "RJ",
                "Rio Grande do Norte": "RN",
                "Rio Grande do Sul": "RS",
                "Rondônia": "RO",
                "Roraima": "RR",
                "Santa Catarina": "SC",
                "São Paulo": "SP",
                "Sergipe": "SE",
                "Tocantins": "TO"
            }
            
            coordenadas_estados = {
                "Acre": {"latitude": -9.0238, "longitude": -70.8120},
                "Alagoas": {"latitude": -9.5713, "longitude": -36.7820},
                "Amapá": {"latitude": 0.9020, "longitude": -52.0030},
                "Amazonas": {"latitude": -3.4168, "longitude": -65.8561},
                "Bahia": {"latitude": -12.5797, "longitude": -41.7007},
                "Ceará": {"latitude": -5.4984, "longitude": -39.3206},
                "Distrito Federal": {"latitude": -15.7998, "longitude": -47.8645},
                "Espírito Santo": {"latitude": -19.1834, "longitude": -40.3089},
                "Goiás": {"latitude": -15.8270, "longitude": -49.8362},
                "Maranhão": {"latitude": -5.4200, "longitude": -45.4321},
                "Mato Grosso": {"latitude": -12.6819, "longitude": -56.9211},
                "Mato Grosso do Sul": {"latitude": -20.7722, "longitude": -54.7852},
                "Minas gerais": {"latitude": -18.5122, "longitude": -44.5550},
                "Pará": {"latitude": -3.4168, "longitude": -52.9296},
                "Paraíba": {"latitude": -7.2399, "longitude": -36.7819},
                "Paraná": {"latitude": -25.2521, "longitude": -52.0215},
                "Pernambuco": {"latitude": -8.8137, "longitude": -36.9541},
                "Piauí": {"latitude": -7.7183, "longitude": -42.7289},
                "Rio de Janeiro": {"latitude": -22.9083, "longitude": -43.1964},
                "Rio Grande do Norte": {"latitude": -5.7945, "longitude": -36.9541},
                "Rio Grande do Sul": {"latitude": -30.0346, "longitude": -51.2177},
                "Rondônia": {"latitude": -10.9472, "longitude": -62.8278},
                "Roraima": {"latitude": 2.7376, "longitude": -61.3419},
                "Santa Catarina": {"latitude": -27.5954, "longitude": -48.5480},
                "São Paulo": {"latitude": -23.5505, "longitude": -46.6333},
                "Sergipe": {"latitude": -10.5741, "longitude": -37.3857},
                "Tocantins": {"latitude": -10.1753, "longitude": -48.2982}
            }
                
            df_mapa['uf_sigla'] = df_mapa['uf'].map(estado_para_sigla)
            df_mapa['latitude'] = df_mapa['uf'].map(lambda x: coordenadas_estados[x]['latitude'])
            df_mapa['longitude'] = df_mapa['uf'].map(lambda x: coordenadas_estados[x]['longitude'])
            
            df_mapa['color'] = df_mapa['saldomovimentacao'].apply(lambda x: 'Negativo' if x < 0 else 'Positivo')
            df_mapa['size'] = df_mapa['saldomovimentacao'].abs() * 1
            
            fig = px.scatter_mapbox(
                df_mapa,
                lat="latitude",
                lon="longitude",
                size=df_mapa["saldomovimentacao"].abs(),
                color='color',
                hover_name="uf",
                hover_data=["saldomovimentacao"],
                zoom=3,
                size_max=50,
                color_discrete_map={"Negativo": "red", "Positivo": "green"}
            )

            fig.update_layout(
                mapbox_style="open-street-map",
                title="Saldo de Movimentação por Estado",
                margin={"r":0,"t":0,"l":0,"b":0}
            )

            st.plotly_chart(fig)
            
        #Salário por região
        guias_titulo = ["Mapa Salário Mediano", "Salário por Região", "Salários por Município"]
        guia_mapa, guia_regiao_salario, guia_municipio_salario = st.tabs(guias_titulo)
            
        with guia_regiao_salario:
            fig = px.box(sal_admitidos,
            x='regiao',
            y='salario',
            title="Boxplot dos salários por idade admitidos")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': ordem_regiao})
            st.plotly_chart(fig)
        
        with guia_municipio_salario:
            fig = px.box(sal_admitidos,
            x='municipio',
            y='salario',
            title="Boxplot dos salários por idade admitidos")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': ordem_municipio})
            st.plotly_chart(fig)
        
        with guia_mapa:
            df_mapa = admitidos.groupby(by='uf')['salario'].median().reset_index()
            df_mapa['uf_sigla'] = df_mapa['uf'].map(estado_para_sigla)
            df_mapa['latitude'] = df_mapa['uf'].map(lambda x: coordenadas_estados[x]['latitude'])
            df_mapa['longitude'] = df_mapa['uf'].map(lambda x: coordenadas_estados[x]['longitude'])
            df_mapa['size'] = df_mapa['salario'].abs() * 1
            
            fig = px.scatter_mapbox(
                df_mapa,
                lat="latitude",
                lon="longitude",
                size=df_mapa["salario"].abs(),
                hover_name="uf",
                hover_data=["salario"],
                zoom=3,
                size_max=50
            )

            fig.update_layout(
                mapbox_style="open-street-map",
                title="Mediana dos Salários por Estado",
                margin={"r":0,"t":0,"l":0,"b":0}
            )

            st.plotly_chart(fig)

        #Sazonalidade do emprego usando modelo linear colocando cada mês como uma variável dummy, verificar se existe um mês com o p-valor < 0,05

        #Ganho real nos salários ou perda pela inflação

        # tipoestabelecimento

        # tipoempregador

        # graudeinstrução

        #por tamanho de empresa
    
    st.write("Criado por: Gabriel Reiss de Castro MIBA 4120 https://www.linkedin.com/in/gabrielreissdecastro/")
    