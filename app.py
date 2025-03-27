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

# 🔹 Função para limpar e converter valores
def limpar_valor(valor):
    if isinstance(valor, str):  # Confirma que é string antes de limpar
        valor = valor.replace('R$', '').replace(' ', '').replace('.', '')  # Remove espaços e pontos de milhar
        valor = valor.replace(',', '.')  # Substitui vírgulas por ponto para conversão numérica
    valor_convertido = pd.to_numeric(valor, errors='coerce')  # Converte, mantendo NaN se não for número
    return valor_convertido

# Aplica a função a ambas as colunas
df['Valor_Despesa'] = df['Valor_Despesa'].apply(limpar_valor).fillna(0)
df['Valor_Receita'] = df['Valor_Receita'].apply(limpar_valor).fillna(0)

# Separa as tabelas de Despesas e Receitas
despesas = df[['Data_Despesa', 'Categoria_Despesa', 'Descrição_Despesa', 'Valor_Despesa']].dropna()
receitas = df[['Data_Receita', 'Categoria_Receita', 'Descrição_Receita', 'Valor_Receita']].dropna()

# Calcula totais
total_despesas = despesas['Valor_Despesa'].sum()
total_receitas = receitas['Valor_Receita'].sum()
saldo = total_receitas - total_despesas

# 🔹 Função para formatar os valores em moeda
def formatar(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

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

# 📊 Gráfico de comparação Despesas vs Receitas
st.subheader("📊 Comparativo: Despesas vs Receitas")
fig, ax = plt.subplots()
sns.barplot(x=['Despesas', 'Receitas'], y=[total_despesas, total_receitas], palette=['#FF6347', '#32CD32'])
plt.ylabel('Valor (R$)')
plt.title('Despesas vs Receitas')
for i, v in enumerate([total_despesas, total_receitas]):
    plt.text(i, v + 1000, formatar(v), ha='center', fontsize=12, color='black')
st.pyplot(fig)

# 📊 Gráficos de Despesas e Receitas por Data

# Agrupando as despesas por mês
despesas_agregadas = despesas.groupby('Data_Despesa')['Valor_Despesa'].sum().reset_index()

# Agrupando as receitas por mês
receitas_agregadas = receitas.groupby('Data_Receita')['Valor_Receita'].sum().reset_index()

# 🔹 Ajustando para garantir que os meses estão em ordem crescente
despesas_agregadas['Data_Despesa'] = pd.to_numeric(despesas_agregadas['Data_Despesa'], errors='coerce')
despesas_agregadas = despesas_agregadas.sort_values(by='Data_Despesa')

receitas_agregadas['Data_Receita'] = pd.to_numeric(receitas_agregadas['Data_Receita'], errors='coerce')
receitas_agregadas = receitas_agregadas.sort_values(by='Data_Receita')

# Gráfico de Despesas ao Longo do Tempo
st.subheader("📊 Despesas ao Longo do Tempo")
fig, ax = plt.subplots()
sns.lineplot(data=despesas_agregadas, x='Data_Despesa', y='Valor_Despesa', marker='o', color='red')
plt.xticks(range(1, 13))  # Garante que os meses de 1 a 12 apareçam no eixo X
plt.xlabel('Meses')  # Modifica o título do eixo X
plt.ylabel('Valor (R$)')
st.pyplot(fig)

# Gráfico de Receitas ao Longo do Tempo
st.subheader("📊 Receitas ao Longo do Tempo")
fig, ax = plt.subplots()
sns.lineplot(data=receitas_agregadas, x='Data_Receita', y='Valor_Receita', marker='o', color='green')
plt.xticks(range(1, 13))  # Garante que os meses de 1 a 12 apareçam no eixo X
plt.xlabel('Meses')  # Modifica o título do eixo X
plt.ylabel('Valor (R$)')
st.pyplot(fig)

# 📊 Comparação de Despesas e Receitas ao Longo do Tempo
st.subheader("📊 Comparação de Despesas e Receitas ao Longo do Tempo")

# Agrupar as despesas e receitas por mês (soma de valores)
despesas_agregadas = despesas.groupby('Data_Despesa')['Valor_Despesa'].sum().reset_index()
receitas_agregadas = receitas.groupby('Data_Receita')['Valor_Receita'].sum().reset_index()

# Garantir que os meses estão em ordem crescente (1 a 12) para ambos
despesas_agregadas['Data_Despesa'] = pd.to_numeric(despesas_agregadas['Data_Despesa'], errors='coerce')
despesas_agregadas = despesas_agregadas.sort_values(by='Data_Despesa')

receitas_agregadas['Data_Receita'] = pd.to_numeric(receitas_agregadas['Data_Receita'], errors='coerce')
receitas_agregadas = receitas_agregadas.sort_values(by='Data_Receita')

# Criar o dataframe combinado para juntar as despesas e receitas, garantindo os valores de cada mês
df_combinado = pd.concat([ 
    despesas_agregadas[['Data_Despesa', 'Valor_Despesa']].rename(columns={'Data_Despesa': 'Mes', 'Valor_Despesa': 'Valor'}).assign(Tipo='Despesa'),
    receitas_agregadas[['Data_Receita', 'Valor_Receita']].rename(columns={'Data_Receita': 'Mes', 'Valor_Receita': 'Valor'}).assign(Tipo='Receita')
])

# Garantir que os meses estão em ordem crescente (1 a 12)
df_combinado['Mes'] = pd.to_numeric(df_combinado['Mes'], errors='coerce')
df_combinado = df_combinado.sort_values(by='Mes')

# Criar o gráfico combinando Despesas e Receitas
fig, ax = plt.subplots()
sns.lineplot(data=df_combinado, x='Mes', y='Valor', hue='Tipo', marker='o', palette={'Despesa': 'red', 'Receita': 'green'})

plt.xticks(range(1, 13))  # Garante que os meses de 1 a 12 apareçam no eixo X
plt.xlabel('Meses')  # Modifica o título do eixo X
plt.ylabel('Valor (R$)')
plt.legend(title='Tipo')  # Exibe a legenda para diferenciar Despesas e Receitas

st.pyplot(fig)


# 📊 Gráfico de Despesas por Categoria e Mês
st.subheader("📊 Despesas por Categoria e Mês")
fig_despesas, ax_despesas = plt.subplots(figsize=(8, 6))  # Tamanho do gráfico
sns.scatterplot(data=despesas, x='Data_Despesa', y='Valor_Despesa', hue='Categoria_Despesa', palette='Reds', s=100, ax=ax_despesas)
ax_despesas.set_title('Despesas por Categoria e Mês')
ax_despesas.tick_params(axis='x', rotation=45)
st.pyplot(fig_despesas)

# 📊 Gráfico de Receitas por Categoria e Mês
st.subheader("📊 Receitas por Categoria e Mês")
fig_receitas, ax_receitas = plt.subplots(figsize=(8, 6))  # Tamanho do gráfico
sns.scatterplot(data=receitas, x='Data_Receita', y='Valor_Receita', hue='Categoria_Receita', palette='Greens', s=100, ax=ax_receitas)
ax_receitas.set_title('Receitas por Categoria e Mês')
ax_receitas.tick_params(axis='x', rotation=45)
st.pyplot(fig_receitas)

