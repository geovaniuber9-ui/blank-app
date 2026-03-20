import streamlit as st
import pandas as pd
import random
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA E ESTILO ---
st.set_page_config(page_title="ChamaQui - Osasco", page_icon="📲", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAF8; }
    
    /* Cartão de Saldo Estilizado */
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 25px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; box-shadow: 0px 8px 16px rgba(27,94,32,0.2);
    }
    
    /* Card das Missões no Radar */
    .chama-card {
        background: white; padding: 20px; border-radius: 18px;
        border-left: 10px solid #2E7D32; margin-bottom: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Badges de Status */
    .status-badge {
        font-size: 12px; font-weight: bold; padding: 5px 12px; border-radius: 20px;
        display: inline-block; margin-bottom: 10px;
    }
    .online { background-color: #C8E6C9; color: #2E7D32; }
    .offline { background-color: #FFCDD2; color: #C62828; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DO ESTADO (BANCO DE DADOS TEMPORÁRIO) ---
if 'saldo' not in st.session_state: st.session_state.saldo = 370.00
if 'online' not in st.session_state: st.session_state.online = True
if 'foto' not in st.session_state: st.session_state.foto = None
if 'missao_ativa' not in st.session_state: st.session_state.missao_ativa = None

# Lista inicial de missões no radar
if 'vagas' not in st.session_state:
    st.session_state.vagas = [
        {"id": 201, "empresa": "ChamaQui Prime", "serv": "Manutenção Elétrica", "val": 220.0, "km": 1.5, "cat": "Eletricista", "loc": "Centro, Osasco", "tel": "5511999999999"},
        {"id": 202, "empresa": "GS Consultoria", "serv": "Montagem de Prateleiras", "val": 150.0, "km": 3.2, "cat": "Montador", "loc": "Vila Yara, Osasco", "tel": "5511888888888"}
    ]

# --- 3. MENU LATERAL (NAVEGAÇÃO) ---
with st.sidebar:
    st.title("📲 ChamaQui")
    
    # Perfil e Status
    if st.session_state.foto:
        st.image(st.session_state.foto, width=100)
    else:
        st.info("👤 Geovani Santi")
    
    st.session_state.online = st.toggle("Ficar Online", value=st.session_state.online)
    status_text = "DISPONÍVEL" if st.session_state.online else "INDISPONÍVEL"
    status_style = "online" if st.session_state.online else "offline"
    st.markdown(f'<div class="status-badge {status_style}">{status_text}</div>', unsafe_allow_html=True)

    # Carteira Rápida
    st.markdown(f"""
        <div class="wallet-box">
            <small>MEU SALDO GS</small><br>
            <span style="font-size: 30px; font-weight: 900;">R$ {st.session_state.saldo:.2f}</span>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Ir para:", ["🚀 Radar de Missões", "👤 Meu Perfil", "💳 Minha Carteira", "🏢 Central da Empresa", "🏆 Ranking Global"])
    
    if st.button("Sair do Sistema", use_container_width=True):
        st.stop()

# --- 4. LÓGICA DAS TELAS ---

# --- TELA: RADAR DE MISSÕES ---
if menu == "🚀 Radar de Missões":
    if not st.session_state.online:
        st.warning("⚠️ Você está offline. Ative o modo 'Online' para receber chamadas.")
    
    # SUBTELA: MISSÃO EM EXECUÇÃO
    elif st.session_state.missao_ativa:
        m = st.session_state.missao_ativa
        st.title("⚡ Missão em Andamento")
        st.success(f"**Serviço:** {m['serv']} | **Valor:** R$ {m['val']:.2f}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("🗺️ ABRIR GPS (ROTA)", f"https://www.google.com/maps/search/?api=1&query={m['loc'].replace(' ', '+')}", use_container_width=True, type="primary")
        with col2:
            st.link_button("💬 CHAMAR NO WHATSAPP", f"https://wa.me/{m['tel']}?text=Olá, sou o prestador do ChamaQui!", use_container_width=True)
        
        st.divider()
        st.subheader("Finalizar e Receber")
        foto_servico = st.camera_input("Tire uma foto do trabalho concluído")
        nota = st.select_slider("Avalie o atendimento/local", options=[1, 2, 3, 4, 5], value=5)
        
        if st.button("CONCLUIR MISSÃO E RECEBER", type="primary", use_container_width=True):
            if foto_servico:
                st.session_state.saldo += m['val']
                st.session_state.missao_ativa = None
                st.balloons()
                st.success("Pagamento creditado com sucesso!")
                time.sleep(2)
                st.rerun()
            else:
                st.error("⚠️ É necessário enviar a foto para comprovação do serviço.")

        if st.button("Cancelar Missão (Voltar ao Radar)", use_container_width=True):
            st.session_state.missao_ativa = None
            st.rerun()

    # SUBTELA: LISTAGEM DO RADAR
    else:
        st.title("ChamaQui - Osasco")
        st.write("Buscando as melhores oportunidades perto de você...")
        raio = st.slider("Ver missões até (km):", 1, 50, 10)
        
        for v in st.session_state.vagas:
            if v['km'] <= raio:
                st.markdown(f"""
                <div class="chama-card">
                    <p style="color: #2E7D32; font-weight: bold;">{v['cat']} <span style="float:right;">📍 {v['km']} km</span></p>
                    <h2 style="margin: 5px 0;">{v['serv']}</h2>
                    <p style="color: #666;">{v['loc']} | {v['empresa']}</p>
                    <h3 style="color: #1B5E20; margin-top: 10px;">R$ {v['val']:.2f}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"ACEITAR TRABALHO #{v['id']}", key=f"btn_{v['id']}", use_container_width=True):
                    st.session_state.missao_ativa = v
                    st.session_state.vagas = [x for x in st.session_state.vagas if x['id'] != v['id']]
                    st.rerun()

# --- TELA: ÁREA DA EMPRESA (PARA LANÇAR CHAMADOS) ---
elif menu == "🏢 Central da Empresa":
    st.title("🏢 Lançar Novo Serviço")
    with st.form("form_vaga"):
        emp = st.text_input("Empresa", value="GS Consultoria")
        serv = st.text_input("Título do Serviço (ex: Reparo de Gôndolas)")
        cat = st.selectbox("Categoria", ["Zeladoria", "Encanador", "Montador", "Beleza", "Eletricista"])
        loc = st.text_input("Endereço Completo")
        val = st.number_input("Valor a Pagar (R$)", min_value=10.0, value=100.0)
        zap = st.text_input("WhatsApp para Contato")
        
        if st.form_submit_button("PUBLICAR NO RADAR"):
            nova_vaga = {
                "id": random.randint(100, 999), "empresa": emp, "serv": serv,
                "val": val, "km": random.uniform(0.5, 9.0), "cat": cat, "loc": loc, "tel": zap
            }
            st.session_state.vagas.append(nova_vaga)
            st.success("✅ Serviço publicado com sucesso!")

# --- TELA: MINHA CARTEIRA ---
elif menu == "💳 Minha Carteira":
    st.title("💳 Gestão Financeira")
    st.metric("Saldo Disponível", f"R$ {st.session_state.saldo:.2f}")
    
    col_pix, col_hist = st.columns(2)
    with col_pix:
        st.subheader("Sacar via Pix")
        valor_saque = st.number_input("Valor", min_value=10.0, max_value=st.session_state.saldo)
        if st.button("Confirmar Saque"):
            st.session_state.saldo -= valor_saque
            st.success(f"Saque de R$ {valor_saque:.2f} enviado!")
            st.rerun()
    with col_hist:
        st.subheader("Histórico")
        st.write("Recentes:")
        st.caption("✅ Missão #201: + R$ 220,00")

# --- TELA: RANKING ---
elif menu == "🏆 Ranking Global":
    st.title("🏆 Ranking de Elite - Osasco")
    rank_data = {
        "Posição": ["1º", "2º", "3º", "4º"],
        "Nome": ["Geovani Santi", "Beatriz S.", "Dayana O.", "Marcos L."],
        "Missões": [152, 140, 98, 85],
        "Avaliação": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐"]
    }
    st.table(pd.DataFrame(rank_data))

# --- TELA: MEU PERFIL ---
elif menu == "👤 Meu Perfil":
    st.title("👤 Configurações de Perfil")
    st.write(f"**Nome:** Geovani Santi")
    st.write("**Nível:** Prata (85% para Ouro)")
    st.progress(0.85)
    
    nova_foto = st.file_uploader("Trocar foto de perfil", type=['png', 'jpg', 'jpeg'])
    if nova_foto:
        st.session_state.foto = nova_foto
        st.rerun()
                    
