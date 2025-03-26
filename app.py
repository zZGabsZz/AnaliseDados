import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import warnings

# Suprime os warnings de futuras versões
warnings.simplefilter(action='ignore', category=FutureWarning)

# Título da aplicação
st.title("📊 Análise Financeira: Despesas vs Receitas")

# Carrega os dados do Google Sheets
url = 'https://docs.google.com/spreadsheets/d/1USAp-HVIxoi0LSUfsxb3Y7lAYWlb_JphF2nEsnEqCT8/export?format=csv&gid=0'

# Carregamento e limpeza dos dados
df = pd.read_csv(url, usecols=[0, 2, 3, 4, 8, 10, 11, 12])
df.columns = ['Data_Despesa', 'Categoria_Despesa', 'Descrição_Despesa', 'Valor_Despesa',
              'Data_Receita', 'Categoria_Receita', 'Descrição_Receita', 'Valor_Receita']

# Remove a primeira linha (caso seja cabeçalho duplicado)
df = df.drop(0)

# Limpeza de valores
df['Valor_Despesa'] = pd.to_numeric(df['Valor_Despesa'].str.replace('R$', '', regex=False).str.replace(',', '.'), errors='coerce').fillna(0)
df['Valor_Receita'] = pd.to_numeric(df['Valor_Receita'].str.replace('R$', '', regex=False).str.replace(',', '.'), errors='coerce').fillna(0)

# Separa as tabelas de Despesas e Receitas
despesas = df[['Data_Despesa', 'Categoria_Despesa', 'Descrição_Despesa', 'Valor_Despesa']]
receitas = df[['Data_Receita', 'Categoria_Receita', 'Descrição_Receita', 'Valor_Receita']]

# Calcula totais
total_despesas = despesas['Valor_Despesa'].sum()
total_receitas = receitas['Valor_Receita'].sum()
saldo = total_receitas - total_despesas

# Exibe o resumo financeiro no Streamlit
st.header("📊 Resumo Financeiro")
st.write(f"🔴 **Total de Despesas:** R$ {total_despesas:,.2f}")
st.write(f"🟢 **Total de Receitas:** R$ {total_receitas:,.2f}")
st.write(f"💰 **Saldo Líquido:** R$ {saldo:,.2f}")

# Identifica as 3 principais categorias
top_despesas = despesas.groupby('Categoria_Despesa')['Valor_Despesa'].sum().nlargest(3)
top_receitas = receitas.groupby('Categoria_Receita')['Valor_Receita'].sum().nlargest(3)

st.subheader("🔎 Principais Categorias de Despesas")
for categoria, valor in top_despesas.items():
    st.write(f"- {categoria}: R$ {valor:,.2f}")

st.subheader("📈 Principais Fontes de Receita")
for categoria, valor in top_receitas.items():
    st.write(f"- {categoria}: R$ {valor:,.2f}")

# Gráfico de comparação Despesas vs Receitas
st.subheader("📊 Comparativo: Despesas vs Receitas")
fig, ax = plt.subplots()
sns.barplot(x=['Despesas', 'Receitas'], y=[total_despesas, total_receitas], palette=['#FF6347', '#32CD32'])
plt.ylabel('Valor (R$)')
plt.title('Despesas vs Receitas')
st.pyplot(fig)

# Gráfico de Receitas ao longo do tempo
st.subheader("📊 Receitas ao Longo do Tempo")
fig, ax = plt.subplots()
sns.lineplot(data=receitas, x='Data_Receita', y='Valor_Receita', marker='o', color='green')
plt.xticks(rotation=45)
plt.ylabel('Valor (R$)')
st.pyplot(fig)

# Mostra as primeiras 10 linhas do DataFrame de Receitas
st.subheader("📋 Primeiras Receitas Registradas")
st.dataframe(receitas.head(10))
