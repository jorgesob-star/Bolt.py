import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Calculadora TVDE",
    page_icon="🚗",
    layout="centered"
)

# Título da aplicação
st.title("🚗 Calculadora de Ganhos TVDE")
st.markdown("Calcule seus rendimentos líquidos como motorista TVDE")

# Entradas do usuário
st.header("Entradas")
col1, col2 = st.columns(2)

with col1:
    ganhos_brutos = st.number_input("Ganhos Brutos (€)", min_value=0.0, value=100.0, step=10.0)
    comissao_plataforma = st.number_input("Comissão da Plataforma (%)", min_value=0.0, max_value=100.0, value=6.0, step=0.5)

with col2:
    custo_gasolina = st.number_input("Custo com Gasolina (€)", min_value=0.0, value=20.0, step=5.0)
    aluguer_viatura = st.number_input("Aluguer da Viatura (€)", min_value=0.0, value=30.0, step=5.0)

# Cálculos
comissao_valor = ganhos_brutos * (comissao_plataforma / 100)
ganhos_liquidos = ganhos_brutos - comissao_valor - custo_gasolina - aluguer_viatura
margem_lucro = (ganhos_liquidos / ganhos_brutos) * 100 if ganhos_brutos > 0 else 0

# Exibir resultados
st.header("Resultados")

col1, col2, col3 = st.columns(3)
col1.metric("Ganhos Líquidos", f"€{ganhos_liquidos:.2f}")
col2.metric("Comissão Plataforma", f"€{comissao_valor:.2f}")
col3.metric("Margem de Lucro", f"{margem_lucro:.1f}%")

# Visualização gráfica
st.subheader("Distribuição dos Custos e Ganhos")

dados = {
    'Categoria': ['Ganhos Líquidos', 'Comissão Plataforma', 'Gasolina', 'Aluguer Viatura'],
    'Valor (€)': [ganhos_liquidos, comissao_valor, custo_gasolina, aluguer_viatura],
    'Tipo': ['Ganho', 'Custo', 'Custo', 'Custo']
}

df = pd.DataFrame(dados)
fig = px.pie(df, values='Valor (€)', names='Categoria', 
             title='Distribuição dos Valores',
             color='Tipo', color_discrete_map={'Ganho':'green', 'Custo':'red'})
st.plotly_chart(fig)

# Detalhamento dos cálculos
with st.expander("Ver detalhamento dos cálculos"):
    st.write(f"**Ganhos brutos:** €{ganhos_brutos:.2f}")
    st.write(f"**Comissão da plataforma ({comissao_plataforma}%):** €{comissao_valor:.2f}")
    st.write(f"**Custo com gasolina:** €{custo_gasolina:.2f}")
    st.write(f"**Aluguer da viatura:** €{aluguer_viatura:.2f}")
    st.write(f"**Ganhos líquidos:** €{ganhos_brutos:.2f} - €{comissao_valor:.2f} - €{custo_gasolina:.2f} - €{aluguer_viatura:.2f} = €{ganhos_liquidos:.2f}")

# Rodapé
st.markdown("---")
st.caption("App desenvolvido para cálculo de ganhos no TVDE. Considere outros custos não incluídos aqui como manutenção, seguros, etc.")
