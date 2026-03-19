import streamlit as st
import time

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="GS Radar Pro", page_icon="📈", layout="wide")

# ESTILO VISUAL "APP DE VIAGEM"
st.markdown("""
    <style>
    .stApp { background-color: #F7F9FB !important; }
    .job-card { 
        background: white; padding: 18px; border-radius: 12px; 
        border: 1px solid #E0E4E8; margin-bottom: 12px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.02);
    }
    .price-tag { color: #111; font-size: 24px; font-weight: 900; }
    .pix-badge { background-color: #00BFA5; color: white; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; }
    .card-badge { background-color: #4285F4; color: white; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; }
    .km-info { color: #70757A; font-size: 14px; font-weight: 500; }
    .sidebar-info { 
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); 
        color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS (SESSÃO)
if 'saldo' not in st.session_state: st.session_state.saldo = 10.00  # Saldo inicial teste
if 'missoes' not in st.session_state:
    st.session_state.missoes = [
        {"id": 1, "cat": "🚰 Encanador", "job": "Vazamento em Banheiro", "loc": "Jd. Elvira, Osasco", "val": 150.0, "pay": "PIX", "dist": "2.1 km"},
        {"id": 2, "cat": "🛋️ Montador", "job": "Painel de TV 75'", "loc": "Vila Yara", "val": 180.0, "pay": "Cartão (Máquina)", "dist": "4.5 km"}
    ]

# --- SIDEBAR: GESTÃO FINANCEIRA E RECARGA ---
with st.sidebar:
    st.markdown(f"""<div class="sidebar-info">
        <small>SALDO PARA TRABALHAR</small><br>
        <span style="font-size: 28px; font-weight: bold;">R$ {st.session_state.saldo:.2f}</span>
    </div>""", unsafe_allow_html=True)
    
    with st.expander("💳 RECARREGAR AGORA"):
        valor_recarga = st.selectbox("Escolha o valor:", [20, 50, 100])
        if st.button(f"Gerar PIX de R$ {valor_recarga}"):
            st.warning("Copia a chave PIX: `geovanisanti@exemplo.com`")
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=PIX_GEVANI_EXEMPLO")
            if st.button("Confirmar Pagamento"):
                st.session_state.saldo += valor_recarga
                st.success("Crédito adicionado!")
                st.rerun()
    
    st.divider()
    modo = st.radio("Módulo:", ["🚀 Radar (Prestador)", "🏢 Empresa (Lançar)"])
    st.divider()
    st.link_button("🆘 Suporte WhatsApp", "https://wa.me/5511999999999?text=Quero%20recarga%20de%20crédito")

# --- MODO PRESTADOR (ESTILO INDRIVE/UBER) ---
if modo == "🚀 Radar (Prestador)":
    st.title("📲 Pedidos Disponíveis")
    
    categorias = ["Todos", "🛠️ Reparos", "🚰 Encanador", "⚡ Eletricista", "🛋️ Montador", "🪚 Marceneiro", "💅 Beleza"]
    escolha_cat = st.selectbox("Filtrar por tipo:", categorias)

    # Filtragem
    lista_exibir = st.session_state.missoes if escolha_cat == "Todos" else [m for m in st.session_state.missoes if m['cat'].strip() == escolha_cat.strip()]

    if not lista_exibir:
        st.info("Nenhuma missão nesta categoria no momento.")
    
    for m in lista_exibir:
        taxa = 2.50 # VALOR FIXO QUE VOCÊ GANHA POR SERVIÇO
        
        st.markdown(f"""
            <div class="job-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <span class="km-info">📍 {m['dist']} • {m['loc']}</span><br>
                        <b style="font-size: 20px;">{m['job']}</b><br>
                        <span style="color: #666;">{m['cat']}</span><br><br>
                        <span class="{'pix-badge' if m['pay'] == 'PIX' else 'card-badge'}">{m['pay']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span class="price-tag">R$ {m['val']:.0f}</span><br>
                        <small style="color: #666;">Taxa GS: R$ {taxa:.2f}</small>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns([3, 1])
        with c1:
            if st.button(f"ACEITAR PEDIDO #{m['id']}", key=f"aceita_{m['id']}", use_container_width=True):
                if st.session_state.saldo >= taxa:
                    st.session_state.saldo -= taxa
                    st.success("Você aceitou! O cliente foi avisado.")
                    st.balloons()
                else:
                    st.error("Sem saldo! Faça uma recarga para aceitar.")
        with c2:
            st.link_button("🗺️ Rota", f"https://www.google.com/maps/search/{m['loc']}+Osasco", use_container_width=True)

# --- MODO EMPRESA ---
else:
    st.title("🏢 Lançar Nova Solicitação")
    with st.form("post_job"):
        col1, col2 = st.columns(2)
        with col1:
            cat = st.selectbox("Categoria", categorias[1:])
            job = st.text_input("O que precisa ser feito?")
            val = st.number_input("Valor oferecido (R$)", min_value=1.0)
        with col2:
            loc = st.text_input("Endereço/Bairro (Osasco)")
            pay = st.radio("Pagamento para o Prestador:", ["PIX", "Cartão (Máquina)", "Dinheiro"])
        
        if st.form_submit_button("LANÇAR NO RADAR 🚀"):
            st.session_state.missoes.append({
                "id": int(time.time()), "cat": cat, "job": job, 
                "loc": loc, "val": val, "pay": pay, "dist": "~1.5 km"
            })
            st.success("Missão publicada!")
            st.rerun()
         
