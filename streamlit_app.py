import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS Consultoria v24", page_icon="⚡", layout="wide")

# 2. ESTILO DARK MODE COM CONTRASTE REALÇADO
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14 !important; color: #FFFFFF; }
    .card-trabalho {
        background: rgba(0, 212, 255, 0.1);
        border: 2px solid #1A237E;
        padding: 15px; border-radius: 12px; margin-bottom: 10px;
    }
    .valor { color: #00E676; font-size: 24px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(90deg, #00D4FF, #0052D4);
        color: white; border-radius: 10px; font-weight: bold; height: 3.5em; width: 100%;
    }
    .stTabs [data-baseweb="tab-list"] button { font-size: 16px; color: #00D4FF; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. BANCO DE DADOS FIXO
servicos_data = {
    "🧹 Zeladoria": [("Varrição Centro", 55.0, "Centro"), ("Pintura Guia", 90.0, "Vila Yara")],
    "♻️ Resíduos": [("Coleta Seletiva", 75.0, "Rochdale"), ("Triagem", 65.0, "Mutinga")],
    "🌱 Jardinagem": [("Roçagem", 110.0, "Ayrosa"), ("Poda", 140.0, "Bela Vista")],
    "🎪 Logística": [("Montagem Palco", 200.0, "Centro"), ("Cercas", 130.0, "Poli")],
    "🏥 Saúde": [("Acompanhante", 150.0, "Hosp. Regional"), ("Cuidador", 250.0, "Saúde")]
}

# 4. INICIALIZAÇÃO DE ESTADOS (Prevenção de KeyError)
if 'logado' not in st.session_state: st.session_state.logado = False
if 'status' not in st.session_state: st.session_state.status = "mural"
if 'missao' not in st.session_state: st.session_state.missao = None
if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0
if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame({"Dia": ["Seg", "Ter", "Qua", "Qui"], "R$": [150, 220, 190, 0]})

# --- LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    if st.button("ACESSAR SISTEMA"):
        st.session_state.logado = True; st.rerun()
    st.stop()

# --- SIDEBAR COM GRÁFICO REFEITO ---
with st.sidebar:
    st.title("👤 Geovani Santi")
    st.metric("Total Ganhos", f"R$ {st.session_state.ganhos:.2f}")
    st.markdown("### 📊 Desempenho")
    # Gráfico em azul neon para visibilidade total
    fig = px.bar(st.session_state.historico, x="Dia", y="R$", color_discrete_sequence=['#00D4FF'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#FFF", height=180, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    if st.button("🚪 Sair"): st.session_state.logado = False; st.rerun()

# --- FLUXO DE TELAS ---

if st.session_state.status == "mural":
    st.title("📍 Radar de Missões")
    tabs = st.tabs(list(servicos_data.keys()))
    
    for i, categoria in enumerate(servicos_data.keys()):
        with tabs[i]:
            for idx, (nome, valor, local) in enumerate(servicos_data[categoria]):
                st.markdown(f'<div class="card-trabalho"><b>{nome}</b><br>📍 {local}<br><span class="valor">R$ {valor:.2f}</span></div>', unsafe_allow_html=True)
                # Criando uma chave única para cada botão para evitar o KeyError
                if st.button(f"ACEITAR: {nome}", key=f"btn_{i}_{idx}"):
                    st.session_state.missao = {"nome": nome, "valor": valor, "local": local}
                    st.session_state.status = "gps"; st.rerun()

elif st.session_state.status == "gps":
    st.header(f"🧭 Destino: {st.session_state.missao['local']}")
    st.markdown(f'<a href="https://www.google.com/maps/search/{st.session_state.missao["local"]}+Osasco" target="_blank"><button style="background:#FFB300; color:black; width:100%; border-radius:12px; padding:15px; font-weight:bold; border:none; cursor:pointer;">🧭 ABRIR NO MAPS / WAZE</button></a>', unsafe_allow_html=True)
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("✅ CHEGUEI NO LOCAL"):
        st.session_state.status = "fotos_entrada"; st.rerun()

elif st.session_state.status == "fotos_entrada":
    st.header("📸 Registro de Entrada")
    s = st.camera_input("🤳 Sua Selfie")
    a = st.camera_input("📷 Foto do Local (ANTES)")
    if s and a:
        if st.button("🚀 INICIAR TRABALHO"):
            st.session_state.status = "trabalhando"; st.rerun()

elif st.session_state.status == "trabalhando":
    st.success(f"👷 EM EXECUÇÃO: {st.session_state.missao['nome']}")
    if st.button("🏁 FINALIZAR SERVIÇO"):
        st.session_state.status = "foto_saida"; st.rerun()

elif st.session_state.status == "foto_saida":
    st.header("📸 Registro de Saída")
    d = st.camera_input("📷 Foto do Serviço (DEPOIS)")
    if d:
        if st.button("💰 RECEBER PAGAMENTO"):
            st.session_state.ganhos += st.session_state.missao['valor']
            st.session_state.status = "sucesso"; st.rerun()

elif st.session_state.status == "sucesso":
    st.balloons(); st.success("Pagamento Creditado!");
    if st.button("VOLTAR AO MURAL"): st.session_state.status = "mural"; st.rerun()
