
import os
from dotenv import load_dotenv

load_dotenv()

from langchain import HuggingFaceHub
llm_huggingface = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature":0, "max_length":60})

import streamlit as st
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)

def init_page() -> None:
    st.set_page_config(
        page_title="Chat Bot"
    )
    st.header("Chat Bot")
    st.sidebar.title("Optoins")

def init_messages() -> None:
    clear_button = st.sidebar.button("Clear Conversation", key="Clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(
                content = "you are a helful AI assistant. Reply your answer in markdown format."   
            )
        ]

def get_answer(messages) -> str:
    response = llm_huggingface.predict(messages)
    return response

def main() -> None:
    init_page()
    #creating model
    init_messages() 

    if user_input := st.chat_input("Input your question!"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Bot is typing ..."):
            answer = get_answer(user_input)
            print(answer)
        st.session_state.messages.append(AIMessage(content=answer))


    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)

if __name__ == "__main__":
    main()

