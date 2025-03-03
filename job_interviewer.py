import os
import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Azure OpenAI 설정
os.environ["AZURE_OPENAI_API_KEY"] = "YOUR_AZURE_OPENAI_API_KEY"
os.environ["AZURE_OPENAI_ENDPOINT"] = "YOUR_AZURE_OPENAI_ENDPOINT"


# AzureChatOpenAI 모델 초기화
model = AzureChatOpenAI(
    openai_api_version="2024-08-01-preview",
    azure_deployment="gpt-4o-mini",
    temperature=0.7
)

# 면접 질문 생성 프롬프트 템플릿
interview_q_prompt = ChatPromptTemplate.from_messages([
    (
        "system", 
        "당신은 면접관 AI입니다. 주어진 잡 디스크립션과 이력서를 바탕으로 지원자에게 묻기 위한 예상 면접 질문 5개를 번호와 함께 생성하세요. 답변은 한국어로 간결하고 명확하게 작성하십시오."
    ),
    (
        "user", 
        "잡 디스크립션: {job_description}\n이력서: {resume}"
    )
])

# 지원자 답변 피드백 프롬프트 템플릿
feedback_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "당신은 면접관 AI입니다. 지원자가 면접 질문에 제시한 답변을 평가하고 피드백을 제공하세요. 피드백은 구체적이며 긍정점과 개선점을 모두 포함해야 합니다."
    ),
    (
        "user",
        "면접 질문: {question}\n지원자 답변: {answer}"
    )
])

st.title("면접관 AI 서비스")

with st.expander("환경변수 확인"):
    env_vars = dict(os.environ)
    st.json(env_vars)

# 사이드바 파일 업로드 섹션
with st.sidebar:
    st.header("파일 업로드")
    job_file = st.file_uploader("잡 디스크립션 파일 업로드 (PDF/TXT)", type=["pdf", "txt"], key="job")
    resume_file = st.file_uploader("이력서 파일 업로드 (PDF/TXT)", type=["pdf", "txt"], key="resume")

job_text = ""
resume_text = ""

# 텍스트 파일 처리 (PDF는 추후 구현)
if job_file:
    if job_file.type == "text/plain":
        job_text = job_file.getvalue().decode("utf-8")
    else:
        job_text = "PDF 파일 처리 기능은 아직 구현되지 않았습니다."

if resume_file:
    if resume_file.type == "text/plain":
        resume_text = resume_file.getvalue().decode("utf-8")
    else:
        resume_text = "PDF 파일 처리 기능은 아직 구현되지 않았습니다."

# 면접 질문 생성
if st.button("면접 질문 생성"):
    if job_text and resume_text:
        messages = interview_q_prompt.format_messages(job_description=job_text, resume=resume_text)
        try:
            interview_questions = model(messages).content
            st.session_state["interview_questions"] = interview_questions
            st.success("면접 질문이 생성되었습니다!")
        except Exception as e:
            st.error(f"면접 질문 생성 중 오류 발생: {str(e)}")
    else:
        st.error("잡 디스크립션과 이력서 파일을 모두 업로드해 주세요.")

# 생성된 면접 질문 출력
if "interview_questions" in st.session_state:
    st.subheader("생성된 면접 질문")
    st.write(st.session_state["interview_questions"])

st.markdown("---")
st.subheader("답변 피드백 받기")

# 사용자가 피드백 받고자 하는 면접 질문과 본인의 답변 입력
feedback_question = st.text_input("피드백 받고자 하는 면접 질문 입력")
candidate_answer = st.text_area("지원자 답변 입력")

if st.button("답변 피드백 받기"):
    if feedback_question and candidate_answer:
        messages = feedback_prompt.format_messages(question=feedback_question, answer=candidate_answer)
        try:
            feedback = model(messages).content
            st.subheader("피드백")
            st.write(feedback)
        except Exception as e:
            st.error(f"피드백 생성 중 오류 발생: {str(e)}")
    else:
        st.error("면접 질문과 지원자 답변을 모두 입력해 주세요.")

# 세션 초기화 (파일 및 생성된 데이터 초기화)
if st.button("세션 초기화"):
    st.session_state.clear()
    st.experimental_rerun()
