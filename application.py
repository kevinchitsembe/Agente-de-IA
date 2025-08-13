#FRONTEND
#application.py
# application.py
import streamlit as st
import requests

st.set_page_config(page_title="AI Query Agent", page_icon="🤖", layout="centered")

st.title("💬 AI Query Agent")

# Inicializar sessão de histórico
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Escreve aqui a tua pergunta...")

if user_input:
    with st.spinner("A pensar..."):
        response = requests.post("http://localhost:8000/query", json={"user_input": user_input})

        if response.status_code == 200:
            data = response.json()
            bot_reply = data.get("natural_response", "Nenhuma resposta disponível.")
            file_name = data.get("file_name")

            # Guardar no histórico
            st.session_state.chat_history.append({
                "user": user_input,
                "bot": bot_reply,
                "file": file_name
            })
        else:
            bot_reply = "Erro ao processar a solicitação. Tenta novamente."
            st.session_state.chat_history.append({
                "user": user_input,
                "bot": bot_reply,
                "file": None
            })

# Exibir histórico do chat
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("assistant"):
        st.markdown(chat["bot"])
        if chat["file"]:
            download_url = f"http://localhost:8000/download/{chat['file']}"
            st.markdown(f"[📥 Baixar Excel com os dados]({download_url})", unsafe_allow_html=True)
