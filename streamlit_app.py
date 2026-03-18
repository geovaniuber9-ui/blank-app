import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="GS LuzSocial v8.7", page_icon="⚡", layout="wide")

# ESTILO CSS PARA LOGIN E MENU
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #050A30 !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    .stButton>button { border-radius: 10px; width: 100%; font-weight: bold; }
    .card { background-color: white; padding: 20px; border-radius: 15px; border-left: 10px solid #1A237E; margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); color: #333; }
    .liquido { color: #2e7d32; font-size: 22px; font-weight: bold; }
    .kit-box { background-color: #E3F2FD; padding: 12px; border-radius: 10px; border: 1px solid #2196F3; margin: 10px 0; color: #0D47A1; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO DE VARIÁVEIS DE SESSÃO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0
if 'status' not in st.session_state: st.session_state.status = "menu"

# --- TELA DE LOGIN (BLOQUEIO INICIAL) ---
if not st.session_state.logado:
    st.title("⚡ GS Consultoria")
    st.subheader("Login - LuzSocial Osasco")
    
    with st.container():
        user = st.text_input("Usuário ou CPF")
        senha = st.text_input("Senha", type="password")
        if st.button("ENTRAR NO SISTEMA"):
            if user != "" and senha != "": # Aqui podes definir um usuário específico depois
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("Por favor, preencha os campos corretamente.")
    st.stop() # Interrompe o código aqui se não estiver logado

# --- BARRA LATERAL (SÓ APARECE APÓS LOGIN) ---
with st.sidebar:
    st.markdown("# ⚡ GS CONSULTORIA")
    st.markdown(f"### 👤 Geovani Santi")
    st.markdown(f"## 💰 Saldo: R$ {st.session_state.saldo:.2f}")
    st.divider()
    
    escolha = st.radio("Menu Principal:", ["Mural de Missões", "Meus Equipamentos", "Suporte GS"])
    
    if st.button("🚪 Sair"):
        st.session_state.logado = False
        st.rerun()

# --- TELA 1: MURAL DE MISSÕES ---
if escolha == "Mural de Missões":
    st.title("📍 Radar de Chamados Próximos")
    st.info("🔔 Radar GS: 50+ missões encontradas perto de você!")
    
    abas = st.tabs(["🧹 Zeladoria", "🩺 Saúde/Cuidador", "🥘 Cozinha"])

    with abas[0]: # Zeladoria
        vagas = [{"n": "Limpeza de Jardim", "l": "Centro", "b": 60.0, "k": "Enxada, Tesoura de Poda e Sacos"}]
        for v in vagas:
            liq = v['b'] * 0.85
            st.markdown(f'<div class="card"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="kit-box">⚒️ Ferramentas: {v["k"]}</div><p class="liquido">R$ {liq:.2f} Líquido</p></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar {v['n']}", key=v['n']):
                st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

    with abas[1]: # Saúde
        vagas = [{"n": "Cuidador de Idoso", "l": "Km 18", "b": 220.0, "k": "Termômetro, Medidor de Pressão e Máscara"}]
        for v in vagas:
            liq = v['b'] * 0.85
            st.markdown(f'<div class="card"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="kit-box">🩺 Kit Saúde: {v["k"]}</div><p class="liquido">R$ {liq:.2f} Líquido</p></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar {v['n']}", key=f"s_{v['n']}"):
                st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

    with abas[2]: # Cozinha
        vagas = [{"n": "Auxiliar de Cozinha", "l": "Rochdale", "b": 130.0, "k": "Touca, Avental e Sapatos Antiderrapantes"}]
        for v in vagas:
            liq = v['b'] * 0.85
            st.markdown(f'<div class="card"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="kit-box">🥘 Kit Cozinha: {v["k"]}</div><p class="liquido">R$ {liq:.2f} Líquido</p></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar {v['n']}", key=f"c_{v['n']}"):
                st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

# --- TELA 2: EQUIPAMENTOS ---
elif escolha == "Meus Equipamentos":
    st.title("⚒️ Gestão de Ferramentas")
    st.write("Marque o que você já tem no seu kit GS:")
    st.checkbox("Vassoura e Pá")
    st.checkbox("Kit de Pressão (Saúde)")
    st.checkbox("Avental e Touca (Cozinha)")

# --- FLUXO DE TRABALHO ---
if st.session_state.status == "mapa":
    st.header(f"🗺️ Rota: {st.session_state.missao_atual['nome']}")
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("CHEGUEI"): st.session_state.status = "foto"; st.rerun()
elif st.session_state.status == "foto":
    st.camera_input("Foto do serviço")
    if st.button("CONCLUIR"):
        st.session_state.saldo += st.session_state.missao_atual['valor']
        st.session_state.status = "pago"; st.rerun()
elif st.session_state.status == "pago":
    st.balloons(); st.success("Pago!"); st.button("Voltar", on_click=lambda: setattr(st.session_state, 'status', 'menu'))
    
