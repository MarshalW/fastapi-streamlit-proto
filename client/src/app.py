import streamlit as st
import requests
from typing import Generator

st.title("基于SSE的前后端分离原型")

# 初始消息
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant",
            "content": "请提出有关《孔乙己》的问题"}
    ]

# 显示输入框
if prompt := st.chat_input(placeholder="这里输入问题，换行请使用 Shift+Enter。"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt})


# 显示之前的消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.messages) > 0:
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):

            headers = {
                "Content-Type": "application/json",
                "accept": "text/event-stream"
            }
            response = requests.post(
                url="http://llm-server:7777/query",
                json={"query": prompt},
                headers=headers,
                stream=True,
            )

            response = st.write_stream(
                response.iter_content(decode_unicode=True))
            
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
