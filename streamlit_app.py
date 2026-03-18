import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="LuzSocial v6.0", page_icon="⚡", layout="centered")

# ESTILO CSS PROFISSIONAL
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .card { background-color: white; padding: 20px; border-radius: 15px; border-left: 10px solid #1A237E; margin-bottom: 20px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); }
    .imposto { color: #d32f2f; font-size: 13px; font-weight: bold; }
    .liquido { color: #2e7d32; font-size: 20px; font-weight: bold; }
    .bruto { color: #757575; font-size: 13px; text-decoration: line-through; }
    .curso-box { background-color: #e3f2fd; padding: 15px; border-radius: 10px; border: 1px solid #1e88e5; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO DE VARIÁVEIS
if 'status' not in st.session_state: st.session_state.status = "login"
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0

# --- TELA DE LOGIN ---
if st.session_state.status == "login":
    st.title("⚡ LuzSocial")
    st.subheader("GS Consultoria & Inovação")
    st.write("Bem-vindo ao futuro do trabalho em Osasco.")
    user = st.text_input("CPF ou Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("ACESSAR SISTEMA"):
        st.session_state.status = "menu"
        st.rerun()

# --- MENU PRINCIPAL ---
elif st.session_state.status == "menu":
    st.title("📂 Central de Oportunidades")
    
    aba = st.selectbox("Selecione uma área:", 
                      ["Mural de Missões", "Escola de Profissões (Cursos Gov)"])

    if aba == "Mural de Missões":
        categoria = st.radio("Filtrar por tipo:", ["Zeladoria Urbana", "Serviços Domésticos", "Comunitário"])
        
        # Base de dados (Nome, Local, Valor Bruto)
        if categoria == "Zeladoria Urbana":
            vagas = [
                {"n": "Varrer Praça da Matriz", "l": "Centro", "b": 30.0},
                {"n": "Limpeza de Bueiro", "l": "Rochdale", "b": 60.0}
            ]
        elif categoria == "Serviços Domésticos":
            vagas = [
                {"n": "Cozinheira (Almoço)", "l": "Vila Yara", "b": 150.0},
                {"n": "Diarista / Limpeza", "l": "Bela Vista", "b": 180.0}
            ]
        else:
            vagas = [{"n": "Passeador de Cães", "l": "Vila Campesina", "b": 40.0}]

        for v in vagas:
            imp = v['b'] * 0.15 # 15% Imposto
            liq = v['b'] - imp
            st.markdown(f"""
                <div class="card">
                    <h3>{v['n']}</h3>
                    <p>📍 {v['l']}</p>
                    <p class="bruto">Bruto: R$ {v['b']:.2f}</p>
                    <p class="imposto">⬇️ Imposto Gov: R$ {imp:.2f}</p>
                    <p class="liquido">💰 Receba Líquido: R$ {liq:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ACEITAR: {v['n']}", key=v['n']):
                st.session_state.missao = {"nome": v['n'], "valor": liq}
                st.session_state.status = "mapa"
                st.rerun()

    elif aba == "Escola de Profissões (Cursos Gov)":
        st.subheader("🎓 Capacitação Gratuita")
        st.write("Estude pelos links oficiais e aumente seus ganhos!")
        
        st.markdown("""
            <div class="curso-box">
                <h4>🛠️ Pintura Profissional (GOV.BR)</h4>
                <p>Aprenda técnicas de acabamento e proteção.</p>
                <a href="https://www.gov.br/pt-br/temas/escola-do-trabalhador" target="_blank">ACESSAR CURSO GRATUITO</a>
            </div>
            <div class="curso-box">
                <h4>🥘 Higiene e Manipulação (SEBRAE)</h4>
                <p>Essencial para cozinheiras e auxiliares.</p>
                <a href="https://www.sebrae.com.br" target="_blank">ACESSAR CURSO GRATUITO</a>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        cert = st.file_uploader("Já tem o certificado? Envie aqui para liberar missões premium:")
        if cert:
            st.success("Certificado recebido! Validando junto ao órgão emissor...")

# --- MAPA ---
elif st.session_state.status == "mapa":
    st.header(f"🗺️ Destino: {st.session_state.missao['nome']}")
    map_df = pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]})
    st.map(map_df)
    if st.button("CHEGUEI NO LOCAL"):
        st.session_state.status = "foto"
        st.rerun()

# --- FOTO E PAGAMENTO ---
elif st.session_state.status == "foto":
    st.header("📸 Finalização")
    st.camera_input("Foto do serviço pronto")
    if st.button("CONCLUIR E RECEBER"):
        st.session_state.saldo += st.session_state.missao['valor']
        st.session_state.status = "pago"
        st.rerun()

elif st.session_state.status == "pago":
    st.balloons()
    st.success(f"✅ Pago! R$ {st.session_state.missao['valor']:.2f} na conta.")
    st.write(f"### Saldo Acumulado: R$ {st.session_state.saldo:.2f}")
    if st.button("VOLTAR AO MENU"):
        st.session_state.status = "menu"
        st.rerun()
