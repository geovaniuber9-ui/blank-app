import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS Consultoria V30", page_icon="⚡", layout="wide")

# 2. ESTILO VISUAL (DARK MODE NEON)
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14 !important; color: #FFFFFF; }
    .card-trabalho {
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid #00D4FF;
        padding: 15px; border-radius: 12px; margin-bottom: 15px;
    }
    .valor { color: #00E676; font-size: 22px; font-weight: bold; }
    .local { color: #FFB300; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. BANCO DE DADOS DE MISSÕES (MAIS SERVIÇOS)
if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0
if 'status' not in st.session_state: st.session_state.status = "mural"

# --- SIDEBAR ---
with st.sidebar:
    st.title("👤 Geovani Santi")
    st.metric("Saldo do Dia", f"R$ {st.session_state.ganhos:.2f}")
    df_hist = pd.DataFrame({"Hora": ["12h", "14h", "16h", "Agora"], "R$": [50, 120, 80, st.session_state.ganhos]})
    fig = px.area(df_hist, x="Hora", y="R$", title="Fluxo de Caixa")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#FFF", height=200)
    st.plotly_chart(fig, use_container_width=True)

# --- MURAL DE MISSÕES EXPANDIDO ---
if st.session_state.status == "mural":
    st.title("📍 Radar de Missões - Osasco")
    t1, t2, t3, t4 = st.tabs(["🧹 Zeladoria", "🏥 Saúde", "♻️ Resíduos", "🎪 Logística"])
    
    with t1:
        # SERVIÇO 1
        st.markdown('<div class="card-trabalho"><b>Varrição de Vias Pública</b><br><span class="local">📍 Centro - Osasco</span><br><span class="valor">R$ 55.00</span></div>', unsafe_allow_html=True)
        if st.button("ACEITAR: VARRIÇÃO CENTRO", key="z1"):
            st.session_state.missao = {"nome": "Varrição", "valor": 55.0, "local": "Centro"}
            st.session_state.status = "gps"; st.rerun()
        
        # SERVIÇO 2
        st.markdown('<div class="card-trabalho"><b>Pintura de Meio-Fio</b><br><span class="local">📍 Bela Vista</span><br><span class="valor">R$ 85.00</span></div>', unsafe_allow_html=True)
        if st.button("ACEITAR: PINTURA BELA VISTA", key="z2"):
            st.session_state.missao = {"nome": "Pintura", "valor": 85.0, "local": "Bela Vista"}
            st.session_state.status = "gps"; st.rerun()

    with t2:
        # SERVIÇO 1
        st.markdown('<div class="card-trabalho"><b>Acompanhante Hospitalar</b><br><span class="local">📍 Vila Yara</span><br><span class="valor">R$ 150.00</span></div>', unsafe_allow_html=True)
        if st.button("ACEITAR: HOSP. VILA YARA", key="s1"):
            st.session_state.missao = {"nome": "Acompanhante", "valor": 150.0, "local": "Vila Yara"}
            st.session_state.status = "gps"; st.rerun()
        
        # SERVIÇO 2
        st.markdown('<div class="card-trabalho"><b>Cuidador em Domicílio</b><br><span class="local">📍 Campesina</span><br><span class="valor">R$ 200.00</span></div>', unsafe_allow_html=True)
        if st.button("ACEITAR: CUIDADOR CAMPESINA", key="s2"):
            st.session_state.missao = {"nome": "Cuidador", "valor": 200.0, "local": "Campesina"}
            st.session_state.status = "gps"; st.rerun()

    with t3:
        st.markdown('<div class="card-trabalho"><b>Triagem de Recicláveis</b><br><span class="local">📍 Mutinga</span><br><span class="valor">R$ 70.00</span></div>', unsafe_allow_html=True)
        if st.button("ACEITAR: TRIAGEM MUTINGA", key="r1"):
            st.session_state.missao = {"nome": "Triagem", "valor": 70.0, "local": "Mutinga"}
            st.session_state.status = "gps"; st.rerun()

    with t4:
        st.markdown('<div class="card-trabalho"><b>Montagem de Estrutura Evento</b><br><span class="local">📍 Arena Osasco</span><br><span class="valor">R$ 180.00</span></div>', unsafe_allow_html=True)
        if st.button("ACEITAR: ARENA OSASCO", key="l1"):
            st.session_state.missao = {"nome": "Montagem", "valor": 180.0, "local": "Arena Osasco"}
            st.session_state.status = "gps"; st.rerun()

elif st.session_state.status == "gps":
    st.header(f"🧭 Rota: {st.session_state.missao['local']}")
    st.info("O GPS está calculando a melhor rota para evitar o trânsito.")
    if st.button("✅ CHEGUEI NO DESTINO", key="cheguei"):
        st.session_state.status = "fotos"; st.rerun()

elif st.session_state.status == "fotos":
    st.header("📸 Validação por Imagem")
    st.camera_input("🤳 Selfie para Início", key="selfie")
    if st.button("🏁 TRABALHO CONCLUÍDO", key="fim"):
        st.session_state.ganhos += st.session_state.missao['valor']
        st.session_state.status = "mural"; st.rerun()
    
