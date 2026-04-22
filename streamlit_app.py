import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Chatbot", page_icon="💬", layout="centered")

st.title("💬 AI Chatbot")
st.caption("Powered by OpenAI")

with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.environ.get("OPENAI_API_KEY", ""),
        help="Get one at https://platform.openai.com/api-keys",
    )
    model = st.selectbox(
        "Model",
        ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0,
    )
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful, friendly AI assistant.",
        height=100,
    )
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your message..."):
    if not api_key_input:
        st.error("Please enter your OpenAI API key in the sidebar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        client = OpenAI(api_key=api_key_input)
        api_messages = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            stream = client.chat.completions.create(
                model=model,
                messages=api_messages,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
    except Exception as e:
        st.error(f"Error: {e}")
        st.session_state.messages.pop()
