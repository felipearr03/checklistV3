from pathlib import Path
from datetime import date, datetime, timedelta
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide")

pasta_atual = Path(__file__).parent.parent.parent.parent

logo_path = r"\\10.0.8.50\Setores\Central de Serviços\Fiscal\FELIPE ANDRADE ROCHA\DELLYS_LOGO-removebg-preview.png"
logo = Image.open(logo_path)
st.sidebar.image(logo, width=200)

caminho_arquivo = r"\\10.0.8.50\Setores\Central de Serviços\Fiscal\FELIPE ANDRADE ROCHA\TESTE\1.1 CHECK LIST - Declarações Estaduais Dellys 2024.xlsx"
caminho_arquivo_secundario = r"\\10.0.8.50\Setores\Central de Serviços\Fiscal\FELIPE ANDRADE ROCHA\TESTE\1.3 CHECK LIST - Fechamento ICMS Dellys 2024.xlsx"

df_fechamento = pd.read_excel(caminho_arquivo, sheet_name=None, parse_dates=True)
df_fechamentoV2 = pd.read_excel(caminho_arquivo_secundario, sheet_name=None, parse_dates=True)

aba_selecionada = st.sidebar.selectbox('Selecione o mês - Obrigação Acessória:', list(df_fechamento.keys()))
df_aba_selecionada = df_fechamento[aba_selecionada]

col11, col12, col13 = st.columns([0.5, 0.25, 0.25])
col11.markdown('## Visão Geral - Metas dos Analistas: Obrigações Acessórias')
col13.metric('Período:', aba_selecionada)
st.divider()

# Verificar se as colunas esperadas estão presentes
colunas_esperadas = ['ENTREGUE POR', 'PRAZO', 'ENTREGA']

if set(colunas_esperadas).issubset(df_aba_selecionada.columns):
    # Preencher células vazias nas colunas 'PRAZO' e 'ENTREGA' com valores de outras colunas
    df_aba_selecionada['PRAZO'] = df_aba_selecionada['PRAZO'].combine_first(df_aba_selecionada['VALORX'])
    df_aba_selecionada['ENTREGA'] = df_aba_selecionada['ENTREGA'].combine_first(df_aba_selecionada['VALORY'])

    # Converter as colunas 'PRAZO' e 'ENTREGA' para datetime se não estiverem no formato adequado
    df_aba_selecionada['PRAZO'] = pd.to_datetime(df_aba_selecionada['PRAZO'], errors='coerce')
    df_aba_selecionada['ENTREGA'] = pd.to_datetime(df_aba_selecionada['ENTREGA'], errors='coerce')

    # Criar coluna "Dias_Diferenca" baseado nas condições dadas
    df_aba_selecionada['Dias_Diferenca'] = (df_aba_selecionada['PRAZO'] - df_aba_selecionada['ENTREGA']).dt.days

    # Criar a coluna "Status" usando as condições fornecidas
    df_aba_selecionada['Status'] = pd.cut(df_aba_selecionada['Dias_Diferenca'],
                                      bins=[-float('inf'), -1, 1, float('inf')],
                                      labels=['Atrasado', 'No Prazo', 'Antecipado'])

    # Filtrar para incluir apenas as colunas necessárias
    df_tabela_dinamica = df_aba_selecionada[['ENTREGUE POR', 'Status']]

    # Criar a tabela dinâmica
    tabela_dinamica = pd.pivot_table(df_tabela_dinamica, 
                                      values='ENTREGUE POR', 
                                      index=['ENTREGUE POR'], 
                                      columns='Status', 
                                      aggfunc='size',  
                                      fill_value=0)

    # Adicionar coluna para calcular a meta com base nas condições dadas
    tabela_dinamica['Meta'] = 0  # Inicializa todas as entradas com 0

    # Atualiza as entradas conforme as condições
    tabela_dinamica.loc[tabela_dinamica['Atrasado'] > 0, 'Meta'] = '80%'
    tabela_dinamica.loc[(tabela_dinamica['Atrasado'] == 0) & (tabela_dinamica['No Prazo'] > 0), 'Meta'] = '100%'
    tabela_dinamica.loc[(tabela_dinamica['Atrasado'] == 0) & (tabela_dinamica['No Prazo'] == 0) & (tabela_dinamica['Antecipado'] > 0), 'Meta'] = '120%'

    # Exibir a tabela dinâmica,=
    st.write("##### Metas Por Analista - Obrigações Acessórias:")
    ##st.write(tabela_dinamica)

    fig = px.bar(tabela_dinamica, x=tabela_dinamica.index, y='Meta', title='Metas dos Analistas - Obrigações acessórias')
    fig.update_layout(xaxis_title='Analista', yaxis_title='Meta', barmode='group')
    ##st.plotly_chart(fig)

col17, col18 = st.columns([0.25, 0.30])
col17.write(tabela_dinamica)
col18.plotly_chart(fig) 
st.divider()

# # # # # # FECHAMENTO
aba_selecionadaV2 = st.sidebar.selectbox('Selecione o mês - Apuração Fiscal:', list(df_fechamentoV2.keys()))
df_aba_selecionadaV2 = df_fechamentoV2[aba_selecionadaV2]

col155, col156, col157 = st.columns([0.5, 0.25, 0.25])
col155.markdown('## Visão Geral - Metas dos Analistas: Fechamento Fiscal')
col157.metric('Período:', aba_selecionadaV2)

colunas_esperadasV2 = ['RESPONSÁVEL', 'PRAZO', 'DATA']

