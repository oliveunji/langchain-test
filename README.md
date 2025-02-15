# 면접관 AI 서비스

환경변수 설정 
1. Azure AI Foundry에서 LLM 모델 생성후 다음의 화면에서 **대상 URI** 값과 **키** 복사
![alt text](/images/azure_portal.png)

2. 다음과 같이 환경변수 코드에 붙여넣기 
    ```
    os.environ["AZURE_OPENAI_API_KEY"] = "키값 붙여넣기"
    // 아래와 같이 ~.openai.azure.com 까지만 URI 붙여넣기 
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://eunk-oai.openai.azure.com"

    ```

실행스크립트 
```
streamlit run job_interviewer.py
```

실행화면
![면접관 AI 서비스](/images/ai_service.png)