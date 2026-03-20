import streamlit as st
import pandas as pd
import random
import time

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ChamaQui", page_icon="📲", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAF8; }
    
    /* Box de Perfil e Status */
    .profile-section {
        background: #FFFFFF; padding: 20px; border-radius: 15px;
        border: 1px solid #E0E0E0; text-align: center; margin-bottom: 20px;
    }
    
    .status-online { color: #2E7D32; font-weight: bold; font-size: 14px; }
    .status-offline { color: #C62828; font-weight: bold; font-size: 14px; }

    /* Wallet */
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; box-shadow: 0px 8px 16px rgba(27,94,32,0.15);
    }
    
    /* Card ChamaQui */
    .chama-card {
        background: white; padding: 20px; border-radius: 18px;
        border-left: 10px solid #2E7D32; margin-bottom: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GERENCIAMENTO DE ESTADO ---
if 'saldo' not in st.session_state: st.session_state.saldo = 370.00
if 'online' not in st.session_state: st.session_state.online = True
if 'foto' not in st.session_state: st.session_state.foto = None
if 'missao_ativa' not in st.session_state: st.session_state.missao_ativa = None

# Dados Iniciais
if 'vagas' not in st.session_state:
    st.session_state.vagas = [
        {"id": 201, "serv": "Manutenção Elétrica", "val": 220.0, "km": 1.5, "cat": "Eletricista", "loc": "Centro, Osasco"},
        {"id": 202, "serv": "Montagem de Prateleiras", "val": 150.0, "km": 3.2, "cat": "Montador", "loc": "Vila Yara, Osasco"}
    ]

# --- 3. MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("📲 ChamaQui")
    
    # Foto e Status
    with st.container():
        if st.session_state.foto:
            st.image(st.session_state.foto, width=100)
        else:
            st.info("👤 Sem Foto")
        
        st.write("**Geovani Santi**")
        
        # Botão Online/Offline
        status_check = st.toggle("Ficar Online", value=st.session_state.online)
        st.session_state.online = status_check
        
        if st.session_state.online:
            st.markdown('<p class="status-online">● DISPONÍVEL</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-offline">○ INDISPONÍVEL</p>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="wallet-box">
            <small>MEU SALDO</small><br>
            <span style="font-size: 32px; font-weight: 900;">R$ {st.session_state.saldo:.2f}</span>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Ir para:", ["🚀 Radar ChamaQui", "👤 Meu Perfil", "💳 Minha Carteira", "🏢 Área da Empresa"])

# --- 4. TELAS ---

if menu == "👤 Meu Perfil":
    st.title("⚙️ Configurações de Perfil")
    foto_upload = st.file_uploader("Carregue sua foto de perfil", type=['jpg', 'png', 'jpeg'])
    if foto_upload:
        st.session_state.foto = foto_upload
        st.success("Foto atualizada com sucesso!")
        st.rerun()

elif menu == "🚀 Radar ChamaQui":
    if not st.session_state.online:
        st.warning("⚠️ Você está offline. Ative o botão no menu para receber chamadas.")
    elif st.session_state.missao_ativa:
        m = st.session_state.missao_ativa
        st.success(f"Trabalho em andamento: {m['serv']}")
        if st.button("Finalizar Missão"):
            st.session_state.saldo += m['val']
            st.session_state.missao_ativa = None
            st.balloons()
            st.rerun()
    else:
        st.title("📲 Radar ChamaQui")
        distancia = st.slider("Ver missões até (km):", 1, 50, 6)
        
        for v in st.session_state.vagas:
            if v['km'] <= distancia:
                st.markdown(f"""
                <div class="chama-card">
                    <p style="color: #2E7D32; font-weight: bold; margin:0;">{v['cat']} <span style="float:right; color:#666;">📍 {v['km']} km</span></p>
                    <h2 style="margin: 10px 0;">{v['serv']}</h2>
                    <p style="color: #555;">{v['loc']}</p>
                    <h3 style="color: #1B5E20;">R$ {v['val']:.2f}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"ACEITAR MISSÃO #{v['id']}", key=f"v_{v['id']}", use_container_width=True):
                    st.session_state.missao_ativa = v
                    st.session_state.vagas = [x for x in st.session_state.vagas if x['id'] != v['id']]
                    st.rerun()

elif menu == "💳 Minha Carteira":
    st.title("💳 Gestão Financeira")
    st.metric("Saldo Disponível", f"R$ {st.session_state.saldo:.2f}")
    
    with st.expander("Realizar Saque (Pix)"):
        valor_saque = st.number_input("Valor do saque", min_value=10.0, max_value=st.session_state.saldo)
        if st.button("Confirmar Saque"):
            st.session_state.saldo -= valor_saque
            st.success(f"Saque de R$ {valor_saque:.2f} processado!")
            st.rerun()

elif menu == "🏢 Área da Empresa":
    st.title("🏢 Publicar no Radar")
    with st.form("pub"):
        serv = st.text_input("Serviço")
        loc = st.text_input("Endereço")
        val = st.number_input("Valor", value=100.0)
        if st.form_submit_button("Lançar Agora"):
            nova = {"id": random.randint(300, 900), "serv": serv, "val": val, "km": 2.5, "cat": "Geral", "loc": loc}
            st.session_state.vagas.append(nova)
            st.success("Serviço lançado no ChamaQui!")
            
