import streamlit as st
import time
import pandas as pd

# 1. CONFIGURAÇÃO E ESTILO (AGORA COM FUNDO DE SP)
st.set_page_config(page_title="GS Radar Master", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    /* Imagem de fundo de São Paulo com opacidade */
    .stApp {
        background: linear-gradient(rgba(232, 245, 233, 0.9), rgba(232, 245, 233, 0.9)), 
        url('https://images.unsplash.com/photo-1543269664-76ad3997752e?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-attachment: fixed;
    }
    
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    
    .status-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 6px solid #2E7D32; margin-bottom: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08); position: relative;
    }

    .urgent-card {
        border: 2px solid #FFD700 !important;
        background-color: #FFFDF0 !important;
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.5) !important;
    }

    .urgent-label {
        background: #FFD700; color: #000; font-size: 10px; font-weight: bold;
        padding: 2px 10px; border-radius: 5px; position: absolute; top: 10px; right: 10px;
    }

    .verified-badge { 
        color: #1E88E5; font-weight: bold; font-size: 11px; 
        background: #E3F2FD; padding: 4px 8px; border-radius: 10px; 
    }

    .price-tag { color: #2E7D32; font-size: 26px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 50.00
if 'missoes' not in st.session_state: st.session_state.missoes = []
if 'historico' not in st.session_state: st.session_state.historico = []

# --- 3. TELA DE LOGIN ---
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("ACESSAR SISTEMA", use_container_width=True):
        if user == "1" and password == "1":
            st.session_state.logado = True
            st.rerun()
    st.stop()

# --- 4. MENU LATERAL ---
with st.sidebar:
    st.markdown(f'<div class="wallet-box"><small>SALDO GS</small><br><span style="font-size: 28px;">R$ {st.session_state.saldo:.2f}</span></div>', unsafe_allow_html=True)
    
    aba = st.radio("Menu GS:", ["🚀 Radar", "🏢 Empresa", "📊 Ganhos", "🏆 Ranking", "🔗 Indique"])
    
    with st.expander("💳 Recarregar"):
        v = st.number_input("Valor", 10.0)
        if st.button("Gerar Pix"):
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=GS_RADAR")
            if st.button("Confirmar Pagamento"):
                st.session_state.saldo += v
                st.rerun()

    if st.button("Logout"):
        st.session_state.logado = False
        st.rerun()

# --- 5. LÓGICA DAS TELAS ---

if aba == "🚀 Radar":
    st.title("📲 Radar GS - Osasco")
    cats = ["🧹 Zeladoria", "🚰 Encanador", "🛠️ Montador", "💅 Beleza", "🏠 Diarista", "🏥 Saúde"]
    tabs = st.tabs(cats)
    
    for i, tab in enumerate(tabs):
        with tab:
            nome_c = cats[i].split(" ")[1]
            lista = [m for m in st.session_state.missoes if m['cat'] == nome_c]
            
            if not lista:
                st.info(f"Nenhum pedido de {nome_c} agora.")
            else:
                for idx, m in enumerate(lista):
                    u_class = "urgent-card" if m['urgente'] else ""
                    st.markdown(f"""
                    <div class="status-card {u_class}">
                        {f'<div class="urgent-label">⚡ URGENTE</div>' if m['urgente'] else ''}
                        <div style="display: flex; justify-content: space-between;">
                            <b>{m['empresa']}</b>
                            { '<span class="verified-badge">✅ VERIFICADA</span>' if m['cpf'] else '' }
                        </div>
                        <h2 style="margin:5px 0;">{m['serv']}</h2>
                        <p>📍 {m['loc']} | 👤 {m['nome_resp']}</p>
                        <div class="price-tag">R$ {m['val']:.2f}</div>
                        <p><small>💳 {m['pag']} | 📝 {m['obs']}</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("ACEITAR MISSÃO", key=f"ac_{nome_c}_{idx}"):
                        st.session_state.historico.append(m)
                        st.success("Missão aceita!")

elif aba == "🏢 Empresa":
    st.title("🏢 Lançar Serviço")
    with st.form("f_os"):
        c1, c2 = st.columns(2)
        with c1:
            emp = st.text_input("Empresa", "GS Consultoria")
            resp = st.text_input("Seu Nome")
            cpf = st.text_input("CPF (Para Verificado)")
        with c2:
            cat = st.selectbox("Categoria", ["Zeladoria", "Encanador", "Montador", "Beleza", "Diarista", "Saúde"])
            val = st.number_input("Valor", 1.0, value=70.0)
            pag = st.selectbox("Pagamento", ["Pix", "Máquina", "Dinheiro"])
        
        serv = st.text_input("O que fazer?")
        loc = st.text_input("Local/Bairro")
        obs = st.text_area("Observações")
        urgente = st.checkbox("⚡ IMPULSIONAR (Custo R$ 5,00)")
        
        taxa = (val * 0.07) + (5.0 if urgente else 0)
        st.warning(f"Taxa total: R$ {taxa:.2f}")
        
        if st.form_submit_button("🚀 PUBLICAR"):
            if st.session_state.saldo >= taxa:
                st.session_state.saldo -= taxa
                st.session_state.missoes.append({
                    "empresa": emp, "nome_resp": resp, "cpf": cpf, "cat": cat,
                    "serv": serv, "loc": loc, "val": val, "pag": pag, 
                    "obs": obs, "urgente": urgente
                })
                st.rerun()
            else: st.error("Saldo insuficiente!")

elif aba == "📊 Ganhos":
    st.title("📊 Meus Ganhos")
    if not st.session_state.historico:
        st.info("Nenhum ganho ainda.")
    else:
        df = pd.DataFrame(st.session_state.historico)
        st.metric("Total Lucrado", f"R$ {df['val'].sum():.2f}")
        st.table(df[['serv', 'val', 'cat']])

elif aba == "🏆 Ranking":
    st.title("🏆 Melhores do Mês")
    st.table({"Posição": ["1º", "2º"], "Nome": ["Antônio", "Marcos"], "Serviços": [45, 38]})

elif aba == "🔗 Indique":
    st.title("🔗 Indique e Ganhe")
    st.write("Ganhe R$ 10,00 por indicação!")
    st.code("gsradar.com/convite/user123")
            
