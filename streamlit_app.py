import streamlit as st
import pandas as pd

# CONFIGURAÇÃO
st.set_page_config(page_title="GS LuzSocial v9.0", page_icon="⚡", layout="wide")

# ESTILO CSS (FOCO NO MENU AZUL ESCURO E CARDS CLAROS)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #050A30 !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    .card { background-color: white; padding: 20px; border-radius: 15px; border-left: 10px solid #1A237E; margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); color: #333; }
    .liquido { color: #2e7d32; font-size: 22px; font-weight: bold; }
    .meta-box { background-color: #E8F5E9; padding: 15px; border-radius: 10px; border: 1px solid #4CAF50; text-align: center; margin-bottom: 20px; }
    .kit-info { background-color: #E3F2FD; padding: 10px; border-radius: 8px; border: 1px solid #2196F3; font-weight: bold; color: #0D47A1; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0
if 'status' not in st.session_state: st.session_state.status = "menu"
if 'meta_diaria' not in st.session_state: st.session_state.meta_diaria = 150.0

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.title("⚡ GS Consultoria - LuzSocial")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Acesso Restrito")
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.button("ENTRAR"):
            st.session_state.logado = True
            st.rerun()
    st.stop()

# --- SIDEBAR (MENU AZUL ESCURO) ---
with st.sidebar:
    st.markdown("# ⚡ GS CONSULTORIA")
    st.markdown(f"### 👤 Geovani Santi")
    st.markdown(f"## 💰 Saldo: R$ {st.session_state.saldo:.2f}")
    st.divider()
    
    escolha = st.radio("Navegar:", ["Mural de Missões", "Minha Meta", "Equipamentos", "Suporte"])
    
    st.divider()
    if st.button("🚨 PÂNICO"): st.error("SOCORRO ATIVADO!")
    if st.button("🚪 Sair"): 
        st.session_state.logado = False
        st.rerun()

# --- TELA 1: MURAL DE MISSÕES COM KITS ---
if escolha == "Mural de Missões":
    st.title("📍 Radar de Oportunidades")
    st.warning("🔔 RADAR: 50+ chamados abertos em Osasco agora!")
    
    tab1, tab2, tab3 = st.tabs(["🧹 Zeladoria", "🩺 Saúde", "🥘 Cozinha"])

    with tab1:
        v = {"n": "Jardinagem Completa", "l": "Bela Vista", "b": 100.0, "k": "Enxada, Tesoura e Sacos"}
        liq = v['b'] * 0.85
        st.markdown(f'<div class="card"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="kit-info">⚒️ Kit: {v["k"]}</div><p class="liquido">R$ {liq:.2f} Líquido</p></div>', unsafe_allow_html=True)
        if st.button("Aceitar Jardinagem"): 
            st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

    with tab2:
        v = {"n": "Acompanhante Cuidador", "l": "Centro", "b": 200.0, "k": "Aparelho de Pressão e Termômetro"}
        liq = v['b'] * 0.85
        st.markdown(f'<div class="card"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="kit-info">🩺 Kit Saúde: {v["k"]}</div><p class="liquido">R$ {liq:.2f} Líquido</p></div>', unsafe_allow_html=True)
        if st.button("Aceitar Cuidador"): 
            st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

# --- TELA 2: METAS ---
elif escolha == "Minha Meta":
    st.title("🎯 Minha Meta de Ganho")
    meta = st.number_input("Quanto quer ganhar hoje?", value=st.session_state.meta_diaria)
    falta = meta - st.session_state.saldo
    progresso = min(st.session_state.saldo / meta, 1.0)
    
    st.markdown(f"""
        <div class="meta-box">
            <h4>Seu Progresso de Hoje</h4>
            <h2 style="color: #2e7d32">R$ {st.session_state.saldo:.2f} de R$ {meta:.2f}</h2>
            <p>Faltam <b>R$ {max(falta, 0):.2f}</b> para bater sua meta!</p>
        </div>
    """, unsafe_allow_html=True)
    st.progress(progresso)

# --- TELA 3: EQUIPAMENTOS ---
elif escolha == "Equipamentos":
    st.title("⚒️ Meus Equipamentos GS")
    st.write("Verifique se seus kits estão completos para não ser penalizado.")
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Vassoura/Pá", value=True)
        st.checkbox("Aparelho de Pressão")
    with col2:
        st.checkbox("Avental/Touca", value=True)
        st.checkbox("Celular Carregado", value=True)

# --- TELA 4: SUPORTE ---
elif escolha == "Suporte":
    st.title("📞 Central Geovani")
    st.markdown(f'<a href="https://wa.me/5511917529636" style="text-decoration:none"><div class="card" style="background-color:#25D366; color:white; text-align:center">💬 FALAR NO WHATSAPP</div></a>', unsafe_allow_html=True)

# --- FLUXO DE MISSÃO ---
if st.session_state.status == "mapa":
    st.header(f"📍 Destino: {st.session_state.missao_atual['nome']}")
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("CHEGUEI"): st.session_state.status = "foto"; st.rerun()
elif st.session_state.status == "foto":
    st.camera_input("Foto da conclusão")
    if st.button("FINALIZAR"):
        st.session_state.saldo += st.session_state.missao_atual['valor']
        st.session_state.status = "pago"; st.rerun()
elif st.session_state.status == "pago":
    st.balloons(); st.success("Dinheiro na conta!"); st.button("Menu", on_click=lambda: setattr(st.session_state, 'status', 'menu'))
    
