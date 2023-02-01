import pandas as pd
import plotly.express as px
import streamlit as st

# Lendo a base de dados
df_vendas = pd.read_excel("Vendas.xlsx")
df_produtos = pd.read_excel("Produtos.xlsx")

df = pd.merge(df_vendas,df_produtos, how="left", on="ID Produto")
df["Custo"] = df["Custo Unitário"] * df["Quantidade"]
df["Lucro"] = df["Valor Venda"] - df["Custo"]
df['mes_ano'] = df['Data Venda'].dt.to_period("M").astype(str)

produtos_vendidos_marca = df.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
lucro_categoria = df.groupby("Categoria")["Lucro"].sum().reset_index()
lucro_mes_categoria = df.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()
def main():

    st.title("Análise Vendas")
    st.image("vendas.png")



    col1, col2, col3 = st.columns(3)
    with col1:
        col1.metric("Total Custo", df["Custo"].sum())
    with col2:    
        col2.metric("Lucro", df["Lucro"].sum())
    with col3:
        col3.metric("Total Clientes", df["ID Cliente"].nunique())

    col1, col2 = st.columns(2, gap="large")

    fig = px.bar(produtos_vendidos_marca, x='Quantidade', 
    y='Marca', orientation="h", text="Quantidade", 
    width=380, height=400, title="Total Produtos vendidos por Marca")
    col1.write(fig)


    fig1 = px.pie(lucro_categoria, values='Lucro', names='Categoria',
    title="Lucro por Marca",width=450, height=400 )
    col2.plotly_chart(fig1)

    fig2 = px.line(lucro_mes_categoria, x="mes_ano", y="Lucro", 
    title='Lucro X Mês X Categoria', width=1000, height=400,
    markers=True, color="Categoria", 
              labels={"mes_ano":"Mês", "Lucro":"Lucro no Mês"})
    st.plotly_chart(fig2)

if __name__ == '__main__':
    main()