# Combine todos os DataFrames do dicionário
#df_concatenadoV2 = pd.concat(df_fechamentoV2.values(), ignore_index=True)

if set(colunas_esperadasV2).issubset(df_aba_selecionadaV2.columns):
    # Converter as colunas 'PRAZO' e 'DATA' para o tipo datetime
    df_aba_selecionadaV2['PRAZO'] = df_aba_selecionadaV2['PRAZO'].combine_first(df_aba_selecionadaV2['VALORX'])
    df_aba_selecionadaV2['DATA'] = df_aba_selecionadaV2['DATA'].combine_first(df_aba_selecionadaV2['VALORY'])

    df_aba_selecionadaV2['PRAZO'] = pd.to_datetime(df_aba_selecionadaV2['PRAZO'], errors='coerce')
    df_aba_selecionadaV2['DATA'] = pd.to_datetime(df_aba_selecionadaV2['DATA'], errors='coerce')

    # Criar coluna "Status" baseado nas condições dadas
    df_aba_selecionadaV2['Dias_Diferenca'] = (df_aba_selecionadaV2['PRAZO'] - df_aba_selecionadaV2['DATA']).dt.days

    # Criar a coluna "Status" usando as condições fornecidas
    df_aba_selecionadaV2['STATUS'] = pd.cut(df_aba_selecionadaV2['Dias_Diferenca'],
                                      bins=[-float('inf'), -1, 1, float('inf')],
                                      labels=['Atrasado', 'No Prazo', 'Antecipado'])

    # Filtrar para incluir apenas as colunas necessárias
    df_tabela_dinamicaV2 = df_aba_selecionadaV2[['RESPONSÁVEL', 'STATUS']]

    # Criar a tabela dinâmica
    # Criar a tabela dinâmica
    tabela_dinamicaV2 = pd.pivot_table(df_tabela_dinamicaV2, 
                                    values='RESPONSÁVEL', 
                                    index=['RESPONSÁVEL'], 
                                    columns='STATUS', 
                                    aggfunc='size',  
                                    fill_value=0)

    # Adicionar coluna para calcular a meta com base nas condições dadas
    tabela_dinamicaV2['Meta'] = 0  # Inicializa todas as entradas com 0

    # Atualizar as entradas conforme as condições
    tabela_dinamicaV2.loc[tabela_dinamicaV2['Atrasado'] > 0, 'Meta'] = '80%'
    tabela_dinamicaV2.loc[tabela_dinamicaV2['No Prazo'] > 0, 'Meta'] = '100%'
    tabela_dinamicaV2.loc[tabela_dinamicaV2['Antecipado'] > 0, 'Meta'] = '120%'

    figV2 = px.bar(tabela_dinamicaV2, x=tabela_dinamicaV2.index, y='Meta', title='Metas dos Analistas - Fechamento Fiscal')
    figV2.update_layout(xaxis_title='Analista', yaxis_title='Meta', barmode='group')

col171, col182 = st.columns([0.25, 0.30])
col171.write(tabela_dinamicaV2)
col182.plotly_chart(figV2) 
st.divider()

## ## ## ## ## ## ## ## ## ## ## ## 
aba_selecionadaV3 = st.sidebar.selectbox('Selecione o mês - Abertura Contábil:', list(df_fechamentoV2.keys()))
df_aba_selecionadaV3 = df_fechamentoV2[aba_selecionadaV3]

col111, col112, col13 = st.columns([0.5, 0.25, 0.25])
col111.markdown('## Visão Geral - Meta dos Analistas: Abertura Período Contábil:')
col13.metric('Período:', aba_selecionadaV3)

colunas_esperadasV3 = ['RESPONSÁVEL', 'ABERTURA CONTÁBIL']

if set(colunas_esperadasV3).issubset(df_aba_selecionadaV3.columns):
    # Filtrar para incluir apenas as colunas necessárias
    df_aba_selecionadaV3 = df_aba_selecionadaV3[['RESPONSÁVEL', 'ABERTURA CONTÁBIL']]

    # Criar a tabela dinâmica para a coluna 'ABERTURA CONTÁBIL'
    df_aba_selecionadaV3 = pd.pivot_table(df_aba_selecionadaV3, 
                                               values='ABERTURA CONTÁBIL', 
                                               index=['RESPONSÁVEL'], 
                                               aggfunc='sum',  
                                               fill_value=0)
    
    df_tabela_dinamicaV3 = df_aba_selecionadaV3

    df_tabela_dinamicaV3['Meta'] = '0%'

    # Atualizar as entradas conforme as condições
    df_tabela_dinamicaV3.loc[df_tabela_dinamicaV3['ABERTURA CONTÁBIL'] >= 2, 'Meta'] = '80%'
    df_tabela_dinamicaV3.loc[df_tabela_dinamicaV3['ABERTURA CONTÁBIL'] == 1, 'Meta'] = '100%'
    df_tabela_dinamicaV3.loc[df_tabela_dinamicaV3['ABERTURA CONTÁBIL'] == 0, 'Meta'] = '120%'

figV3 = px.bar(df_tabela_dinamicaV3, x=df_tabela_dinamicaV3.index, y='Meta', title='Metas dos Analistas - Abertura Contábil')
figV3.update_layout(xaxis_title='Analista', yaxis_title='Meta', barmode='group')
    # Exibir a tabela dinâmica para 'ABERTURA CONTÁBIL'

col199, col191 = st.columns([0.25, 0.30])
col199.write(df_tabela_dinamicaV3)
col191.plotly_chart(figV3)

st.divider()

st.sidebar.markdown('###### Desevolvido por: Felipe Rocha')
