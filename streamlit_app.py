import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS Consultoria Full", page_icon="⚡", layout="wide")

# 2. ESTILO VISUAL PREMIUM (DARK MODE)
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14 !important; color: #FFFFFF; }
    .card-trabalho {
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid #00D4FF;
        padding: 15px; border-radius: 12px; margin-bottom: 10px;
    }
    .valor { color: #00E676; font-size: 22px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(90deg, #00D4FF, #0052D4);
        color: white; border-radius: 10px; font-weight: bold; height: 3.5em; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INICIALIZAÇÃO DE DADOS
if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0
if 'status' not in st.session_state: st.session_state.status = "mural"

# --- SIDEBAR COM GRÁFICO ---
with st.sidebar:
    st.title("👤 Geovani Santi")
    st.metric("Saldo Total", f"R$ {st.session_state.ganhos:.2f}")
    df = pd.DataFrame({"Dia": ["Seg", "Ter", "Qua", "Hoje"], "R$": [100, 150, 90, st.session_state.ganhos]})
    fig = px.line(df, x="Dia", y="R$", markers=True)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#FFF", height=200)
    st.plotly_chart(fig, use_container_width=True)

# --- RADAR DE MISSÕES COMPLETO ---
if st.session_state.status == "mural":
    st.title("📍 Radar de Missões - Osasco")
    t1, t2, t3, t4 = st.tabs(["🏥 Saúde", "🧹 Zeladoria", "♻️ Resíduos", "🎪 Logística"])
    
    with t1:
        st.markdown('<div class="card-trabalho"><b>Acompanhante Idoso</b><br>📍 Vila Yara<br><span class="valor">R$ 102.00</span></div>', unsafe_allow_html=True)
        if st.button("ACEITAR MISSÃO: SAÚDE", key="s1"):
            st.session_state.missao = {"nome": "Acompanhante", "valor": 102.0, "local": "Vila Yara"}
            st.session_state.status = "gps"; st.rerun()
            
    with t2:
        st.markdown('<div class="card-trabalho"><b>Varrição de Vias</b><br>📍 Centro<br><span class="valor">R$ 55.00</span></div>', unsafe_allow_html=True)
        if st.button("ACEITAR MISSÃO: VARRIÇÃO", key="z1"):
            st.session_state.missao = {"nome": "Varrição", "valor": 55.0, "local": "Centro"}
            st.session_state.status = "gps"; st.rerun()

    with t3:
        st.markdown('<div class="card-trabalho"><b>Triagem Manual</b><br>📍 Mutinga<br><span class="valor">R$ 65.00</span></div>', unsafe_allow_html=True)
        if st.button("ACEITAR MISSÃO: TRIAGEM", key="r1"):
            st.session_state.missao = {"nome": "Triagem", "valor": 65.0, "local": "Mutinga"}
            st.session_state.status = "gps"; st.rerun()

    with t4:
        st.markdown('<div class="card-trabalho"><b>Montagem de Palco</b><br>📍 Arena Osasco<br><span class="valor">R$ 150.00</span></div>', unsafe_allow_html=True)
        if st.button("ACEITAR MISSÃO: LOGÍSTICA", key="l1"):
            st.session_state.missao = {"nome": "Montagem", "valor": 150.0, "local": "Arena"}
            st.session_state.status = "gps"; st.rerun()

elif st.session_state.status == "gps":
    st.header(f"🧭 Rota para: {st.session_state.missao['local']}")
    st.markdown(f'<a href="https://www.google.com/maps/search/{st.session_state.missao["local"]}+Osasco" target="_blank"><button style="background:#FFB300; width:100%; border-radius:10px; padding:15px; font-weight:bold;">ABRIR NO GOOGLE MAPS</button></a>', unsafe_allow_html=True)
    if st.button("✅ CHEGUEI NO LOCAL", key="cheguei"):
        st.session_state.status = "fotos"; st.rerun()

elif st.session_state.status == "fotos":
    st.header("📸 Validação de Serviço")
    st.camera_input("🤳 Selfie no Local", key="selfie")
    if st.button("🏁 FINALIZAR E RECEBER", key="fim"):
        st.session_state.ganhos += st.session_state.missao['valor']
        st.session_state.status = "mural"; st.rerun()
      
