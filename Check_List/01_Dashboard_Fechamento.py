from pathlib import Path
from datetime import date, datetime, timedelta
import pandas as pd
import streamlit as st 
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide")

# Indicando onde o arquivo de excel está salvo
pasta_atual = Path(__file__).parent.parent.parent
caminho_arquivo = r"\\10.0.8.50\Setores\Central de Serviços\Fiscal\FELIPE ANDRADE ROCHA\TESTE\1.3 CHECK LIST - Fechamento ICMS Dellys 2024.xlsx"

# Fazendo a leitura do arquivo Excel
df_fechamento = pd.read_excel(caminho_arquivo, sheet_name=None, parse_dates=True)

logo_path = r"\\10.0.8.50\Setores\Central de Serviços\Fiscal\FELIPE ANDRADE ROCHA\DELLYS_LOGO-removebg-preview.png"  # Substitua pelo caminho do seu arquivo de imagem
logo = Image.open(logo_path)
st.sidebar.image(logo, width=200)

mes_selecionado = st.sidebar.selectbox('Selecione o Mês:', df_fechamento.keys())
opcoes_filiais = ['Todas as Filiais'] + list(df_fechamento[mes_selecionado]['FILIAL'].unique())
filial_selecionada = st.sidebar.selectbox('Selecione a Filial:', opcoes_filiais)

if filial_selecionada == 'Todas as Filiais':
    df_filial_selecionada = df_fechamento[mes_selecionado]
else:
    df_filial_selecionada = df_fechamento[mes_selecionado][df_fechamento[mes_selecionado]['FILIAL'] == filial_selecionada]

contagem_filiais = df_fechamento[mes_selecionado]['%CONCLUSÃO'].lt(100).sum()

col11, col12, col13 = st.columns([0.5, 0.25, 0.25])
col11.markdown('# Progresso Fechamento Fiscal:') 
col13.metric('Filiais pendentes:', contagem_filiais)
st.divider()
##
filiais_faltando = df_fechamento[mes_selecionado]['%CONCLUSÃO'].lt(100).sum()
filiais_concluidas = len(df_fechamento[mes_selecionado]) - filiais_faltando
df_pizza = pd.DataFrame({'Status': ['Concluídas', 'Faltando'], 'Quantidade': [filiais_concluidas, filiais_faltando]})


df_filial_selecionada['%CONCLUSÃO'] = pd.to_numeric(df_filial_selecionada['%CONCLUSÃO'], errors='coerce')
df_filial_selecionada['FILIAL'] = df_filial_selecionada['FILIAL'].astype(str)

fig = px.bar(df_filial_selecionada, x='%CONCLUSÃO', y='FILIAL', orientation='h', range_x=[0, 100])
fig_pizza = px.pie(df_pizza, values='Quantidade', names='Status', title=f'Filiais Concluídas vs Faltando - {mes_selecionado}')
##
fig_progresso_regiao = px.bar(df_filial_selecionada.groupby('Região')['%CONCLUSÃO'].mean().reset_index(),
                               x='Região', y='%CONCLUSÃO',
                               title=f'Progresso de Conclusão por Região - {mes_selecionado}',
                               labels={'%CONCLUSÃO': 'Progresso de Conclusão'},
                               range_y=[0, 100])
###
col14, col144, col15 = st.columns([0.45, 0.20, 0.20])
col14.plotly_chart(fig)
col144.plotly_chart(fig_pizza)

st.divider()

###
col16, col17, col179  = st.columns([0.15, 0.20, 0.25])
col17.plotly_chart(fig_progresso_regiao)

st.sidebar.markdown('###### Desevolvido por: Felipe Rocha')
##streamlit run "Desktop\Projetos Py\Check_List\01_Dashboard_Fechamento.py"