import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="Maybank AI Chatbot", page_icon="🤖")
st.title("Maybank AI Chatbot")

#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "deepseek-v4-pro"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What is up?")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )