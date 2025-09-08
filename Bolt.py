import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Calculadora TVDE Semanal",
    page_icon="🚗",
    layout="centered"
)

# Título da aplicação
st.title("🚗 Calculadora de Ganhos Semanais TVDE")
st.markdown("Calcule seus rendimentos líquidos semanais como motorista TVDE")

# Inicializar variáveis de sessão
if 'comissao_plataforma' not in st.session_state:
    st.session_state.comissao_plataforma = 6.0
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

# Entradas principais do usuário
st.header("Entradas Semanais")

# Valores iniciais conforme solicitado
apuro_semanal = 700.0
aluguer_semanal = 270.0
combustivel_semanal = 150.0

col1, col2 = st.columns(2)

with col1:
    dias_trabalhados = st.slider("Dias trabalhados na semana", 1, 7, 5)
    ganhos_brutos_semana = st.number_input(
        "Ganhos Brutos Semanais (€)", 
        min_value=0.0, 
        value=apuro_semanal, 
        step=10.0,
        help="Total de ganhos brutos na semana (apuro)"
    )

with col2:
    custo_gasolina_semana = st.number_input(
        "Custo com Gasolina Semanal (€)", 
        min_value=0.0, 
        value=combustivel_semanal, 
        step=10.0
    )
    aluguer_semana = st.number_input(
        "Aluguer Semanal da Viatura (€)", 
        min_value=0.0, 
        value=aluguer_semanal, 
        step=10.0
    )
    outros_custos = st.number_input(
        "Outros Custos Semanais (€)", 
        min_value=0.0, 
        value=0.0, 
        step=5.0,
        help="Lavagens, portagens, estacionamento, etc."
    )

# Cálculos
comissao_valor_semana = ganhos_brutos_semana * (st.session_state.comissao_plataforma / 100)

ganhos_liquidos_semana = (ganhos_brutos_semana - comissao_valor_semana - 
                         custo_gasolina_semana - aluguer_semana - outros_custos)

margem_lucro = (ganhos_liquidos_semana / ganhos_brutos_semana) * 100 if ganhos_brutos_semana > 0 else 0

# Exibir resultados
st.header("Resultados Semanais")

col1, col2, col3 = st.columns(3)
col1.metric("Ganhos Líquidos Semanais", f"€{ganhos_liquidos_semana:.2f}")
col2.metric("Comissão Plataforma", f"€{comissao_valor_semana:.2f}")
col3.metric("Margem de Lucro", f"{margem_lucro:.1f}%")

# Visualização gráfica
st.subheader("Distribuição dos Custos e Ganhos")

# Preparar dados para o gráfico
categorias = ['Ganhos Líquidos', 'Comissão Plataforma', 'Gasolina', 'Aluguer Viatura', 'Outros Custos']
valores = [
    max(ganhos_liquidos_semana, 0), 
    comissao_valor_semana, 
    custo_gasolina_semana, 
    aluguer_semana, 
    outros_custos
]
cores = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#9b59b6']

# Criar gráfico
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categorias, valores, color=cores)
ax.set_ylabel('Valores (€)')
ax.set_title('Distribuição Semanal de Custos e Ganhos')

# Adicionar valores nas barras
for bar, valor in zip(bars, valores):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'€{valor:.2f}', ha='center', va='bottom')

plt.xticks(rotation=45)
st.pyplot(fig)

# Detalhamento dos cálculos
with st.expander("📊 Ver detalhamento dos cálculos"):
    st.subheader("Detalhamento Semanal")
    st.write(f"**Ganhos brutos semanais (apuro):** €{ganhos_brutos_semana:.2f}")
    st.write(f"**Comissão da plataforma ({st.session_state.comissao_plataforma}%):** €{comissao_valor_semana:.2f}")
    st.write(f"**Custo com gasolina semanal:** €{custo_gasolina_semana:.2f}")
    st.write(f"**Aluguer da viatura semanal:** €{aluguer_semana:.2f}")
    st.write(f"**Outros custos:** €{outros_custos:.2f}")
    st.write(f"**Ganhos líquidos semanais:** €{ganhos_brutos_semana:.2f} - €{comissao_valor_semana:.2f} - €{custo_gasolina_semana:.2f} - €{aluguer_semana:.2f} - €{outros_custos:.2f} = €{ganhos_liquidos_semana:.2f}")
    
    # Cálculo diário
    st.subheader("Médias Diárias")
    st.write(f"**Ganhos brutos diários:** €{ganhos_brutos_semana/dias_trabalhados:.2f}")
    st.write(f"**Ganhos líquidos diários:** €{ganhos_liquidos_semana/dias_trabalhados:.2f}")

# Projeção mensal
st.header("📈 Projeção Mensal")
dias_uteis_mes = st.slider("Dias úteis no mês", 20, 31, 22)
semanas_mes = dias_uteis_mes / dias_trabalhados
ganhos_mensais = ganhos_liquidos_semana * semanas_mes

col1, col2 = st.columns(2)
col1.metric("Projeção de Ganhos Mensais", f"€{ganhos_mensais:.2f}")
col2.metric("Média Diária Líquida", f"€{ganhos_liquidos_semana/dias_trabalhados:.2f}")

# Resumo final
st.header("💶 Resumo Financeiro")
resumo_col1, resumo_col2, resumo_col3 = st.columns(3)
resumo_col1.metric("Apuro Semanal", f"€{ganhos_brutos_semana:.2f}")
resumo_col2.metric("Custos Semanais", f"€{(comissao_valor_semana + custo_gasolina_semana + aluguer_semana + outros_custos):.2f}")
resumo_col3.metric("Lucro Semanal", f"€{ganhos_liquidos_semana:.2f}", 
                  delta=f"{margem_lucro:.1f}%")

# Rodapé
st.markdown("---")
st.caption("App desenvolvido para cálculo de ganhos no TVDE. Considere outros custos não incluídos aqui como manutenção, seguros, etc.")
