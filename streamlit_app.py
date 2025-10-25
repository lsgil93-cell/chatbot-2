import streamlit as st
from openai import OpenAI

# -------------------------------
# 🎨 기본 UI 설정
# -------------------------------
st.set_page_config(page_title="💬 Chatbot", page_icon="💬", layout="centered")

st.title("💬 OpenAI Chatbot")
st.write(
    "간단한 AI 챗봇입니다. OpenAI API Key를 입력하면 대화를 시작할 수 있습니다. "
    "API Key는 [여기서 발급](https://platform.openai.com/account/api-keys) 가능합니다."
)

# -------------------------------
# 🔑 API Key 입력 및 저장
# -------------------------------
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

openai_api_key = st.text_input(
    "🔐 OpenAI API Key를 입력하세요",
    type="password",
    value=st.session_state.api_key,
)

if openai_api_key:
    st.session_state.api_key = openai_api_key

if not st.session_state.api_key:
    st.info("AP
