import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS LuzSocial v11.0", page_icon="♻️", layout="wide")

# ESTILO CSS PREMIUM (DARK MODE)
st.markdown("""
    <style>
    .main { background-color: #0B0E14; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-image: linear-gradient(#050A30, #001219) !important; border-right: 1px solid #1A237E; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    .card-premium {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    .valor-liq { color: #00E676; font-size: 24px; font-weight: bold; }
    .badge-verde { background: #1B5E20; color: #69F0AE; padding: 4px 12px; border-radius: 50px; font-size: 11px; font-weight: bold; }
    .stButton>button { background: linear-gradient(90deg, #00D4FF, #0052D4); color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0
if 'status' not in st.session_state: st.session_state.status = "menu"

# --- LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("Usuário")
        s = st.text_input("Senha", type="password")
        if st.button("ACESSAR"):
            st.session_state.logado = True; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 👤 Geovani Santi")
    st.markdown(f"## 💰 R$ {st.session_state.saldo:.2f}")
    st.progress(min(st.session_state.saldo / 300.0, 1.0))
    st.divider()
    menu = st.radio("Selecione a Área:", ["Mural de Missões", "Meu Inventário", "Suporte"])
    if st.button("🚪 Sair"): st.session_state.logado = False; st.rerun()

# --- TELA: MURAL DE MISSÕES ---
if menu == "Mural de Missões":
    st.title("📍 Radar GS - Novas Oportunidades")
    
    tabs = st.tabs(["♻️ Reciclagem", "🩺 Saúde", "🧹 Zeladoria", "👨‍🍳 Cozinha", "🚚 Pequenos Fretes"])

    with tabs[0]: # RECICLAGEM
        vagas = [
            {"n": "Coleta de Óleo de Cozinha (10L)", "l": "Km 18", "b": 30.0, "k": "Bombonas GS"},
            {"n": "Recolha de Eletrônicos", "l": "Centro", "b": 50.0, "k": "Caixa de Proteção"},
            {"n": "Descarte de Entulho (5 sacos)", "l": "Rochdale", "b": 80.0, "k": "Carrinho de Mão e Luvas"}
        ]
        for v in vagas:
            liq = v['b'] * 0.90 # Menor imposto para incentivar ecologia
            st.markdown(f"""
                <div class="card-premium">
                    <span class="badge-verde">RECICLAGEM AMBIENTAL</span>
                    <h3>{v['n']}</h3>
                    <p>📍 {v['l']} | 📦 Kit: {v['k']}</p>
                    <div class="valor-liq">R$ {liq:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Aceitar Coleta: {v['n']}", key=v['n']):
                st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

    with tabs[4]: # FRETES
        v = {"n": "Entrega de Encomenda (Moto/Carro)", "l": "Vila Yara", "b": 45.0, "k": "Baú ou Porta-malas livre"}
        liq = v['b'] * 0.85
        st.markdown(f'<div class="card-premium"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
        if st.button("Aceitar Entrega"):
            st.session_state.missao_atual = {"nome": v['n'], "valor": liq}; st.session_state.status = "mapa"; st.rerun()

    # (Manter abas de Saúde, Cozinha e Zeladoria conforme versões anteriores)

# --- FLUXO DE TRABALHO ---
if st.session_state.status == "mapa":
    st.header(f"🗺️ Rota: {st.session_state.missao_atual['nome']}")
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("CHEGUEI"): st.session_state.status = "foto"; st.rerun()
elif st.session_state.status == "foto":
    st.camera_input("Prove o serviço com foto")
    if st.button("FINALIZAR"):
        st.session_state.saldo += st.session_state.missao_atual['valor']
        st.session_state.status = "pago"; st.rerun()
elif st.session_state.status == "pago":
    st.balloons(); st.success("Dinheiro na conta!"); st.button("Menu", on_click=lambda: setattr(st.session_state, 'status', 'menu'))
    
