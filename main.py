import os
import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Azure OpenAI 설정
os.environ["AZURE_OPENAI_API_KEY"] = "YOUR_AZURE_OPENAI_API_KEY"
os.environ["AZURE_OPENAI_ENDPOINT"] = "YOUR_AZURE_OPENAI_ENDPOINT"

# AzureChatOpenAI 모델 초기화
model = AzureChatOpenAI(
    openai_api_version="2024-08-01-preview",
    azure_deployment="gpt-4o-mini",
    temperature=0.7
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 도움이 되는 한국어 어시스턴트입니다."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Streamlit 앱 시작
st.title("AI 채팅 어시스턴트")

# 세션 상태에 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사용자 입력
user_input = st.text_input("질문을 입력하세요:")

if user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append(HumanMessage(content=user_input))
    
    # AI 응답 생성
    prompt = prompt_template.invoke({"messages": st.session_state.messages})
    response = model.invoke(prompt)
    
    # AI 메시지 추가
    st.session_state.messages.append(AIMessage(content=response.content))

# 대화 내용 표시
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        st.text_area("사용자:", value=message.content, height=100, disabled=True)
    elif isinstance(message, AIMessage):
        st.text_area("AI:", value=message.content, height=100, disabled=True)

# 대화 초기화 버튼
if st.button("대화 초기화"):
    st.session_state.messages = []
    st.experimental_rerun()
