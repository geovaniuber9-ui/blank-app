import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS LuzSocial v12.0", page_icon="⚡", layout="wide")

# ESTILO PREMIUM (DARK MODE)
st.markdown("""
    <style>
    .main { background-color: #0B0E14; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-image: linear-gradient(#050A30, #001219) !important; border-right: 1px solid #1A237E; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    .card-premium {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; margin-bottom: 15px;
    }
    .valor-liq { color: #00E676; font-size: 24px; font-weight: bold; }
    .urgente { border: 1px solid #FF5252; box-shadow: 0px 0px 10px rgba(255, 82, 82, 0.3); }
    .badge { padding: 4px 10px; border-radius: 50px; font-size: 11px; font-weight: bold; text-transform: uppercase; }
    .stButton>button { background: linear-gradient(90deg, #00D4FF, #0052D4); color: white; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0
if 'status' not in st.session_state: st.session_state.status = "menu"

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    u = st.text_input("Usuário (CPF)")
    s = st.text_input("Senha", type="password")
    if st.button("ACESSAR SISTEMA"):
        st.session_state.logado = True; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 👤 Geovani Santi")
    st.markdown(f"## 💰 Saldo: R$ {st.session_state.saldo:.2f}")
    st.divider()
    menu = st.radio("Ir para:", ["Mural de Missões", "Escola de Profissões", "Meu Inventário", "Suporte"])
    if st.button("🚪 Sair"): st.session_state.logado = False; st.rerun()

# --- TELA: MURAL DE MISSÕES ---
if menu == "Mural de Missões":
    st.title("📍 Novas Oportunidades")
    tabs = st.tabs(["♻️ Reciclagem", "🩺 Saúde", "🧹 Zeladoria", "👩‍🍳 Cozinha"])

    with tabs[0]: # RECICLAGEM
        vagas = [
            {"n": "Coleta de Óleo (10L)", "l": "Km 18", "b": 30.0, "k": "Bombonas GS"},
            {"n": "Recolha de Eletrônicos", "l": "Centro", "b": 45.0, "k": "Caixa de Proteção"}
        ]
        for v in vagas:
            liq = v['b'] * 0.90
            st.markdown(f'<div class="card-premium"><span class="badge" style="background:#1B5E20">Ambiental</span><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar {v['n']}"): st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

    with tabs[1]: # SAÚDE
        vagas = [
            {"n": "Acompanhante Idoso (4h)", "l": "Vila Yara", "b": 120.0, "k": "Medidor de Pressão/Termômetro", "u": True},
            {"n": "Auxiliar de Curativos", "l": "Km 18", "b": 80.0, "k": "Kit Primeiros Socorros GS", "u": False}
        ]
        for v in vagas:
            liq = v['b'] * 0.85
            estilo = "card-premium urgente" if v['u'] else "card-premium"
            st.markdown(f'<div class="{estilo}"><span class="badge" style="background:#B71C1C">Saúde</span><h3>{v["n"]} {"🚨" if v["u"] else ""}</h3><p>📍 {v["l"]} | 📦 {v["k"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar {v['n']}"): st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

    with tabs[2]: # ZELADORIA
        vagas = [
            {"n": "Varrição de Praça", "l": "Centro (Matriz)", "b": 35.0, "k": "Vassoura e Pá Profissional"},
            {"n": "Limpeza de Bueiro", "l": "Rochdale", "b": 75.0, "k": "Luvas e Gancho de Metal", "u": True}
        ]
        for v in vagas:
            liq = v['b'] * 0.85
            st.markdown(f'<div class="card-premium"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar {v['n']}"): st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

    with tabs[3]: # COZINHA
        vagas = [
            {"n": "Preparo de Marmitas (Dia)", "l": "Bela Vista", "b": 150.0, "k": "Touca e Avental GS"},
            {"n": "Auxiliar de Churrasqueiro", "l": "Km 18", "b": 100.0, "k": "Kit Churrasco GS"}
        ]
        for v in vagas:
            liq = v['b'] * 0.85
            st.markdown(f'<div class="card-premium"><span class="badge" style="background:#E65100">Cozinha</span><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar {v['n']}"): st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

# --- ESCOLA DE PROFISSÕES ---
elif menu == "Escola de Profissões":
    st.title("🎓 Escola de Profissões GS")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Exemplo: Link de tutorial
    st.markdown("### Cursos Disponíveis:")
    st.button("📜 Certificado: Cuidador Básico")
    st.button("📜 Certificado: Higiene Alimentar")

# --- MAPA E FOTO ---
if st.session_state.status == "mapa":
    st.header(f"📍 Rota: {st.session_state.missao_atual['nome']}")
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("CHEGUEI"): st.session_state.status = "foto"; st.rerun()
elif st.session_state.status == "foto":
    st.camera_input("Foto do serviço pronto")
    if st.button("FINALIZAR"):
        st.session_state.saldo += st.session_state.missao_atual['valor']
        st.session_state.status = "pago"; st.rerun()
elif st.session_state.status == "pago":
    st.balloons(); st.button("Menu", on_click=lambda: setattr(st.session_state, 'status', 'menu'))
             
