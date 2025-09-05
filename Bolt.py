import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Descontos (sem Uber)", layout="centered")
st.title("💸 Calculadora de Descontos (sem Uber)")
st.markdown("Calcule rapidamente os descontos da Empresa, Aluguer, Seguro e Combustível.")

# Entrada principal
st.subheader("Insira os valores:")
valor_inicial = st.number_input("💰 Valor inicial", min_value=0.0, value=700.0, step=10.0)

# Linha dividida em 2 colunas
col1, col2 = st.columns(2)

with col1:
    # Percentagem Empresa (esquerda)
    perc_esq = st.number_input("👔 Empresa (%)", min_value=0.0, value=7.0, step=0.5)
    # Aluguer editável
    aluguer = st.number_input("🏠 Aluguer (€)", min_value=0.0, value=280.0, step=1.0)

with col2:
    # Percentagem Empresa (direita)
    perc_dir = st.number_input("👔 Empresa (%)", min_value=0.0, value=12.0, step=0.5)
    # Seguro editável
    seguro = st.number_input("🛡️ Seguro (€)", min_value
