import os
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

def chat_loop():
    messages = []
    print("대화를 시작합니다. 종료하려면 'quit'를 입력하세요.")
    while True:
        user_input = input("사용자: ")
        if user_input.lower() == 'quit':
            break
        
        messages.append(HumanMessage(content=user_input))
        prompt = prompt_template.invoke({"messages": messages})
        response = model.invoke(prompt)
        ai_response = response.content
        print("AI: " + ai_response)
        messages.append(AIMessage(content=ai_response))

if __name__ == "__main__":
    chat_loop()
