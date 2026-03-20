import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

# --- 1. CONFIGURAÇÃO E IDENTIDADE ---
st.set_page_config(page_title="ChamaQui - Serviços", page_icon="📲", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAF8; }
    
    /* Perfil no Menu */
    .profile-sidebar {
        text-align: center;
        padding: 10px;
        border-bottom: 1px solid #ddd;
        margin-bottom: 20px;
    }
    .profile-img {
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #2E7D32;
    }
    
    /* Wallet e Status */
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 10px; box-shadow: 0px 8px 16px rgba(27,94,32,0.2);
    }
    
    .status-badge {
        font-size: 12px; font-weight: bold; padding: 5px 12px; border-radius: 20px;
        display: inline-block; margin-top: 5px;
    }
    .online { background-color: #C8E6C9; color: #2E7D32; }
    .offline { background-color: #FFCDD2; color: #C62828; }

    /* Cards ChamaQui */
    .mission-card {
        background: white; padding: 20px; border-radius: 18px;
        border-left: 10px solid #2E7D32; margin-bottom: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS ---
if 'saldo' not in st.session_state: st.session_state.saldo = 150.00
if 'online' not in st.session_state: st.session_state.online = True
if 'foto_perfil' not in st.session_state: st.session_state.foto_perfil = None
if 'xp' not in st.session_state: st.session_state.xp = 85
if 'missao_ativa' not in st.session_state: st.session_state.missao_ativa = None
if 'missoes' not in st.session_state:
    st.session_state.missoes = [
        {"id": 201, "emp": "ChamaQui Prime", "serv": "Manutenção Elétrica", "val": 220.0, "km": 1.5, "cat": "Eletricista", "tel": "5511999999999", "loc": "Centro, Osasco"},
        {"id": 202, "emp": "Loja Mix", "serv": "Montagem de Prateleiras", "val": 150.0, "km": 3.2, "cat": "Montador", "tel": "5511888888888", "loc": "Vila Yara, Osasco"}
    ]

# --- 3. MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("📲 ChamaQui")
    
    # Área do Perfil
    with st.container():
        if st.session_state.foto_perfil:
            st.image(st.session_state.foto_perfil, width=120)
        else:
            st.warning("👤 Sem Foto")
        
        st.write("**Geovani Santi**")
        status_label = "DISPONÍVEL" if st.session_state.online else "INDISPONÍVEL"
        status_class = "online" if st.session_state.online else "offline"
        st.markdown(f'<div class="status-badge {status_class}">{status_label}</div>', unsafe_allow_html=True)
        
        # Botão On/Off
        if st.toggle("Ficar Online", value=st.session_state.online):
            st.session_state.online = True
        else:
            st.session_state.online = False

    st.markdown("---")
    
    # Wallet
    st.markdown(f"""
        <div class="wallet-box">
            <small>MEU SALDO</small><br>
            <span style="font-size: 28px; font-weight: 900;">R$ {st.session_state.saldo:.2f}</span>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Ir para:", ["🚀 Radar ChamaQui", "👤 Meu Perfil", "🏢 Área da Empresa", "🏆 Ranking"])

# --- 4. TELAS ---

# --- TELA: MEU PERFIL (NOVO) ---
if menu == "👤 Meu Perfil":
    st.title("⚙️ Configurações de Perfil")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sua Foto")
        nova_foto = st.file_uploader("Trocar foto de perfil", type=['jpg', 'png', 'jpeg'])
        if nova_foto:
            st.session_state.foto_perfil = nova_foto
            st.success("Foto atualizada!")
            st.rerun()
            
    with col2:
        st.subheader("Dados do Prestador")
        st.text_input("Nome Completo", "Geovani Santi")
        st.text_input("Especialidade Principal", "Vendas e Gestão")
        st.write(f"**Nível:** Prata ({st.session_state.xp}% para Ouro)")
        st.progress(st.session_state.xp / 100)

# --- TELA: RADAR ---
elif menu == "🚀 Radar ChamaQui":
    if not st.session_state.online:
        st.error("⚠️ Você está OFFLINE. Fique online no menu lateral para ver novas missões.")
        st.info("Dica: Prestadores online recebem chamadas 3x mais rápido.")
    
    elif st.session_state.missao_ativa:
        m = st.session_state.missao_ativa
        st.title("🛠️ Missão em Curso")
        st.info(f"📍 {m['serv']} em {m['loc']}")
        
        c1, c2 = st.columns(2)
        c1.link_button("🗺️ VER ROTA (GPS)", f"https://www.google.com/maps/search/?api=1&query={m['loc'].replace(' ', '+')}", use_container_width=True)
        c2.link_button("💬 FALAR COM CLIENTE", f"https://wa.me/{m['tel']}", use_container_width=True)
        
        st.divider()
        cam = st.camera_input("Foto da Entrega")
        if st.button("FINALIZAR E RECEBER", type="primary"):
            if cam:
                st.session_state.saldo += m['val']
                st.session_state.missao_ativa = None
                st.success("Trabalho concluído! Saldo atualizado.")
                st.balloons()
                st.rerun()
            else:
                st.error("Tire uma foto para comprovar a conclusão.")

    else:
        st.title("📲 Radar ChamaQui - Osasco")
        st.write("Buscando as melhores oportunidades perto de você...")
        
        dist = st.slider("Ver missões até (km):", 1, 50, 15)
        
        vagas = [v for v in st.session_state.missoes if v['km'] <= dist]
        
        if not vagas:
            st.warning("Nada no radar por enquanto. Tente aumentar a distância.")
        else:
            for v in vagas:
                st.markdown(f"""
                <div class="mission-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #2E7D32; font-weight: bold;">{v['cat']}</span>
                        <span style="color: #666;">📍 {v['km']} km</span>
                    </div>
                    <h3 style="margin: 10px 0;">{v['serv']}</h3>
                    <p style="color: #555; font-size: 14px;">{v['loc']} | {v['emp']}</p>
                    <div style="font-size: 24px; font-weight: bold; color: #1B5E20; margin-top: 10px;">
                        R$ {v['val']:.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"CHAMAR ESTA MISSÃO #{v['id']}", key=f"btn_{v['id']}", use_container_width=True):
                    st.session_state.missao_ativa = v
                    st.session_state.missoes = [x for x in st.session_state.missoes if x['id'] != v['id']]
                    st.rerun()

# --- TELA: EMPRESA ---
elif menu == "🏢 Área da Empresa":
    st.title("🏢 Publicar no ChamaQui")
    with st.form("pub_chamaqui"):
        serv = st.text_input("O que você precisa?")
        end = st.text_input("Endereço de atendimento")
        val = st.number_input("Quanto vai pagar?", min_value=20.0)
        cat = st.selectbox("Categoria", ["Montador", "Eletricista", "Zeladoria", "Beleza", "Outros"])
        
        if st.form_submit_button("LANÇAR NO RADAR"):
            nova = {"id": random.randint(1000, 9999), "emp": "ChamaQui User", "serv": serv, "val": val, "km": 2.0, "cat": cat, "tel": "5511999999999", "loc": end}
            st.session_state.missoes.append(nova)
            st.success("Sua chamada foi enviada para os prestadores!")

# --- TELA: RANKING ---
elif menu == "🏆 Ranking":
    st.title("🏆 Melhores ChamaQui - Osasco")
    st.table(pd.DataFrame({
        "Prestador": ["Geovani Santi", "Marcos V.", "Ana Julia"],
        "Missões": [142, 120, 98],
        "Avaliação": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐"]
    }))
    
