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
    st.info("API Key를 입력해야 대화를 시작할 수 있습니다.", icon="🗝️")
    st.stop()

# -------------------------------
# 🤖 모델 선택
# -------------------------------
model = st.selectbox(
    "모델 선택",
    ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4-turbo"],
    index=0,
    help="모델에 따라 응답 품질과 속도가 다를 수 있습니다."
)

# -------------------------------
# 💬 채팅 상태 관리
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요? 😊"}
    ]

# ✅ 대화 초기화 버튼
if st.button("🧹 대화 초기화"):
    # 전체 세션을 지우지 말고 messages만 초기화
    st.session_state.messages = [
        {"role": "assistant", "content": "대화를 새로 시작합니다. 무엇을 도와드릴까요?"}
    ]
    st.rerun()  # ✅ 최신 rerun 사용

# -------------------------------
# 🧠 OpenAI 클라이언트 생성
# -------------------------------
client = OpenAI(api_key=st.session_state.api_key)

# -------------------------------
# 💬 기존 대화 표시
# -------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# ✍️ 사용자 입력 및 응답 처리
# -------------------------------
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI 응답 생성
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 실시간 스트리밍 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"❌ 오류 발생: {str(e)}")
