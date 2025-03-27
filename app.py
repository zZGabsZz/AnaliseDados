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

# Função para limpar e converter valores numéricos
def limpar_valor(valor):
    if isinstance(valor, str):
        valor = valor.replace('R$', '').replace(',', '.')
    return pd.to_numeric(valor, errors='coerce')

# Aplica a função de limpeza
df['Valor_Despesa'] = df['Valor_Despesa'].apply(limpar_valor).fillna(0)
df['Valor_Receita'] = df['Valor_Receita'].apply(limpar_valor).fillna(0)

# Função para formatar valores
def formatar(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Separa as tabelas de Despesas e Receitas
despesas = df[['Data_Despesa', 'Categoria_Despesa', 'Descrição_Despesa', 'Valor_Despesa']].dropna()
receitas = df[['Data_Receita', 'Categoria_Receita', 'Descrição_Receita', 'Valor_Receita']].dropna()

# Calcula totais
total_despesas = despesas['Valor_Despesa'].sum()
total_receitas = receitas['Valor_Receita'].sum()
saldo = total_receitas - total_despesas

# Exibe o resumo financeiro no Streamlit
st.header("📊 Resumo Financeiro")
st.write(f"🔴 **Total de Despesas:** {formatar(total_despesas)}")
st.write(f"🟢 **Total de Receitas:** {formatar(total_receitas)}")
st.write(f"💰 **Saldo Líquido:** {formatar(saldo)}")

# Identifica as 3 principais categorias
top_despesas = despesas.groupby('Categoria_Despesa')['Valor_Despesa'].sum().nlargest(3)
top_receitas = receitas.groupby('Categoria_Receita')['Valor_Receita'].sum().nlargest(3)

st.subheader("🔎 Principais Categorias de Despesas")
for categoria, valor in top_despesas.items():
    st.write(f"- {categoria}: {formatar(valor)}")

st.subheader("📈 Principais Fontes de Receita")
for categoria, valor in top_receitas.items():
    st.write(f"- {categoria}: {formatar(valor)}")

# Gráfico de comparação Despesas vs Receitas
st.subheader("📊 Comparativo: Despesas vs Receitas")
fig, ax = plt.subplots()
sns.barplot(x=['Despesas', 'Receitas'], y=[total_despesas, total_receitas], palette=['#FF6347', '#32CD32'])
plt.ylabel('Valor (R$)')
plt.title('Despesas vs Receitas')
for i, v in enumerate([total_despesas, total_receitas]):
    plt.text(i, v + 1000, f'R$ {v:,.2f}', ha='center', fontsize=12, color='black')
st.pyplot(fig)

# Gráficos de Despesas e Receitas por Data

# Despesas por Data
st.subheader("📊 Despesas ao Longo do Tempo")
fig, ax = plt.subplots()
sns.lineplot(data=despesas, x='Data_Despesa', y='Valor_Despesa', marker='o', color='red')
plt.xticks(rotation=45)
plt.ylabel('Valor (R$)')
st.pyplot(fig)

# Receitas por Data
st.subheader("📊 Receitas ao Longo do Tempo")
fig, ax = plt.subplots()
sns.lineplot(data=receitas, x='Data_Receita', y='Valor_Receita', marker='o', color='green')
plt.xticks(rotation=45)
plt.ylabel('Valor (R$)')
st.pyplot(fig)

# Gráfico de Despesas e Receitas com destaque de categorias
st.subheader("📊 Despesas e Receitas por Categoria e Mês")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Despesas por Categoria
sns.scatterplot(data=despesas, x='Data_Despesa', y='Valor_Despesa', hue='Categoria_Despesa', palette='Reds', s=100, ax=axes[0])
axes[0].set_title('Despesas por Categoria e Mês')
axes[0].tick_params(axis='x', rotation=45)

# Receitas por Categoria
sns.scatterplot(data=receitas, x='Data_Receita', y='Valor_Receita', hue='Categoria_Receita', palette='Greens', s=100, ax=axes[1])
axes[1].set_title('Receitas por Categoria e Mês')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
st.pyplot(fig)
