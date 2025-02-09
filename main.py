import os
import streamlit as st
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Azure OpenAI 설정
os.environ["AZURE_OPENAI_API_KEY"] = "YOUR_AZURE_OPENAI_API_KEY"
os.environ["AZURE_OPENAI_ENDPOINT"] = "YOUR_AZURE_OPENAI_ENDPOINT"

# AzureChatOpenAI 모델 초기화
model = AzureChatOpenAI(
    openai_api_version="2024-08-01-preview",
    azure_deployment="gpt-4o-mini",
    temperature=0.7
)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-ada-002",
    model = "text-embedding-ada-002"
)
vectorstore = Chroma(
    collection_name="rag_docs",
    embedding_function=embeddings, 
    persist_directory="./chroma_db"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", """당신은 컨텍스트 정보를 사용해 질문에 답변하는 도우미입니다. 다음 지침을 따르세요:
    1. 주어진 컨텍스트를 기반으로 답변
    2. 모르는 내용은 '잘 모르겠습니다'라고 답변
    3. 한국어로 간결하게 답변
    
    컨텍스트: {context}"""),
        ("user", "{input}")
    ]
)
document_chain = create_stuff_documents_chain(model, prompt_template)
retrieval_chain = create_retrieval_chain(vectorstore.as_retriever(), document_chain)

# Streamlit 앱 시작
st.title("AI 채팅 어시스턴트")

with st.sidebar:
    uploaded_files = st.file_uploader(
        "지식 문서 업로드 (PDF/TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        documents = []
        for file in uploaded_files:
            if file.type == "text/plain":
                text = file.getvalue().decode("utf-8")
                documents.extend([Document(page_content=text)])
            # PDF 처리 구현 필요 (예: pypdf 설치 후 추가)
        
        chunks = text_splitter.split_documents(documents)
        vectorstore.add_documents(chunks)
        st.toast(f"{len(chunks)}개 문서 청크 저장 완료!", icon="✅")

# 세션 상태에 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("질문을 입력하세요:"):
    # 사용자 메시지 추가
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    # AI 응답 생성 (수정된 부분)
    try:
        response = retrieval_chain.invoke({"input": prompt})
        ai_message = AIMessage(content=response["answer"])
        st.session_state.messages.append(ai_message)
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")

for message in st.session_state.messages:
    with st.chat_message("human" if isinstance(message, HumanMessage) else "ai"):
        st.markdown(message.content)

# 대화 초기화 버튼
if st.button("대화 초기화"):
    st.session_state.messages = []
    st.rerun()
