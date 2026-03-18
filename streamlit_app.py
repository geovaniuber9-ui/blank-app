import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS Consultoria v22", page_icon="⚡", layout="wide")

# 2. CSS PARA FORÇAR O DARK MODE E CORES VIBRANTES
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14 !important; color: #E0E0E0; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1A237E; border-radius: 10px; padding: 10px; color: white;
    }
    .card-trabalho {
        background: rgba(255, 255, 255, 0.08);
        border-left: 5px solid #00D4FF;
        padding: 15px; border-radius: 10px; margin-bottom: 12px;
    }
    .valor { color: #00E676; font-size: 24px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(90deg, #00D4FF, #0052D4);
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INICIALIZAÇÃO SEGURA DE VARIÁVEIS
if 'logado' not in st.session_state: st.session_state.logado = False
if 'status' not in st.session_state: st.session_state.status = "mural"
if 'missao' not in st.session_state: st.session_state.missao = None
if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0
if 'historico' not in st.session_state: 
    st.session_state.historico = pd.DataFrame({"Dia": ["Seg", "Ter", "Qua"], "R$": [0, 0, 0]})

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center; color: #00D4FF;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    if st.button("ENTRAR NO SISTEMA"):
        st.session_state.logado = True
        st.rerun()
    st.stop()

# --- SIDEBAR COM GRÁFICO REFEITO ---
with st.sidebar:
    st.title("👤 Geovani Santi")
    st.metric("Saldo Atual", f"R$ {st.session_state.ganhos:.2f}")
    
    st.markdown("### 📊 Ganhos Semanais")
    fig = px.line(st.session_state.historico, x="Dia", y="R$", markers=True)
    fig.update_traces(line_color='#00E676', line_width=4, marker=dict(size=10, color="#00D4FF"))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color="#FFFFFF", margin=dict(l=0, r=0, t=10, b=0), height=180,
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#333")
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    if st.button("🚪 Sair"):
        st.session_state.logado = False
        st.rerun()

# --- FLUXO DE TELAS (CORRIGIDO) ---

# TELA 1: MURAL
if st.session_state.status == "mural":
    st.title("📍 Missões em Osasco")
    
    # Categorias solicitadas
    cat_nomes = ["🧹 Zeladoria", "♻️ Resíduos", "🌱 Jardinagem", "🎪 Eventos", "🏥 Saúde"]
    tabs = st.tabs(cat_nomes)
    
    missoes_lista = [
        [("Varrição Praça ABC", 50.0, "Centro"), ("Pintura de Guia", 90.0, "Vila Yara")],
        [("Coleta Seletiva", 75.0, "Rochdale"), ("Triagem Resíduos", 60.0, "Mutinga")],
        [("Roçagem Terreno", 110.0, "Ayrosa"), ("Poda Árvore", 130.0, "Bela Vista")],
        [("Montagem Palco", 180.0, "Centro"), ("Cercas Evento", 140.0, "Poli")],
        [("Acompanhante", 120.0, "Saúde"), ("Instrumentador", 250.0, "Km 18")]
    ]

    for i, tab in enumerate(tabs):
        with tab:
            for nome, valor, local in missoes_lista[i]:
                st.markdown(f'<div class="card-trabalho"><b>{nome}</b><br>📍 {local}<br><span class="valor">R$ {valor:.2f}</span></div>', unsafe_allow_html=True)
                if st.button(f"ACEITAR: {nome}", key=f"btn_{nome}_{local}"):
                    st.session_state.missao = {"nome": nome, "valor": valor, "local": local}
                    st.session_state.status = "gps"
                    st.rerun()

# TELA 2: GPS
elif st.session_state.status == "gps":
    st.header(f"🧭 Rota: {st.session_state.missao['local']}")
    st.markdown(f'<a href="https://www.google.com/maps/search/{st.session_state.missao["local"]}+Osasco" target="_blank"><button style="background:#FFB300; color:black; width:100%; border-radius:12px; padding:15px; font-weight:bold; border:none;">🧭 ABRIR NO GOOGLE MAPS</button></a>', unsafe_allow_html=True)
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("✅ CHEGUEI NO LOCAL"):
        st.session_state.status = "fotos_inicio"
        st.rerun()

# TELA 3: FOTOS ANTES
elif st.session_state.status == "fotos_inicio":
    st.header("📸 Registro de Entrada")
    st.warning("Envie a Selfie e a Foto do ANTES para começar.")
    s = st.camera_input("🤳 Selfie")
    a = st.camera_input("📷 Foto do Local (ANTES)")
    if s and a:
        if st.button("🚀 INICIAR TRABALHO"):
            st.session_state.status = "trabalhando"
            st.rerun()

# TELA 4: TRABALHANDO
elif st.session_state.status == "trabalhando":
    st.success(f"👷 EM EXECUÇÃO: {st.session_state.missao['nome']}")
    if st.button("🚨 EMERGÊNCIA"): st.error("Suporte acionado!")
    if st.button("🏁 FINALIZAR SERVIÇO"):
        st.session_state.status = "foto_depois"
        st.rerun()

# TELA 5: FOTO DEPOIS
elif st.session_state.status == "foto_depois":
    st.header("📸 Foto Final")
    d = st.camera_input("📷 Foto do DEPOIS")
    if d:
        if st.button("💰 RECEBER PAGAMENTO"):
            st.session_state.ganhos += st.session_state.missao['valor']
            st.session_state.status = "sucesso"
            st.rerun()

# TELA 6: SUCESSO
elif st.session_state.status == "sucesso":
    st.balloons()
    st.success(f"Pagamento de R$ {st.session_state.missao['valor']:.2f} realizado!")
    if st.button("VOLTAR AO MURAL"):
        st.session_state.status = "mural"
        st.rerun()
        
