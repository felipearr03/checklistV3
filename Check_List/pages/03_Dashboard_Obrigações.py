from pathlib import Path
from datetime import date, datetime, timedelta
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide")

pasta_atual = Path(__file__).parent.parent.parent.parent

logo_path = r"\\10.0.8.50\Setores\Central de Serviços\Fiscal\FELIPE ANDRADE ROCHA\DELLYS_LOGO-removebg-preview.png"  # Substitua pelo caminho do seu arquivo de imagem
logo = Image.open(logo_path)
st.sidebar.image(logo, width=200)
caminho_arquivo = r"\\10.0.8.50\Setores\Central de Serviços\Fiscal\FELIPE ANDRADE ROCHA\TESTE\1.1 CHECK LIST - Declarações Estaduais Dellys 2024.xlsx"

# Fazendo a leitura do arquivo Excel
df_fechamento = pd.read_excel(caminho_arquivo, sheet_name=None, parse_dates=True)
df_concatenado = pd.concat(df_fechamento.values(), ignore_index=True)

## ##
mes_selecionado = st.sidebar.selectbox('Selecione o Mês:', df_fechamento.keys())
opcoes_filiais = ['Todas as Filiais'] + list(df_fechamento[mes_selecionado]['CÓD.'].unique())
filial_selecionada = st.sidebar.selectbox('Selecione a Filial:', opcoes_filiais)

if filial_selecionada == 'Todas as Filiais':
    df_filial_selecionada = df_fechamento[mes_selecionado]
else:
    df_filial_selecionada = df_fechamento[mes_selecionado][df_fechamento[mes_selecionado]['CÓD.'] == filial_selecionada]

# Criando uma tabela dinâmica usando o DataFrame filtrado
tabela_dinamica = pd.pivot_table(df_filial_selecionada, values='STATUS', index='CÓD.', aggfunc=['count', lambda x: x.eq('OK').sum()])

# Renomeando as colunas
tabela_dinamica.columns = ['Total Obrigações', 'Qtd. Entregue']

# Calculando o progresso por filial
tabela_dinamica['%Progresso'] = (tabela_dinamica['Qtd. Entregue'] / tabela_dinamica['Total Obrigações']) * 100

contagem_filiais = tabela_dinamica['%Progresso'].lt(100).sum()

col11, col12, col13 = st.columns([0.5, 0.25, 0.25])
col11.markdown('# Progresso Entrega das obrigações acessórias:') 
col13.metric('Filiais pendentes:', contagem_filiais)
st.divider()

# Adicionando um gráfico de barras para representar o progresso por filial com Plotly Express
fig = px.bar(tabela_dinamica, x='%Progresso', y=tabela_dinamica.index, orientation='h', 
             labels={'%Progresso': '%Progresso (%)', 'index': 'Filial'})

# Definindo o layout do gráfico
fig.update_layout(title='Progresso de Entrega por Filial',
                  xaxis_title='Progresso (%)',
                  yaxis_title='Filial')

filiais_pendentes = df_filial_selecionada[df_filial_selecionada['STATUS'] != 'OK']

# Criando uma tabela dinâmica para filiais pendentes
tabela_dinamica_pendentes = pd.DataFrame(index=df_filial_selecionada['CÓD.'].unique())
tabela_dinamica_pendentes['Qtd. Obrigações Pendentes'] = 0

if not filiais_pendentes.empty:
    tabela_dinamica_pendentes = pd.pivot_table(filiais_pendentes, values='STATUS', index='CÓD.', aggfunc='count')
    tabela_dinamica_pendentes.columns = ['Qtd. Obrigações Pendentes']

# Adicionando um gráfico de pizza para o total do progresso e total pendente
fig_pizza = px.pie(names=['Entregue', 'Pendente'], values=[tabela_dinamica['Qtd. Entregue'].sum(), tabela_dinamica_pendentes['Qtd. Obrigações Pendentes'].sum()])
col14, col15, col16 = st.columns([0.45, 0.20, 0.20])
col14.plotly_chart(fig)
col15.plotly_chart(fig_pizza)
st.divider()

col18, col19, col110 = st.columns([0.5, 0.25, 0.25])
col18.markdown('## Filiais pendentes de Entrega:')

if not tabela_dinamica_pendentes.empty:
    st.write(tabela_dinamica_pendentes)
else:
    st.write("Não há filiais pendentes de entrega.")
