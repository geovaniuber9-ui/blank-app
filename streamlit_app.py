import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS Consultoria V31 - Eco", page_icon="🌱", layout="wide")

# 2. ESTILO VISUAL (AMBIENTE VERDE CLARO)
st.markdown("""
    <style>
    /* FUNDO VERDE CLARO ECO */
    .stApp { background-color: #E8F5E9 !important; color: #1B5E20; }
    
    /* CARDS BRANCOS COM BORDA VERDE */
    .card-trabalho {
        background: #FFFFFF;
        border: 2px solid #2E7D32;
        padding: 15px; border-radius: 12px; margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .titulo-card { color: #1B5E20; font-size: 18px; font-weight: bold; }
    .valor { color: #388E3C; font-size: 22px; font-weight: bold; }
    .local { color: #FFA000; font-weight: bold; }
    
    /* BOTÕES VERDE FLORESTA */
    .stButton>button {
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        color: white; border-radius: 10px; font-weight: bold; height: 3.5em; width: 100%;
        border: none;
    }
    .stTabs [data-baseweb="tab-list"] button { font-size: 14px; color: #2E7D32; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. BANCO DE DADOS DE MISSÕES (MUITAS OPÇÕES)
if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0
if 'status' not in st.session_state: st.session_state.status = "mural"

# --- SIDEBAR ECOLÓGICA ---
with st.sidebar:
    st.title("👤 Geovani Santi")
    st.metric("Ganhos Sustentáveis", f"R$ {st.session_state.ganhos:.2f}")
    df_hist = pd.DataFrame({"Hora": ["12h", "14h", "16h", "Agora"], "R$": [50, 120, 80, st.session_state.ganhos]})
    fig = px.area(df_hist, x="Hora", y="R$", title="Fluxo de Caixa 🌱")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#1B5E20", height=200)
    st.plotly_chart(fig, use_container_width=True)

# --- MURAL DE MISSÕES EXPANDIDO (TODAS CATEGORIAS COM 5 OPÇÕES) ---
if st.session_state.status == "mural":
    st.title("🌱 Radar de Missões Ecológicas - Osasco")
    t1, t2, t3, t4, t5 = st.tabs(["🧹 Zeladoria", "🏥 Saúde", "♻️ Resíduos", "🌱 Jardinagem", "🎪 Logística"])
    
    # 🧹 ZELADORIA (5 OPÇÕES)
    with t1:
        missoes_zeladoria = [
            ("Varrição de Vias Pública", 55.0, "Centro"),
            ("Pintura de Meio-Fio
             
