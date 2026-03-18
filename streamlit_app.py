import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS Consultoria Full", page_icon="⚡", layout="wide")

# 2. ESTILO VISUAL PREMIUM (DARK MODE + NEON)
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
    .stTabs [data-baseweb="tab-list"] button { font-size: 14px; color: #00D4FF; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. BANCO DE DADOS COMPLETO (TODOS OS SEGMENTOS)
if 'db_servicos' not in st.session_state:
    st.session_state.db_servicos = {
        "🧹 Zeladoria": [("Varrição de Vias", 55.0, "Centro"), ("Pintura de Guia", 90.0, "Vila Yara"), ("Limpeza Bueiro", 75.0, "Rochdale")],
        "♻️ Resíduos": [("Coleta Seletiva", 70.0, "Km 18"), ("Triagem Manual", 65.0, "Mutinga"), ("Gestão Resíduos", 120.0, "Industrial")],
        "🌱 Jardinagem": [("Roçagem Praça", 110.0, "Ayrosa"), ("Poda Árvore", 140.0, "Bela Vista"), ("Manutenção", 95.0, "Campesina")],
        "🎪 Logística": [("Montagem Palco", 200.0, "Arena"), ("Cercas/Grades", 130.0, "Centro"), ("Carga/Descarga", 110.0, "Poli")],
        "🏥 Saúde": [("Acompanhante", 150.0, "Regional"), ("Cuidador", 250.0, "Saúde"), ("Instrumentador", 300.0, "Centro")]
    }

# 4. CONTROLE DE ESTADO (PREVENÇÃO DE ERROS NO CELULAR)
if 'logado' not in st.session_state: st.session_state.logado = False
if 'status' not in st.session_state: st.session_state.status = "mural"
if 'missao' not in st.session_state: st.session_state.missao = None
if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0
if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame({"Dia": ["Seg", "Ter", "Qua", "Qui"], "R$": [150, 220, 190, 0]})

# --- FLUXO DE TELAS ---

# TELA 0: LOGIN
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center; color: #00D4FF;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    if st.button("ACESSAR DASHBOARD", key="main_login"):
        st.session_state.logado = True
        st.rerun()
    st.stop()

# SIDEBAR (GRÁFICO NEON)
with st.sidebar:
    st.title("👤 Geovani Santi")
    st.metric("Saldo Acumulado", f"R$ {st.session_state.ganhos:.2f}")
    st.markdown("### 📊 Desempenho")
    fig = px.bar(st.session_state.historico, x="Dia", y="R$", color_discrete_sequence=['#00D4FF'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#FFF", height=180, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    if st.button("🚪 Sair", key="logout"):
        st.session_state.logado = False; st.rerun()

# TELA 1: MURAL COMPLETO
if st.session_state.status == "mural":
    st.title("📍 Radar de Missões")
    categorias = list(st.session_state.db_servicos.keys())
    tabs = st.tabs(categorias)
    
    for i, cat in enumerate(categorias):
        with tabs[i]:
            for idx, (nome, valor, local) in enumerate(st.session_state.db_servicos[cat]):
                st.markdown(f'<div class="card-trabalho"><b>{nome}</b><br>📍 {local}<br><span class="valor">R$ {valor:.2f}</span></div>', unsafe_allow_html=True)
                # ID ÚNICO PARA NÃO DAR ERRO: cat + index
                if st.button(f"ACEITAR: {nome}", key=f"btn_{cat}_{idx}"):
                    st.session_state.missao = {"nome": nome, "valor": valor, "local": local}
                    st.session_state.status = "gps"; st.rerun()

# TELA 2: GPS
elif st.session_state.status == "gps":
    st.header(f"🧭 Destino: {st.session_state.missao['local']}")
    st.markdown(f'<a href="https://www.google.com/maps/search/{st.session_state.missao["local"]}+Osasco" target="_blank"><button style="background:#FFB300; color:black; width:100%; border-radius:12px; padding:15px; font-weight:bold; border:none; cursor:pointer;">🧭 ABRIR NO GOOGLE MAPS</button></a>', unsafe_allow_html=True)
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("✅ CHEGUEI NO LOCAL", key="arrive"):
        st.session_state.status = "fotos_entrada"; st.rerun()

# TELA 3: FOTOS ANTES (SELFIE + LOCAL)
elif st.session_state.status == "fotos_entrada":
    st.header("📸 Registro de Entrada")
    st.warning("Tire a Selfie e a Foto do Local para liberar o trabalho.")
    s = st.camera_input("🤳 Sua Selfie", key="selfie_in")
    a = st.camera_input("📷 Foto do Local (ANTES)", key="foto_antes")
    if s and a:
        if st.button("🚀 INICIAR TAREFA AGORA", key="start_work"):
            st.session_state.status = "em_andamento"; st.rerun()

# TELA 4: EM SERVIÇO (PÂNICO)
elif st.session_state.status == "em_andamento":
    st.success(f"👷 EM EXECUÇÃO: {st.session_state.missao['nome']}")
    if st.button("🚨 BOTÃO DE PÂNICO / AJUDA", key="panic"):
        st.error("Central notificada! Aguarde no local.")
    if st.button("🏁 FINALIZAR TRABALHO", key="finish_work"):
        st.session_state.status = "fotos_saida"; st.rerun()

# TELA 5: FOTO DEPOIS
elif st.session_state.status == "fotos_saida":
    st.header("📸 Registro de Entrega")
    st.info("Registre o resultado final para receber.")
    d = st.camera_input("📷 Foto do Serviço (DEPOIS)", key="foto_depois")
    if d:
        if st.button("💰 RECEBER PAGAMENTO", key="get_paid"):
            st.session_state.ganhos += st.session_state.missao['valor']
            st.session_state.status = "pago"; st.rerun()

# TELA 6: SUCESSO
elif st.session_state.status == "pago":
    st.balloons(); st.success("💎 Pagamento Creditado!");
    if st.button("VOLTAR AO MURAL", key="back_mural"):
        st.session_state.status = "mural"; st.rerun()
                            
