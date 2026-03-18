import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO E ESTILO DE ALTO CONTRASTE
st.set_page_config(page_title="GS Consultoria v21.0", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
    .card-trabalho {
        background: rgba(255, 255, 255, 0.07);
        border-left: 5px solid #00D4FF;
        padding: 15px; border-radius: 10px; margin-bottom: 12px;
    }
    .valor { color: #00E676; font-size: 22px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(90deg, #00D4FF, #0052D4);
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em;
    }
    /* Estilo para labels de gráficos */
    .stPlotlyChart { border: 1px solid #1A237E; border-radius: 15px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS E CATEGORIAS
dados_trabalhos = {
    "🧹 Zeladoria": [("Varrição de Praças", 48.0, "Centro"), ("Limpeza de Bueiro", 80.0, "Rochdale")],
    "♻️ Resíduos": [("Coleta Seletiva", 70.0, "Km 18"), ("Triagem", 60.0, "Mutinga")],
    "🌱 Jardinagem": [("Roçagem", 90.0, "Ayrosa"), ("Poda", 115.0, "Campesina")],
    "🎪 Logística": [("Montagem de Palco", 160.0, "Centro"), ("Cercas", 120.0, "Poli")],
    "🏥 Saúde": [("Acompanhante", 130.0, "Vila Yara"), ("Cuidador", 220.0, "Adalgisa")]
}

# 3. CONTROLE DE ESTADOS
if 'logado' not in st.session_state: st.session_state.logado = False
if 'status' not in st.session_state: st.session_state.status = "mural"
if 'missao' not in st.session_state: st.session_state.missao = None
if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0
if 'historico' not in st.session_state: 
    st.session_state.historico = pd.DataFrame(columns=["Data", "Serviço", "Valor"])

# --- LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center; color: #00D4FF;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    if st.button("ACESSAR DASHBOARD"):
        st.session_state.logado = True; st.rerun()
    st.stop()

# --- SIDEBAR COM GRÁFICO CLARO ---
with st.sidebar:
    st.title("👤 Geovani Santi")
    st.metric("Total Acumulado", f"R$ {st.session_state.ganhos:.2f}")
    
    if not st.session_state.historico.empty:
        st.markdown("---")
        st.subheader("📊 Desempenho")
        # Gráfico com cores vibrantes para não ficar escuro
        fig = px.bar(st.session_state.historico, x="Data", y="Valor", 
                     color_discrete_sequence=['#00D4FF'])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#FFFFFF",
            margin=dict(l=0, r=0, t=20, b=0),
            height=200
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    if st.button("🚪 Sair"):
        st.session_state.logado = False; st.rerun()

# --- FLUXO PRINCIPAL ---

if st.session_state.status == "mural":
    st.title("📍 Mural de Missões")
    tabs = st.tabs(list(dados_trabalhos.keys()))
    for i, cat in enumerate(dados_trabalhos.keys()):
        with tabs[i]:
            for nome, valor, local in dados_trabalhos[cat]:
                st.markdown(f'<div class="card-trabalho"><b>{nome}</b><br>📍 {local}<br><span class="valor">R$ {valor:.2f}</span></div>', unsafe_allow_html=True)
                if st.button(f"ACEITAR: {nome}", key=f"{nome}_{local}"):
                    st.session_state.missao = {"nome": nome, "valor": valor, "local": local}
                    st.session_state.status = "gps"; st.rerun()

elif st.session_state.status == "gps":
    st.header(f"🧭 Destino: {st.session_state.missao['local']}")
    st.markdown(f'<a href="https://www.google.com/maps/search/{st.session_state.missao["local"]}+Osasco" target="_blank"><button style="background:#FFB300; width:100%; border-radius:12px; padding:15px; font-weight:bold; border:none; color:black;">🧭 ABRIR GPS</button></a>', unsafe_allow_html=True)
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("✅ CHEGUEI NO LOCAL"):
        st.session_state.status = "antes"; st.rerun()

elif st.session_state.status == "antes":
    st.header("📸 Registro de Entrada")
    st.warning("Tire a Selfie e a Foto do ANTES para liberar o serviço.")
    s = st.camera_input("🤳 Sua Selfie")
    a = st.camera_input("📷 Foto do Local (ANTES)")
    if s and a:
        if st.button("🚀 INICIAR TRABALHO"):
            st.session_state.status = "executando"; st.rerun()

elif st.session_state.status == "executando":
    st.success(f"👷 EM EXECUÇÃO: {st.session_state.missao['nome']}")
    if st.button("🚨 BOTÃO DE PÂNICO", type="secondary"):
        st.error("Alerta enviado à central GS!")
    if st.button("🏁 FINALIZAR TRABALHO"):
        st.session_state.status = "depois"; st.rerun()

elif st.session_state.status == "depois":
    st.header("📸 Registro de Saída")
    d = st.camera_input("📷 Foto do Serviço CONCLUÍDO")
    if d:
        if st.button("💎 FINALIZAR E RECEBER"):
            # Adiciona ao histórico para o gráfico
            nova_linha = pd.DataFrame({"Data": [pd.Timestamp.now().strftime("%d/%m")], 
                                      "Serviço": [st.session_state.missao['nome']], 
                                      "Valor": [st.session_state.missao['valor']]})
            st.session_state.historico = pd.concat([st.session_state.historico, nova_linha])
            st.session_state.ganhos += st.session_state.missao['valor']
            st.session_state.status = "pago"; st.rerun()

elif st.session_state.status == "pago":
    st.balloons()
    st.success("Pagamento Creditado!")
    if st.button("VOLTAR AO MURAL"):
        st.session_state.status = "mural"; st.rerun()
    
