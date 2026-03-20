import streamlit as st
import pandas as pd
import random
import time

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="GS Radar Pro", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAF8; }
    
    /* Header de Perfil */
    .user-profile {
        background: white; padding: 15px; border-radius: 15px;
        border: 1px solid #E0E0E0; margin-bottom: 20px; display: flex; align-items: center;
    }
    
    /* Wallet */
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; box-shadow: 0px 8px 16px rgba(27, 94, 32, 0.2);
    }
    
    /* Card de Missão */
    .mission-card {
        background: white; padding: 20px; border-radius: 18px;
        border-left: 10px solid #2E7D32; margin-bottom: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }
    .urgent-card { border-left-color: #FFD700; background-color: #FFFDF0; }
    
    .badge-verified { background: #E3F2FD; color: #1E88E5; font-size: 11px; padding: 3px 8px; border-radius: 20px; font-weight: bold; }
    .price-tag { color: #2E7D32; font-size: 26px; font-weight: 800; }
    
    /* Botões Custom */
    .stButton button { width: 100%; border-radius: 12px; height: 3.2em; font-weight: 700; transition: 0.3s; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ESTADOS E DADOS ---
if 'saldo' not in st.session_state: st.session_state.saldo = 150.00
if 'xp' not in st.session_state: st.session_state.xp = 85  # Experiência do prestador
if 'missao_ativa' not in st.session_state: st.session_state.missao_ativa = None
if 'historico' not in st.session_state: st.session_state.historico = []

# Dados de exemplo (Missões no Radar)
if 'missoes' not in st.session_state:
    st.session_state.missoes = [
        {"id": 101, "emp": "Mercado Central", "serv": "Reparo de Gôndolas", "val": 180.0, "km": 2.4, "cat": "Montador", "urg": True, "tel": "5511999999999", "loc": "Av. dos Autonomistas, 2000"},
        {"id": 102, "emp": "Condomínio Life", "serv": "Limpeza Pós Obra", "val": 350.0, "km": 5.8, "cat": "Zeladoria", "urg": False, "tel": "5511888888888", "loc": "Rua Bela Vedere, 120"},
        {"id": 103, "emp": "Clínica Saúde", "serv": "Troca de Torneiras", "val": 90.0, "km": 1.1, "cat": "Encanador", "urg": False, "tel": "5511777777777", "loc": "Rua Narciso Sturlini, 55"}
    ]

# --- 3. SIDEBAR (PERFIL E SALDO) ---
with st.sidebar:
    st.markdown(f"""
        <div class="wallet-box">
            <small>MEU SALDO GS</small><br>
            <span style="font-size: 32px; font-weight: 900;">R$ {st.session_state.saldo:.2f}</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**Nível Atual: Prata** ({st.session_state.xp}% para Ouro)")
    st.progress(st.session_state.xp / 100)
    
    menu = st.radio("Navegação", ["🚀 Radar de Missões", "🏢 Central da Empresa", "🏆 Ranking Global", "⚙️ Configurações"])
    
    if st.button("Sair do Sistema"):
        st.stop()

# --- 4. TELAS ---

if menu == "🚀 Radar de Missões":
    if st.session_state.missao_ativa:
        m = st.session_state.missao_ativa
        st.title("⚡ Missão Ativa")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"**DESTINO:** {m['loc']}")
            st.link_button("🗺️ ABRIR NO GOOGLE MAPS", f"https://www.google.com/maps/search/?api=1&query={m['loc'].replace(' ', '+')}", use_container_width=True)
        with col2:
            zap_msg = f"Olá, sou o prestador da GS Consultoria e aceitei sua missão de {m['serv']}. Estou a caminho!"
            st.link_button("💬 CHAMAR NO WHATSAPP", f"https://wa.me/{m['tel']}?text={zap_msg}", use_container_width=True)

        st.divider()
        with st.container(border=True):
            st.subheader("Finalização")
            cam = st.camera_input("Foto do serviço pronto")
            if st.button("CONCLUIR E RECEBER R$ " + str(m['val']), type="primary"):
                if cam:
                    with st.spinner("Processando pagamento..."):
                        time.sleep(2)
                        st.session_state.saldo += m['val']
                        st.session_state.xp += 5
                        st.session_state.historico.append(m)
                        st.session_state.missao_ativa = None
                        st.success("Pagamento Creditado!")
                        st.balloons()
                        st.rerun()
                else:
                    st.error("Anexe a foto para comprovar o serviço.")

    else:
        st.title("📲 Radar GS Osasco")
        
        # Filtros Rápidos
        f_col1, f_col2 = st.columns(2)
        dist_limite = f_col1.slider("Raio de distância (km)", 1, 30, 10)
        cat_filtro = f_col2.multiselect("Categorias", ["Zeladoria", "Encanador", "Montador", "Beleza"], default=["Zeladoria", "Encanador", "Montador", "Beleza"])
        
        vagas = [v for v in st.session_state.missoes if v['km'] <= dist_limite and v['cat'] in cat_filtro]
        
        if not vagas:
            st.warning("Nenhuma missão encontrada nesse raio de distância.")
        else:
            for v in vagas:
                u_style = "urgent-card" if v['urg'] else ""
                st.markdown(f"""
                <div class="mission-card {u_style}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="badge-verified">✅ CLIENTE VERIFICADO</span>
                        <span style="font-weight: bold; color: #666;">📍 {v['km']} km</span>
                    </div>
                    <h2 style="margin: 10px 0; font-size: 22px;">{v['serv']}</h2>
                    <p style="color: #444; margin: 0;"><b>Empresa:</b> {v['emp']}</p>
                    <p style="color: #777; font-size: 14px;">{v['loc']}</p>
                    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 15px;">
                        <span class="price-tag">R$ {v['val']:.2f}</span>
                        <span style="background: #EEE; padding: 4px 10px; border-radius: 8px; font-size: 12px;">{v['cat']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"ACEITAR TRABALHO #{v['id']}", key=f"v_{v['id']}"):
                    st.session_state.missao_ativa = v
                    st.session_state.missoes = [x for x in st.session_state.missoes if x['id'] != v['id']]
                    st.rerun()

elif menu == "🏆 Ranking Global":
    st.title("🏆 Melhores de Osasco")
    st.write("Os top 3 ganham bônus de 5% em todas as missões!")
    
    ranking_data = {
        "Posição": ["1º", "2º", "3º", "4º"],
        "Prestador": ["Geovani Santi", "Marcos Silva", "Antônia Souza", "Lucas Lima"],
        "Missões": [142, 128, 115, 98],
        "Avaliação": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐"]
    }
    st.table(pd.DataFrame(ranking_data))

elif menu == "🏢 Central da Empresa":
    st.title("🏢 Painel do Contratante")
    st.write("Publique vagas e encontre profissionais em minutos.")
    
    with st.form("pub"):
        serv_n = st.text_input("Nome do Serviço")
        end_n = st.text_input("Endereço Completo")
        tel_n = st.text_input("WhatsApp para Contato (Ex: 5511...)")
        c1, c2, c3 = st.columns(3)
        cat_n = c1.selectbox("Categoria", ["Zeladoria", "Encanador", "Montador", "Beleza"])
        val_n = c2.number_input("Valor", 50.0)
        urg_n = c3.checkbox("Urgente?")
        
        if st.form_submit_button("🚀 PUBLICAR NO RADAR"):
            nova = {
                "id": random.randint(1000, 9999), "emp": "GS Consultoria", 
                "serv": serv_n, "loc": end_n, "val": val_n, "cat": cat_n, 
                "urg": urg_n, "km": 3.5, "tel": tel_n
            }
            st.session_state.missoes.append(nova)
            st.success("Vaga enviada para o Radar!")
    
