from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from dotenv import load_dotenv
import os
import base64

def img_model() -> list:
    # 환경 변수 로드
    load_dotenv()
    current_directory = os.getcwd()

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

    # 보드게임 이미지 처리
    image_folder = os.path.join(current_directory, 'src/model/photo')
    
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    encoded_images = []
    
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        base64_image = encode_image(image_path)
        encoded_images.append(base64_image)
        # print(f"\n인코딩된 이미지 ({image_file}):")
        # print(base64_image)
        print("\n")
        
    return encoded_images

if __name__ == "__main__":
    results = img_model()