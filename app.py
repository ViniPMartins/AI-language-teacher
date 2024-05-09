import streamlit as st
import random
import time


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

with st.sidebar:
    st.title("Simple chat")

    with st.popover("Escolha a Lingua"):
        lingua_nativa = st.selectbox("Lingua Nativa", ("Portuguese", "English"))
        lingua_praticar = st.selectbox("Lingua que deseja praticar", ("Portuguese", "English"))

    with st.expander("Avaliar última Frase enviada"):
        st.markdown("A explicação estará aqui")

    with st.expander("Traduzir última resposta"):
        st.markdown("A outras explicação estará aqui")
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_message" not in st.session_state:
    st.session_state.last_message = ""

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.last_message = prompt