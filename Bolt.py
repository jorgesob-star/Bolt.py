import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Calculadora TVDE",
    page_icon="🚗",
    layout="centered"
)

# Título da aplicação
st.title("🚗 Calculadora de Ganhos TVDE")
st.markdown("Calcule seus rendimentos líquidos como motorista TVDE")

# Inicializar variáveis de sessão para manter os valores
if 'comissao_plataforma' not in st.session_state:
    st.session_state.comissao_plataforma = 6.0
if 'aluguer_viatura' not in st.session_state:
    st.session_state.aluguer_viatura = 30.0
if 'show_advanced' not in st.session_state:
    st.session_state.show_advanced = False

# Função para alternar a visualização das configurações avançadas
def toggle_advanced():
    st.session_state.show_advanced = not st.session_state.show_advanced

# Botão para mostrar/ocultar configurações avançadas
st.button(
    "⚙️ Configurações Avançadas" if not st.session_state.show_advanced else "⬆️ Ocultar Configurações",
    on_click=toggle_advanced
)

# Mostrar configurações avançadas se o botão foi clicado
if st.session_state.show_advanced:
    with st.expander("Configurações Avançadas", expanded=True):
        st.session_state.comissao_plataforma = st.number_input(
            "Comissão da Plataforma (%)", 
            min_value=0.0, max_value=100.0, 
            value=st.session_state.comissao_plataforma, step=0.5,
            key="comissao_input"
        )
        st.session_state.aluguer_viatura = st.number_input(
            "Aluguer da Viatura (€)", 
            min_value=0.0, value=st.session_state.aluguer_viatura, step=5.0,
            key="aluguer_input"
        )

# Entradas principais do usuário
st.header("Entradas")
col1, col2 = st.columns(2)

with col1:
    ganhos_brutos = st.number_input("Ganhos Brutos (€)", min_value=0.0, value=100.0, step=10.0)

with col2:
    custo_gasolina = st.number_input("Custo com Gasolina (€)", min_value=0.0, value=20.0, step=5.0)

# Cálculos
comissao_valor = ganhos_brutos * (st.session_state.comissao_plataforma / 100)
ganhos_liquidos = ganhos_brutos - comissao_valor - custo_gasolina - st.session_state.aluguer_viatura
margem_lucro = (ganhos_liquidos / ganhos_brutos) * 100 if ganhos_brutos > 0 else 0

# Exibir resultados
st.header("Resultados")

col1, col2, col3 = st.columns(3)
col1.metric("Ganhos Líquidos", f"€{ganhos_liquidos:.2f}")
col2.metric("Comissão Plataforma", f"€{comissao_valor:.2f} ({st.session_state.comissao_plataforma}%)")
col3.metric("Margem de Lucro", f"{margem_lucro:.1f}%")

# Visualização simplificada
st.subheader("Distribuição dos Valores")

# Criar gráfico de barras simples
valores = [ganhos_liquidos, comissao_valor, custo_gasolina, st.session_state.aluguer_viatura]
categorias = ['Ganhos Líquidos', 'Comissão Plataforma', 'Gasolina', 'Aluguer Viatura']

data = {"Categorias": categorias, "Valores (€)": valores}
st.bar_chart(data, x="Categorias", y="Valores (€)")

# Detalhamento dos cálculos
with st.expander("Ver detalhamento dos cálculos"):
    st.write(f"**Ganhos brutos:** €{ganhos_brutos:.2f}")
    st.write(f"**Comissão da plataforma ({st.session_state.comissao_plataforma}%):** €{comissao_valor:.2f}")
    st.write(f"**Custo com gasolina:** €{custo_gasolina:.2f}")
    st.write(f"**Aluguer da viatura:** €{st.session_state.aluguer_viatura:.2f}")
    st.write(f"**Ganhos líquidos:** €{ganhos_brutos:.2f} - €{comissao_valor:.2f} - €{custo_gasolina:.2f} - €{st.session_state.aluguer_viatura:.2f} = €{ganhos_liquidos:.2f}")

# Adicionar seção para múltiplos dias
st.header("📅 Cálculo para Múltiplos Dias")
dias_trabalhados = st.slider("Número de dias trabalhados", 1, 30, 1)
ganhos_totais = ganhos_liquidos * dias_trabalhados

st.metric(f"Ganhos líquidos para {dias_trabalhados} dias", f"€{ganhos_totais:.2f}")

# Rodapé
st.markdown("---")
st.caption("App desenvolvido para cálculo de ganhos no TVDE. Considere outros custos não incluídos aqui como manutenção, seguros, etc.")
