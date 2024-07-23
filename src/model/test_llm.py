from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os

def test_llm(text: str) -> str:
    load_dotenv()
    
    # Azure OpenAI 클라이언트 설정
    client = AzureChatOpenAI(
        openai_api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version = "2023-05-15",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )
    
    system_message = SystemMessage(content="""You are a specialized translator for board game discussions. 너무 많은 부연 설명은 하지 말고 간단히 답해줘. 너무 짧게 대답해도 안돼.
    """)
    
    human_message = HumanMessage(content=f"""내 질문에 대해 답해줘. 너무 길게는 답하지마. 내 질문은
    '{text}'
    """)
    
    messages = [system_message, human_message]
    
    response = client.invoke(messages)
    
    return response.content
  

if __name__ == "__main__":
    input_chat = "루미큐브 처음에 낼 때 숫자합이 30 넘어야 돼?"
    print(test_llm(input_chat))