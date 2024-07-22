from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os

def kor_to_eng(question : str) -> str:
    # Azure OpenAI 클라이언트 설정
    client = AzureChatOpenAI(
        openai_api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version = "2023-05-15",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )

    # 게임 속의 특정 용어를 한국어로 두고 싶다면 아래 문구를 추가하세요
    # system_message에 추가 : 2. Preserving all game-specific terminology exactly as it appears in Korean, without translation or explanation.
    # human_message에 추가  : 1. Keep all game-specific terms in their original Korean form without translation.
    
    system_message = SystemMessage(content="""You are a specialized translator for board game discussions. Your task is to translate Korean questions about board game situations into clear, concise English. Focus on:
    1. Accurately conveying the user's intent and any implied questions.
    2. Maintaining the original context and game situation details.
    3. Structuring the translation to be easily understood by an AI language model that has been trained on board game rulebooks.
        Translate in a way that allows an AI to provide expert analysis on the board game situation, assuming it has full knowledge of game rules and terms.
    """)

    human_message = HumanMessage(content=f"""Translate the following Korean text about a board game situation into English:

    '{question}'

    In your translation:
    1. Maintain the original question's intent and any implicit queries.
    2. Structure the translation clearly for easy processing by an AI language model.
    3. Translate all game-specific terms into English, assuming the AI understands all board game terminology..""")
    
    messages = [system_message, human_message]
    
    response = client.invoke(messages)
    
    return response.content
  
if __name__ == "__main__":
  translated_text = kor_to_eng("순서는 시계반대 방향으로 돌고 있고 라임 하나 나온 플레이어가 종을 쳤는데 이때 누가 카드를 가져가야해?")
  print(translated_text)