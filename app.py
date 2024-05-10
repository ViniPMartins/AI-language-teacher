import streamlit as st
import random
import time
import os
from AgentAI import AgentAI
#import google.generativeai as genai

API_KEY_CHATBOT = st.secrets["API_KEY_CHATBOT"]
API_KEY_AVALIA = st.secrets["API_KEY_AVALIA"]
API_KEY_TRADUTOR = st.secrets["API_KEY_TRADUTOR"]

def create_agents(lang_nat, lang_practice):
    chat_instruction = f'''Você está ajudando uma pessoa a aprender {lang_practice}
    e tem a tarefa de manter uma conversa interessante de descontraida no idioma {lang_practice}.
    Priorize frases curtas e fáceis de ler'''
    chatbot = AgentAI(API_KEY_CHATBOT)
    chatbot.create_new_agent(chat_instruction, chat_agent=True)

    aval_instruction = f'''Você é um professor de {lang_practice} e avalia se a frase escrita está correta.
    Avalie de forma gramatical se a frase está correta de acordo com as regras gramaticais do {lang_practice}.
    Caso não esteja correto, Reponda em {lang_nat} onde está o erro e reescreva a frase de forma correta.
    Caso esteja correta, responda: Muito bem, frase correta!, no idioma {lang_nat}'''
    avaliador = AgentAI(API_KEY_AVALIA)
    avaliador.create_new_agent(aval_instruction, chat_agent=False, model_name='gemini-1.5-pro-latest')

    trad_instruction = f'''Você é tradutor de idiomas especialista em tradução das linguas {lang_practice} e {lang_nat}.
    Após cada frase, se a frase estiver em {lang_nat}, responda apenas a tradução em {lang_practice}.
    Se a frase estiver em {lang_practice}, responda apenas a tradução em {lang_nat}.'''
    tradutor = AgentAI(API_KEY_TRADUTOR)
    tradutor.create_new_agent(trad_instruction, chat_agent=False, model_name='gemini-1.5-pro-latest')

    return chatbot, avaliador, tradutor

st.set_page_config(
   page_title="Language Teacher",
   page_icon="📚",
   layout="wide",
)

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
        lingua_nativa = st.text_input("Digite sua Lingua Nativa", "Portugues")
        lingua_praticar = st.text_input("Lingua que deseja praticar", "Inglês")

    chatbot, avaliador, tradutor = create_agents(lingua_nativa, lingua_praticar)

    with st.expander("Avaliar última Frase enviada"):
        if st.button("Avaliar"):
            if st.session_state.last_message == '':
                st.markdown("Começe a conversa no chat")
            else:
                avaliacao = avaliador.response(st.session_state.last_message)    
                st.markdown(f"Mensagem: {st.session_state.last_message}")
                st.markdown(f"Avaliação: {avaliacao}")

    with st.expander("Tradução Instantânea"):
        sentence = st.text_input("Insira o que deseja traduzir")
        if st.button("Traduzir"):
            traducao = tradutor.response(sentence)
            st.text_input("Texto traduzido", traducao)
        

# Tela de Chat
st.title("Chat Lang-Teacher")
st.markdown(f"Converse com a IA para praticar!")

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