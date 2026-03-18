import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA (WIDE MODE PARA PARECER DASHBOARD)
st.set_page_config(page_title="GS LuzSocial v7.5", page_icon="⚡", layout="wide")

# ESTILO CSS AVANÇADO
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stSidebar { background-color: #1A237E !important; color: white !important; }
    .card { background-color: white; padding: 25px; border-radius: 15px; border-left: 10px solid #1A237E; margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); }
    .liquido { color: #2e7d32; font-size: 24px; font-weight: bold; }
    .imposto { color: #d32f2f; font-size: 14px; font-weight: bold; }
    .bruto { color: #757575; font-size: 14px; text-decoration: line-through; }
    .btn-panic { background-color: #ff1744 !important; color: white !important; border-radius: 10px; font-weight: bold; }
    .whatsapp-btn { background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; display: block; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO DE VARIÁVEIS DE SESSÃO
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0
if 'status' not in st.session_state: st.session_state.status = "menu"

# --- BARRA LATERAL (MENU DE NAVEGAÇÃO) ---
with st.sidebar:
    st.title("⚡ GS Consultoria")
    st.write("### Colaborador: Geovani")
    st.write(f"💰 Saldo: **R$ {st.session_state.saldo:.2f}**")
    st.divider()
    
    escolha = st.radio("Navegação Principal:", 
                      ["📍 Mural de Missões", "🎓 Escola de Profissões", "📊 Meu Extrato", "📞 Suporte & Segurança"])
    
    st.divider()
    if st.button("🚨 BOTÃO DE PÂNICO", use_container_width=True):
        st.error("⚠️ Alerta enviado para Central GS e GPS ativado!")

# --- TELA 1: MURAL DE MISSÕES ---
if escolha == "📍 Mural de Missões":
    st.title("📍 Missões em Osasco")
    aba = st.tabs(["🧹 Zeladoria", "🏠 Domésticos", "🤝 Comunitário"])

    with aba[0]: # Zeladoria
        servicos = [
            {"n": "Varrer Praça da Matriz", "l": "Centro", "b": 35.0},
            {"n": "Limpeza de Bueiro", "l": "Rochdale", "b": 70.0},
            {"n": "Pintura Meio-fio", "l": "Km 18", "b": 55.0}
        ]
        for s in servicos:
            imp = s['b'] * 0.15
            liq = s['b'] - imp
            st.markdown(f"""
                <div class="card">
                    <h3>{s['n']}</h3>
                    <p>📍 Localização: {s['l']}</p>
                    <p class="bruto">Bruto: R$ {s['b']:.2f}</p>
                    <p class="imposto">⬇️ Imposto Retido: R$ {imp:.2f}</p>
                    <p class="liquido">💰 Receba Líquido: R$ {liq:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Aceitar Missão: {s['n']}", key=s['n']):
                st.session_state.missao_atual = {"nome": s['n'], "valor": liq}
                st.session_state.status = "mapa"
                st.rerun()

# --- TELA 2: MAPA E GPS ---
elif st.session_state.status == "mapa":
    st.title(f"🗺️ Rota: {st.session_state.missao_atual['nome']}")
    df_mapa = pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]})
    st.map(df_mapa)
    st.info("Siga para o ponto marcado para iniciar o serviço.")
    if st.button("CHEGUEI E INICIEI TRABALHO"):
        st.session_state.status = "foto"
        st.rerun()

# --- TELA 3: ESCOLA DE PROFISSÕES ---
elif escolha == "🎓 Escola de Profissões":
    st.title("🎓 Portal de Capacitação (GOV/SEBRAE)")
    st.info("Conclua cursos oficiais para liberar missões de Especialista (até R$ 250,00).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div style="background-color:#fff; padding:20px; border-radius:10px; border:1px solid #ddd">
                <h4>🛠️ Zeladoria e Manutenção</h4>
                <p>Fonte: Escola do Trabalhador 4.0</p>
                <a href="https://www.gov.br/pt-br/temas/escola-do-trabalhador" target="_blank">Acessar Curso Gratuito</a>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style="background-color:#fff; padding:20px; border-radius:10px; border:1px solid #ddd">
                <h4>🥘 Higiene Alimentar</h4>
                <p>Fonte: SEBRAE Osasco</p>
                <a href="https://www.sebrae.com.br" target="_blank">Acessar Curso Gratuito</a>
            </div>
        """, unsafe_allow_html=True)

# --- TELA 4: EXTRATO ---
elif escolha == "📊 Meu Extrato":
    st.title("📊 Histórico Financeiro")
    st.metric("Total Acumulado", f"R$ {st.session_state.saldo:.2f}")
    st.write("---")
    st.write("Últimas movimentações:")
    # Tabela Simulada
    data = {"Data": ["18/03/2026", "17/03/2026"], "Serviço": ["Limpeza Urbana", "Cozinha"], "Líquido": [29.75, 127.50]}
    st.table(pd.DataFrame(data))

# --- TELA 5: SUPORTE WHATSAPP ---
elif escolha == "📞 Suporte & Segurança":
    st.title("📞 Central de Suporte GS")
    st.write("Precisa falar com o administrador? Clique no botão abaixo:")
    
    msg = "Olá Geovani, preciso de suporte no app LuzSocial!"
    link_zap = f"https://wa.me/5511917529636?text={msg.replace(' ', '%20')}"
    
    st.markdown(f"""
        <a href="{link_zap}" target="_blank" class="whatsapp-btn">
            💬 CHAMAR GEOVANI NO WHATSAPP
        </a>
    """, unsafe_allow_html=True)
    st.write("---")
    st.write("🏢 **Endereço:** Base Osasco Centro.")

# --- TELAS DE FINALIZAÇÃO ---
elif st.session_state.status == "foto":
    st.title("📸 Comprovação")
    st.camera_input("Tire foto do serviço pronto")
    if st.button("ENVIAR PARA PAGAMENTO"):
        st.session_state.saldo += st.session_state.missao_atual['valor']
        st.session_state.status = "pago"
        st.rerun()

elif st.session_state.status == "pago":
    st.balloons()
    st.success(f"✅ Pagamento de R$ {st.session_state.missao_atual['valor']:.2f} creditado!")
    if st.button("VOLTAR AO MENU"):
        st.session_state.status = "menu"
        st.rerun()
    
