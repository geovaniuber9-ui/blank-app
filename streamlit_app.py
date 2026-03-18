import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS Consultoria - Login Rápido", page_icon="🌱", layout="wide")

# --- ACESSO RÁPIDO SOLICITADO ---
USUARIO_CORRETO = "1"
SENHA_CORRETA = "1"

# 2. ESTILO VISUAL ECO (VERDE CLARO)
st.markdown("""
    <style>
    .stApp { background-color: #E8F5E9 !important; color: #1B5E20; }
    .card-trabalho {
        background: #FFFFFF; border: 2px solid #2E7D32;
        padding: 15px; border-radius: 12px; margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .titulo-card { color: #1B5E20; font-size: 18px; font-weight: bold; }
    .valor { color: #388E3C; font-size: 22px; font-weight: bold; }
    .local { color: #FFA000; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        color: white; border-radius: 10px; font-weight: bold; height: 3.5em; width: 100%;
        border: none;
    }
    .login-box {
        background: white; padding: 30px; border-radius: 15px;
        border: 2px solid #4CAF50; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONTROLE DE SESSÃO
if 'logado' not in st.session_state:
    st.session_state.logado = False

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.header("GS Consultoria 🌱")
        st.subheader("Acesso Restrito")
        
        user = st.text_input("Usuário (Dica: 1)")
        password = st.text_input("Senha (Dica: 1)", type="password")
        
        if st.button("ENTRAR"):
            if user == USUARIO_CORRETO and password == SENHA_CORRETA:
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("Dados incorretos!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- ÁREA LOGADA (SÓ APARECE APÓS LOGIN 1/1) ---

if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0
if 'status' not in st.session_state: st.session_state.status = "mural"

# SIDEBAR
with st.sidebar:
    st.title("👤 Geovani Santi")
    if st.button("SAIR"):
        st.session_state.logado = False
        st.rerun()
    st.metric("Ganhos Atuais", f"R$ {st.session_state.ganhos:.2f}")
    df_hist = pd.DataFrame({"Hora": ["12h", "14h", "16h", "Agora"], "R$": [50, 120, 80, st.session_state.ganhos]})
    fig = px.area(df_hist, x="Hora", y="R$", title="Fluxo de Caixa 🌱")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#1B5E20", height=200)
    st.plotly_chart(fig, use_container_width=True)

# MURAL DE MISSÕES (25 OPÇÕES)
if st.session_state.status == "mural":
    st.title("🌱 Radar GS - Osasco")
    t1, t2, t3, t4, t5 = st.tabs(["🧹 Zeladoria", "🏥 Saúde", "♻️ Resíduos", "🌳 Jardinagem", "🎪 Logística"])
    
    def criar_card(titulo, valor, local, chave):
        st.markdown(f'<div class="card-trabalho"><span class="titulo-card">{titulo}</span><br><span class="local">📍 {local}</span><br><span class="valor">R$ {valor:.2f}</span></div>', unsafe_allow_html=True)
        if st.button(f"ACEITAR: {titulo.upper()}", key=chave):
            st.session_state.missao = {"nome": titulo, "valor": valor, "local": local}
            st.session_state.status = "gps"; st.rerun()

    with t1:
        dados = [("Varrição de Vias", 55.0, "Centro"), ("Pintura de Meio-Fio", 85.0, "Bela Vista"), ("Limpeza de Bueiro", 75.0, "Rochdale"), ("Manutenção de Guia", 90.0, "Vila Yara"), ("Zeladoria Praça", 100.0, "Ayrosa")]
        for i, d in enumerate(dados): criar_card(d[0], d[1], d[2], f"z{i}")

    with t2:
        dados = [("Acompanhante Hosp.", 150.0, "Centro"), ("Cuidador Idoso", 200.0, "Campesina"), ("Instrumentador", 300.0, "Vila Yara"), ("Exames", 120.0, "Km 18"), ("Pós-Cirúrgico", 220.0, "Saúde")]
        for i, d in enumerate(dados): criar_card(d[0], d[1], d[2], f"s{i}")

    with t3:
        dados = [("Triagem Manual", 70.0, "Mutinga"), ("Coleta Seletiva", 65.0, "Industrial"), ("Triturador", 100.0, "Rochdale"), ("Resíduos Ind.", 150.0, "Km 18"), ("Triagem Vidro", 80.0, "Centro")]
        for i, d in enumerate(dados): criar_card(d[0], d[1], d[2], f"r{i}")

    with t4:
        dados = [("Roçagem Grama", 110.0, "Vila Yara"), ("Poda Árvore", 140.0, "Centro"), ("Poda Arbusto", 95.0, "Campesina"), ("Limpeza Jardim", 80.0, "Ayrosa"), ("Instalação Grama", 130.0, "Industrial")]
        for i, d in enumerate(dados): criar_card(d[0], d[1], d[2], f"j{i}")

    with t5:
        dados = [("Montagem Palco", 180.0, "Arena"), ("Instalação Cercas", 130.0, "Centro"), ("Empilhadeira", 200.0, "Industrial"), ("Carga/Descarga", 110.0, "Km 18"), ("Montagem Tendas", 140.0, "Vila Yara")]
        for i, d in enumerate(dados): criar_card(d[0], d[1], d[2], f"l{i}")

elif st.session_state.status == "gps":
    st.header(f"🧭 Rota: {st.session_state.missao['local']}")
    st.success("GPS Ativado!")
    if st.button("✅ CHEGUEI NO LOCAL"):
        st.session_state.status = "fotos"; st.rerun()

elif st.session_state.status == "fotos":
    st.header("📸 Validação")
    st.camera_input("🤳 Selfie para Validação", key="selfie")
    if st.button("🏁 TRABALHO CONCLUÍDO 🌱"):
        st.session_state.ganhos += st.session_state.missao['valor']
        st.session_state.status = "mural"; st.rerun()
    
