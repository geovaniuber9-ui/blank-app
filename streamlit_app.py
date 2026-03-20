import streamlit as st
import pandas as pd
import random
import time

# --- 1. CONFIGURAÇÃO GERAL ---
st.set_page_config(page_title="ChamaQui - Osasco", page_icon="📲", layout="wide")

# Estilos CSS para manter o visual dos seus prints
st.markdown("""
    <style>
    .stApp { background-color: #F8FAF8; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #EEE; }
    
    /* Card de Saldo Verde */
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Card de Missão Estilizado */
    .chama-card {
        background: white; padding: 20px; border-radius: 18px;
        border-left: 10px solid #2E7D32; margin-bottom: 15px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }
    
    .status-badge {
        font-size: 11px; font-weight: bold; padding: 4px 12px; border-radius: 20px;
        display: inline-block; margin-bottom: 10px;
    }
    .online { background-color: #C8E6C9; color: #1B5E20; }
    .offline { background-color: #FFCDD2; color: #B71C1C; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE DADOS EM MEMÓRIA (SESSION STATE) ---
if 'saldo' not in st.session_state: st.session_state.saldo = 370.00
if 'online' not in st.session_state: st.session_state.online = True
if 'foto' not in st.session_state: st.session_state.foto = None
if 'missao_ativa' not in st.session_state: st.session_state.missao_ativa = None
if 'vagas' not in st.session_state:
    st.session_state.vagas = [
        {"id": 201, "serv": "Manutenção Elétrica", "val": 220.0, "km": 1.5, "cat": "Eletricista", "loc": "Centro, Osasco", "tel": "5511999999999", "emp": "ChamaQui Prime"},
        {"id": 202, "serv": "Montagem de Móveis", "val": 150.0, "km": 3.2, "cat": "Montador", "loc": "Vila Yara, Osasco", "tel": "5511888888888", "emp": "GS Consultoria"}
    ]

# --- 3. MENU LATERAL DE NAVEGAÇÃO ---
with st.sidebar:
    st.title("📲 ChamaQui")
    
    # Foto e Identificação
    if st.session_state.foto:
        st.image(st.session_state.foto, width=100)
    else:
        st.info("👤 Geovani Santi")
    
    # Controle de Status
    st.session_state.online = st.toggle("Ficar Online", value=st.session_state.online)
    status_text = "DISPONÍVEL" if st.session_state.online else "INDISPONÍVEL"
    status_class = "online" if st.session_state.online else "offline"
    st.markdown(f'<div class="status-badge {status_class}">{status_text}</div>', unsafe_allow_html=True)

    # Carteira (Visual Print 1000024141)
    st.markdown(f"""
        <div class="wallet-box">
            <small>MEU SALDO GS</small><br>
            <span style="font-size: 28px; font-weight: 900;">R$ {st.session_state.saldo:.2f}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Navegação entre as telas
    menu = st.radio("Navegação:", ["🚀 Radar de Missões", "👤 Meu Perfil", "💳 Minha Carteira", "🏢 Central da Empresa", "🏆 Ranking Global"])

# --- 4. LÓGICA DAS TELAS ---

# --- TELA 1: RADAR E EXECUÇÃO ---
if menu == "🚀 Radar de Missões":
    if not st.session_state.online:
        st.warning("⚠️ Você está offline. Mude para 'Online' no menu para ver o radar.")
    
    # Se houver uma missão aceita, mostra a tela de execução (Print 1000024142)
    elif st.session_state.missao_ativa:
        m = st.session_state.missao_ativa
        st.title("⚡ Missão em Andamento")
        with st.container(border=True):
            st.info(f"**Serviço:** {m['serv']} | **Valor:** R$ {m['val']:.2f}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("🗺️ ABRIR GPS (ROTA)", f"https://www.google.com/maps/search/?api=1&query={m['loc'].replace(' ', '+')}", use_container_width=True, type="primary")
            with c2:
                st.link_button("💬 WHATSAPP CLIENTE", f"https://wa.me/{m['tel']}?text=Olá, sou o prestador do ChamaQui!", use_container_width=True)
        
        st.divider()
        st.subheader("Finalizar Trabalho")
        foto = st.camera_input("Tire uma foto do serviço pronto")
        nota = st.select_slider("Avalie o cliente", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], value="⭐⭐⭐⭐⭐")
        
        if st.button("CONCLUIR E RECEBER PAGAMENTO", type="primary", use_container_width=True):
            if foto:
                st.session_state.saldo += m['val']
                st.session_state.missao_ativa = None
                st.success("Pagamento Creditado!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("⚠️ Foto obrigatória para comprovar a conclusão.")
        
        if st.button("Cancelar e voltar ao Radar"):
            st.session_state.missao_ativa = None
            st.rerun()

    # Se não houver missão, mostra a listagem (Print 1000024130)
    else:
        st.title("🚀 Radar ChamaQui")
        raio = st.slider("Distância máxima (km):", 1, 50, 10)
        
        vagas_visiveis = [v for v in st.session_state.vagas if v['km'] <= raio]
        
        if not vagas_visiveis:
            st.info("Nenhuma missão encontrada neste raio. Tente aumentar a distância.")
        else:
            for v in vagas_visiveis:
                st.markdown(f"""
                <div class="chama-card">
                    <p style="color: #2E7D32; font-weight: bold;">{v['cat']} <span style="float:right;">📍 {v['km']} km</span></p>
                    <h2 style="margin: 5px 0;">{v['serv']}</h2>
                    <p style="color: #666;">{v['loc']} | {v['emp']}</p>
                    <h3 style="color: #1B5E20; margin-top: 10px;">R$ {v['val']:.2f}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"ACEITAR MISSÃO #{v['id']}", key=f"btn_{v['id']}", use_container_width=True):
                    st.session_state.missao_ativa = v
                    st.session_state.vagas = [x for x in st.session_state.vagas if x['id'] != v['id']]
                    st.rerun()

# --- TELA 2: CENTRAL DA EMPRESA (Print 1000024094) ---
elif menu == "🏢 Central da Empresa":
    st.title("🏢 Lançar Nova Solicitação")
    with st.form("form_vaga"):
        emp = st.text_input("Sua Empresa/Nome", value="GS Consultoria")
        serv = st.text_input("O que você precisa?")
        cat = st.selectbox("Categoria", ["Zeladoria", "Eletricista", "Montador", "Beleza", "Outros"])
        loc = st.text_input("Endereço do atendimento")
        val = st.number_input("Valor a oferecer (R$)", min_value=10.0, value=100.0)
        zap = st.text_input("Seu WhatsApp (Ex: 5511999999999)")
        
        if st.form_submit_button("LANÇAR NO RADAR"):
            nova = {
                "id": random.randint(1000, 9999), "emp": emp, "serv": serv,
                "val": val, "km": random.uniform(0.5, 6.0), "cat": cat, "loc": loc, "tel": zap
            }
            st.session_state.vagas.append(nova)
            st.success("✅ Missão lançada com sucesso!")

# --- TELA 3: CARTEIRA ---
elif menu == "💳 Minha Carteira":
    st.title("💳 Gestão Financeira")
    st.metric("Saldo Disponível", f"R$ {st.session_state.saldo:.2f}")
    if st.button("Solicitar Saque via PIX"):
        st.success("Pedido de saque enviado! O dinheiro cairá em breve.")

# --- TELA 4: RANKING (Print 1000024134) ---
elif menu == "🏆 Ranking Global":
    st.title("🏆 Elite do ChamaQui")
    df_rank = pd.DataFrame({
        "Profissional": ["Geovani Santi", "Beatriz S.", "Dayana O.", "Marcos L."],
        "Missões": [152, 140, 98, 85],
        "Avaliação": ["⭐ 5.0", "⭐ 4.9", "⭐ 4.8", "⭐ 4.7"]
    })
    st.table(df_rank)

# --- TELA 5: MEU PERFIL ---
elif menu == "👤 Meu Perfil":
    st.title("👤 Configurações")
    f = st.file_uploader("Trocar foto de perfil", type=['png', 'jpg'])
    if f:
        st.session_state.foto = f
        st.rerun()
        
