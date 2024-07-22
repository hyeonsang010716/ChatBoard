from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from dotenv import load_dotenv
import os
import base64

def multimodal(game_name, user_question):
    # 환경 변수 로드
    load_dotenv()

    # Azure OpenAI 클라이언트 설정
    client = AzureChatOpenAI(
        openai_api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version = "2023-05-15",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def extract_info_from_image(image_path, prompt):
        base64_image = encode_image(image_path)

        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                },
                {
                    "type": "text",
                    "text": "보드게임 중에 사진과 같은 상황이 발생했습니다. 이 상황을 글로 해석해주고 질문에 대한 답을 해주세요."
                }
            ])
        ]

        response = client.invoke(messages)
        return response.content

    # 프롬프트 템플릿
    prompt = f'''
    당신은 보드게임을 해석하는 최고의 전문가입니다. 주어진 하나 또는 여러 장의 보드게임 진행 상황 이미지를 세심하게 분석하여 다음 정보를 정확하게 추출해주세요. 여러 이미지가 주어진 경우, 각 이미지를 연결하여 인과관계나 순서를 고려하세요.
    사용자가 묻는 질문에 대한 답을 해주세요. 사용자의 질문은 {user_question}입니다. 제공된 사진이 사용자가 질문하는 시점입니다.

    추출할 정보:
        - 현재 진행 상황
        - 플레이어의 수
        - 각 플레이어가 어떤 행동을 하고 있는지
        - 반칙 여부 및 반칙을 한 플레이어와 반칙 내용
        - 여러 이미지 간의 변화 설명 (여러 이미지가 주어진 경우)
        - 현재 상황에서 룰 적용함에 따라 어떤 동작이 이루어져야하는지.
        - 사용자의 질문에 대한 대답 찾기

    주의사항:
    1. 사진에 제시된 보드게임은 {game_name} 보드게임입니다. 다른 보드게임과 착각하지 마세요.
    2. 사람이 이해하기 쉽게 설명해주세요.
    3. 반칙이 발생한 경우, 어떤 플레이어가 어떤 반칙을 했는지 설명해주세요.
    4. 정보가 없는 경우 해당 필드를 ("정보가 없습니다.")로 설정하세요.
    5. String 형식을 엄격히 준수하세요.
    6. 사진이 여러장인 경우 사진 사이에 변화를 주목하세요. 사진을 이어서 sequence로 생각해야합니다.
    """

    추가 지시사항:
    하나 또는 여러 이미지를 면밀히 분석하여 정확한 정보를 제공해주세요.
    제시된 보드게임의 룰을 정확하게 파악하고 그에 대한 룰을 적용해서 답해주세요!
    너무 길게 설명하지 마세요. 간단히 설명해주세요.
    플레이어 수를 파악하는 건 아주 중요합니다. 사물을 잘 판단하여 플레이어 수를 정확히 파악하세요.
    '''

    # 보드게임 이미지 처리
    image_folder = '/root/LLM_Bootcamp/ChatBoard/src/model/photo'        # 해당 루트로 변경
    
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        result = extract_info_from_image(image_path, prompt)
        print(f"\n게임 정보 ({image_file}):")
        print(result)
        print("\n")
    return result  # 모든 결과를 반환

# 메인 함수 실행
if __name__ == "__main__":
    results = multimodal("할리갈리", "순서는 시계반대 방향으로 돌고 있고 라임 하나 나온 플레이어가 종을 쳤는데 이때 누가 카드를 가져가야해?")
    print("해석 완료")