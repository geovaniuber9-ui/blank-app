import streamlit as st
import time
import pandas as pd

# 1. CONFIGURAÇÃO E ESTILO AVANÇADO
st.set_page_config(page_title="GS Radar Super Pro", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #E8F5E9 !important; }
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .status-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 6px solid #2E7D32; margin-bottom: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08); position: relative;
    }
    .urgent-card {
        border: 2px solid #FFD700 !important;
        background-color: #FFFDF0 !important;
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.4) !important;
    }
    .urgent-label {
        background: #FFD700; color: #000; font-size: 10px; font-weight: bold;
        padding: 2px 10px; border-radius: 5px; position: absolute; top: 10px; right: 10px;
    }
    .verified-badge { color: #1E88E5; font-weight: bold; font-size: 11px; background: #E3F2FD; padding: 4px 8px; border-radius: 10px; }
    .price-tag { color: #2E7D32; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE DADOS
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 100.00
if 'missoes' not in st.session_state: st.session_state.missoes = []
if 'historico' not in st.session_state: st.session_state.historico = []

# --- 3. LOGIN ---
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("ACESSAR SISTEMA", use_container_width=True):
        if user == "1" and password == "1":
            st.session_state.logado = True
            st.rerun()
    st.stop()

# --- 4. BARRA LATERAL MULTIFUNÇÕES ---
with st.sidebar:
    st.markdown(f'<div class="wallet-box"><small>SALDO DISPONÍVEL</small><br><span style="font-size: 28px;">R$ {st.session_state.saldo:.2f}</span></div>', unsafe_allow_html=True)
    
    menu = st.selectbox("Navegação", ["🚀 Radar de Missões", "🏢 Painel da Empresa", "📊 Meus Ganhos", "🏆 Ranking GS", "🔗 Indique e Ganhe"])
    
    st.divider()
    with st.expander("💳 Recarregar"):
        v_rec = st.number_input("Valor", min_value=10.0)
        if st.button("Gerar Pix"): st.image("https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=GS")
    
    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()

# --- 5. MODO RADAR (PRESTADOR) ---
if menu == "🚀 Radar de Missões":
    st.title("📲 Radar em Tempo Real")
    
    tabs = st.tabs(["🧹 Zeladoria", "🛠️ Reparos", "💅 Beleza", "🏠 Diarista", "🏥 Saúde"])
    
    for i, tab in enumerate(tabs):
        with tab:
            # Categorias mapeadas
            cat_map = ["Zeladoria", "Reparos", "Beleza", "Diarista", "Saúde"]
            servicos = [m for m in st.session_state.missoes if m['cat'] == cat_map[i]]
            
            if not servicos:
                st.info("Buscando novos sinais no radar...")
            else:
                for idx, m in enumerate(servicos):
                    urgent_class = "urgent-card" if m['urgente'] else ""
                    st.markdown(f"""
                    <div class="status-card {urgent_class}">
                        {f'<div class="urgent-label">⚡ URGENTE</div>' if m['urgente'] else ''}
                        <div style="display: flex; justify-content: space-between;">
                            <span style="font-size:12px;"><b>{m['empresa']}</b></span>
                            { '<span class="verified-badge">✅ VERIFICADA</span>' if m['cpf'] else '' }
                        </div>
                        <h3 style="margin:5px 0;">{m['serv']}</h3>
                        <p style="font-size:14px; color:#555;">📍 {m['loc']}</p>
                        <div class="price-tag">R$ {m['val']:.2f}</div>
                        <p><small>💰 {m['pag']} | 👤 {m['nome_resp']}</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c1, c2, c3 = st.columns(3)
                    with c1: 
                        if st.button("✅ ACEITAR", key=f"ac_{idx}_{i}"):
                            st.session_state.historico.append(m)
                            st.success("Missão aceita!")
                    with c2: st.button("💬 CHAT", key=f"ch_{idx}_{i}")
                    with c3: st.button("🗺️ MAPA", key=f"mp_{idx}_{i}")

# --- 6. PAINEL DA EMPRESA ---
elif menu == "🏢 Painel da Empresa":
    st.title("🏢 Lançar Serviço")
    with st.form("new_os"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.text_input("Empresa", value="GS Consultoria")
            resp = st.text_input("Responsável")
            cpf = st.text_input("CPF (Selo Verificado)")
        with col2:
            cat = st.selectbox("Categoria", ["Zeladoria", "Reparos", "Beleza", "Diarista", "Saúde"])
            valor = st.number_input("Valor ao Prestador", min_value=1.0)
            pag = st.selectbox("Pagamento", ["Pix", "Máquina", "Dinheiro"])
        
        serv = st.text_input("Descrição do Serviço")
        loc = st.text_input("Localização")
        urgente = st.checkbox("⚡ IMPULSIONAR (URGENTE) - Custo: R$ 5,00")
        
        taxa = (valor * 0.07) + (5.0 if urgente else 0)
        st.warning(f"Total de taxas para publicação: R$ {taxa:.2f}")
        
        if st.form_submit_button("🚀 LANÇAR NO RADAR"):
            if st.session_state.saldo >= taxa:
                st.session_state.saldo -= taxa
                st.session_state.missoes.append({
                    "empresa": emp, "nome_resp": resp, "cpf": cpf, "
    
