import streamlit as st
import pandas as pd
import random
import time

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="ChamaQui", page_icon="📲", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAF8; }
    
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
    
    .status-badge {
        font-size: 12px; font-weight: bold; padding: 5px 12px; border-radius: 20px;
        display: inline-block; margin-top: 5px;
    }
    .online { background-color: #C8E6C9; color: #2E7D32; }
    .offline { background-color: #FFCDD2; color: #C62828; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ESTADO DO SISTEMA ---
if 'saldo' not in st.session_state: st.session_state.saldo = 370.00
if 'online' not in st.session_state: st.session_state.online = True
if 'foto' not in st.session_state: st.session_state.foto = None
if 'missao_ativa' not in st.session_state: st.session_state.missao_ativa = None
if 'vagas' not in st.session_state:
    st.session_state.vagas = [
        {"id": 201, "serv": "Manutenção Elétrica", "val": 220.0, "km": 1.5, "cat": "Eletricista", "loc": "Centro, Osasco", "tel": "5511999999999"},
        {"id": 202, "serv": "Montagem de Prateleiras", "val": 150.0, "km": 3.2, "cat": "Montador", "loc": "Vila Yara, Osasco", "tel": "5511888888888"}
    ]

# --- 3. MENU LATERAL ---
with st.sidebar:
    st.title("📲 ChamaQui")
    
    if st.session_state.foto:
        st.image(st.session_state.foto, width=100)
    else:
        st.info("👤 Geovani Santi")
    
    st.session_state.online = st.toggle("Ficar Online", value=st.session_state.online)
    status_label = "DISPONÍVEL" if st.session_state.online else "INDISPONÍVEL"
    status_class = "online" if st.session_state.online else "offline"
    st.markdown(f'<div class="status-badge {status_class}">{status_label}</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="wallet-box">
            <small>MEU SALDO</small><br>
            <span style="font-size: 32px; font-weight: 900;">R$ {st.session_state.saldo:.2f}</span>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Ir para:", ["🚀 Radar ChamaQui", "👤 Meu Perfil", "💳 Minha Carteira"])

# --- 4. TELAS ---

if menu == "🚀 Radar ChamaQui":
    if not st.session_state.online:
        st.warning("⚠️ Você está offline. Fique online para ver o radar.")
    
    # --- TELA DE MISSÃO EM ANDAMENTO (CORRIGIDA) ---
    elif st.session_state.missao_ativa:
        m = st.session_state.missao_ativa
        st.title("⚡ Missão em Andamento")
        st.info(f"**Serviço:** {m['serv']} | **Valor:** R$ {m['val']:.2f}")
        
        # Botões de Ação Imediata
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.link_button("🗺️ ABRIR GPS (INICIAR ROTA)", f"https://www.google.com/maps/search/?api=1&query={m['loc'].replace(' ', '+')}", use_container_width=True, type="primary")
        with col_btn2:
            st.link_button("💬 CHAMAR NO WHATSAPP", f"https://wa.me/{m['tel']}?text=Olá, sou o prestador do ChamaQui!", use_container_width=True)
        
        st.divider()
        
        # Área de Finalização
        st.subheader("Finalizar e Receber")
        st.write("Tire uma foto do trabalho concluído para liberar o pagamento:")
        foto_servico = st.camera_input("Foto da conclusão")
        
        estrelas = st.select_slider("Avalie o cliente/local", options=[1, 2, 3, 4, 5], value=5)
        st.write(f"Sua nota: {'⭐' * estrelas}")
        
        c_fin1, c_fin2 = st.columns(2)
        if c_fin1.button("CONCLUIR MISSÃO E RECEBER", type="primary", use_container_width=True):
            if foto_servico:
                with st.spinner("Processando pagamento..."):
                    time.sleep(1.5)
                    st.session_state.saldo += m['val']
                    st.session_state.missao_ativa = None
                    st.success("Pagamento creditado com sucesso!")
                    st.balloons()
                    st.rerun()
            else:
                st.error("Por favor, tire a foto do serviço antes de concluir.")
        
        if c_fin2.button("Cancelar e Voltar ao Radar", use_container_width=True):
            st.session_state.missao_ativa = None
            st.rerun()

    # --- TELA DO RADAR ---
    else:
        st.title("📲 Radar ChamaQui")
        dist = st.slider("Raio de busca (km):", 1, 50, 6)
        
        for v in st.session_state.vagas:
            if v['km'] <= dist:
                st.markdown(f"""
                <div class="chama-card">
                    <p style="color: #2E7D32; font-weight: bold;">{v['cat']} <span style="float:right; color:#666;">📍 {v['km']} km</span></p>
                    <h2 style="margin: 5px 0;">{v['serv']}</h2>
                    <p style="color: #555; margin-bottom: 5px;">{v['loc']}</p>
                    <h3 style="color: #1B5E20; margin: 0;">R$ {v['val']:.2f}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"ACEITAR MISSÃO #{v['id']}", key=f"v_{v['id']}", use_container_width=True):
                    st.session_state.missao_ativa = v
                    st.session_state.vagas = [x for x in st.session_state.vagas if x['id'] != v['id']]
                    st.rerun()

elif menu == "👤 Meu Perfil":
    st.title("👤 Meu Perfil")
    f = st.file_uploader("Trocar foto de perfil", type=['jpg', 'png'])
    if f: 
        st.session_state.foto = f
        st.rerun()

elif menu == "💳 Minha Carteira":
    st.title("💳 Minha Carteira")
    st.metric("Saldo Total", f"R$ {st.session_state.saldo:.2f}")
    if st.button("Solicitar Saque via Pix"):
        st.info("Saque solicitado! Prazo de até 2 horas.")
                             
