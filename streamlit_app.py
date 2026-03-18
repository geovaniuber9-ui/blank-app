import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS Consultoria v23", page_icon="⚡", layout="wide")

# 2. CSS DE ALTO CONTRASTE (Adeus telas escuras!)
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14 !important; color: #FFFFFF; }
    .card-trabalho {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid #00D4FF;
        padding: 15px; border-radius: 12px; margin-bottom: 12px;
    }
    .valor { color: #00E676; font-size: 24px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(90deg, #00D4FF, #0052D4);
        color: white; border-radius: 10px; font-weight: bold; height: 3.5em; width: 100%;
    }
    /* Deixa as abas (tabs) visíveis */
    .stTabs [data-baseweb="tab-list"] button { font-size: 18px; color: #00D4FF; }
    </style>
    """, unsafe_allow_html=True)

# 3. BANCO DE DADOS ROBUSTO (Para as abas não ficarem vazias)
servicos = {
    "🧹 Zeladoria": [("Varrição Centro", 50.0, "Osasco Centro"), ("Pintura de Guia", 85.0, "Vila Yara"), ("Limpeza Bueiro", 70.0, "Rochdale")],
    "♻️ Resíduos": [("Coleta Seletiva", 75.0, "Km 18"), ("Triagem Manual", 60.0, "Mutinga"), ("Resíduo Industrial", 120.0, "Industrial")],
    "🌱 Jardinagem": [("Corte de Grama", 100.0, "Bela Vista"), ("Poda de Árvore", 140.0, "City Bussocaba"), ("Plantio", 80.0, "IAPI")],
    "🎪 Logística": [("Montagem Palco", 200.0, "Arena"), ("Cerca de Evento", 130.0, "Centro"), ("Carga/Descarga", 110.0, "Poli")],
    "🏥 Saúde": [("Acompanhante", 150.0, "Hosp. Regional"), ("Cuidador", 250.0, "Saúde"), ("Instrumentador", 300.0, "Centro")]
}

# 4. INICIALIZAÇÃO DE ESTADO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'status' not in st.session_state: st.session_state.status = "mural"
if 'missao' not in st.session_state: st.session_state.missao = None
if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0
# Histórico inicial para o gráfico não nascer vazio
if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame({"Data": ["15/03", "16/03", "17/03", "18/03"], "R$": [120, 250, 180, 0]})

# --- LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    if st.button("ENTRAR NO DASHBOARD"):
        st.session_state.logado = True; st.rerun()
    st.stop()

# --- SIDEBAR COM GRÁFICO ULTRA VISÍVEL ---
with st.sidebar:
    st.title("👤 Geovani Santi")
    st.metric("Total Ganhos", f"R$ {st.session_state.ganhos:.2f}")
    
    st.markdown("### 📈 Produção Semanal")
    # Gráfico com cores neon para brilhar no fundo escuro
    fig = px.area(st.session_state.historico, x="Data", y="R$", 
                  color_discrete_sequence=['#00E676']) # Verde Lima
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color="#00D4FF", margin=dict(l=0, r=0, t=20, b=0), height=200,
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#333")
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    if st.button("🚪 Sair"):
        st.session_state.logado = False; st.rerun()

# --- FLUXO DE TELAS ---

if st.session_state.status == "mural":
    st.title("📍 Radar de Missões")
    tabs = st.tabs(list(servicos.keys()))
    
    for i, categoria in enumerate(servicos.keys()):
        with tabs[i]:
            for nome, valor, local in servicos[categoria]:
                st.markdown(f"""
                <div class="card-trabalho">
                    <b>{nome}</b><br>📍 {local}<br>
                    <span class="valor">R$ {valor:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"ACEITAR: {nome}", key=f"btn_{nome}_{local}_{i}"):
                    st.session_state.missao = {"nome": nome, "valor": valor, "local": local}
                    st.session_state.status = "gps"; st.rerun()

elif st.session_state.status == "gps":
    st.header(f"🧭 Rota: {st.session_state.missao['local']}")
    st.markdown(f'<a href="https://www.google.com/maps/search/{st.session_state.missao["local"]}+Osasco" target="_blank"><button style="background:#FFB300; color:black; width:100%; border-radius:12px; padding:15px; font-weight:bold; border:none; cursor:pointer;">🧭 ABRIR NO MAPS / WAZE</button></a>', unsafe_allow_html=True)
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("✅ CHEGUEI NO LOCAL"):
        st.session_state.status = "entrada"; st.rerun()

elif st.session_state.status == "entrada":
    st.header("📸 Validação de Início")
    st.info("Obrigatório: Selfie + Foto do local ANTES do serviço.")
    s = st.camera_input("🤳 Selfie")
    a = st.camera_input("📷 Foto do Local (ANTES)")
    if s and a:
        if st.button("🚀 INICIAR TRABALHO AGORA"):
            st.session_state.status = "trabalhando"; st.rerun()

elif st.session_state.status == "trabalhando":
    st.success(f"👷 EM EXECUÇÃO: {st.session_state.missao['nome']}")
    if st.button("🏁 FINALIZAR TRABALHO"):
        st.session_state.status = "saida"; st.rerun()

elif st.session_state.status == "saida":
    st.header("📸 Comprovação de Saída")
    st.info("Registre o DEPOIS para receber o pagamento.")
    d = st.camera_input("📷 Foto do Serviço (DEPOIS)")
    if d:
        if st.button("💰 RECEBER PAGAMENTO"):
            st.session_state.ganhos += st.session_state.missao['valor']
            # Atualiza gráfico
            hoje = pd.Timestamp.now().strftime("%d/%m")
            nova_data = pd.DataFrame({"Data": [hoje], "R$": [st.session_state.missao['valor']]})
            st.session_state.historico = pd.concat([st.session_state.historico, nova_data])
            st.session_state.status = "pago"; st.rerun()

elif st.session_state.status == "pago":
    st.balloons()
    st.success(f"Pagamento Confirmado! R$ {st.session_state.missao['valor']:.2f} na conta.")
    if st.button("VOLTAR AO MURAL"):
        st.session_state.status = "mural"; st.rerun()
