import streamlit as st
import random
import time
import os
from AgentAI import AgentAI

API_KEY_GEMINI = st.secrets("API_KEY_GEMINI")

chat_instruction = '''Você está ajudando uma pessoa a aprender ingles
e tem a tarefa de manter uma conversa interessante de descontraida no idioma inglês.
Priorize frases curtas e fáceis de ler'''
chatbot = AgentAI(API_KEY_GEMINI).create_new_agent(chat_instruction, chat_agent=True)

aval_instruction = '''Você é um professor de inglês e avalia se a frase escrita está correta.
Avalie de forma gramatical se a frase está correta de acordo com as regras gramaticais da lingua inglesa.
Caso não esteja correto, Reponda em português onde está o erro e reescreva a frase de forma correta.
Caso esteja correta, responda: Muito bem, frase correta!'''
avaliador = AgentAI(API_KEY_GEMINI).create_new_agent(aval_instruction, chat_agent=False)

trad_instruction = '''Você é tradutor de idiomas especialista em tradução das linguas inglesa e portugues.
Após cada frase, se a frase estiver em portugues, responda apenas a tradução em ingles.
Se a frase estiver em ingles, responda apenas a tradução em portugues.'''
tradutor = AgentAI(API_KEY_GEMINI).create_new_agent(trad_instruction, chat_agent=False)

# Streamed response emulator
# def randon_response():
#     response = random.choice(
#         [
#             "Hello there! How can I assist you today?",
#             "Hi, human! Is there anything I can help you with?",
#             "Do you need help?",
#         ]
#     )
#     return response

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_message" not in st.session_state:
    st.session_state.last_message = ""

# Tela lateral de opções
with st.sidebar:
    st.title("Lang-Teacher - Professor de Linguas")
    st.markdown("Powered Gemini - Google")
    st.markdown("Desafio Alura")

    with st.popover("Escolha a Lingua"):
        lingua_nativa = st.selectbox("Lingua Nativa", ("Portuguese", "English"))
        lingua_praticar = st.selectbox("Lingua que deseja praticar", ("Portuguese", "English"))

    with st.expander("Avaliar última Frase enviada"):
        on = st.toggle("Ativar avaliação")
        if on:
            if st.session_state.last_message == '':
                st.markdown("Começe a conversa no chat")
            else:
                avaliacao = avaliador.response(st.session_state.last_message)    
                st.markdown(avaliacao)

    with st.expander("Tradução Instantânea"):
        sentence = st.text_input("Insira o que deseja traduzir")
        if st.button("Traduzir"):
            traducao = tradutor.response(sentence)
            st.text_input("Texto traduzido", traducao)
        

# Tela de Chat
st.title("Chat Lang-Teacher")
st.markdown("Converse com a IA para praticar seu inglês!")

def response_generator(message):
    for word in message.split():
        yield word + " "
        time.sleep(0.1)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message = chatbot.response(prompt)
        response = st.write_stream(response_generator(message))

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.last_message = prompt