from PIL import Image
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import cv2
import io
import os
import base64

def img_model(image_path: str, game_name: str,) -> str:
    load_dotenv()
    
    # Azure OpenAI 클라이언트 설정
    client = AzureChatOpenAI(
        openai_api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version = "2023-05-15",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )
    
    # 사진 압축 함수
    # def compress_model(image_path: str, max_size=(700, 700), quality=95) -> str:
    #     with Image.open(image_path) as img:
    #         img = img.convert("RGB")
    #         img.thumbnail(max_size)
            
    #         # 압축된 이미지 크기를 출력
    #         width, height = img.size
    #         print(f"Compressed image size: {width}x{height}")
            
    #         buffer = io.BytesIO()
    #         img.save(buffer, format="JPEG", quality=quality)  # Save the image to a buffer with JPEG compression
            
    #         # 압축된 이미지를 파일로 저장
    #         current_directory = os.getcwd()
    #         output_dir = os.path.join(current_directory, 'data', 'compressed_images')
    #         os.makedirs(output_dir, exist_ok=True)
    #         output_path = os.path.join(output_dir, os.path.basename(image_path))
    #         with open(output_path, "wb") as f:
    #             f.write(buffer.read())
                
    #         buffer.seek(0)
    #         encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
    #     return encoded_image
    
    def encode_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_image

    def extract_info_from_image(image_path, prompt, game_name):

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
                    "text": "보드게임 중에 사진과 같은 상황이 발생했습니다. 보드게임이 {game_name}임을 명심하고, {game_name}에서 벌어진 이 상황에 대한 내용을 설명해주세요."
                }
            ])
        ]

        response = client.invoke(messages)
        return response.content
    
    # 프롬프트 템플릿
    prompt = f'''
    You are the best expert in interpreting board games. Carefully analyze the given one or multiple images of the board game in progress and accurately extract the following information.
    The provided photo is at the point of the user's question. **Describe it exactly as you see it**, as if you were explaining a single picture, detailing the arrangement and objects comprehensively. Describe everything so precisely that someone could draw the exact picture just by listening to your explanation.
    Make sure to mention every single detail!! Provide very, very detailed answers about objects related to the board game.

    Information to extract:
    - Current progress
    - Number of players Number of players (pay special attention to the number of card piles, hands, player pieces, and player actions)
    - What each player is doing (based on the cards they have played and their positions)
    - Where and how each item is positioned in the current game situation (describe the position of each card, game pieces, the bell if present, and any other objects)

    Precautions:
    1. The board game shown in the photo is the {game_name} board game. Do not confuse it with other board games.
    2. Clearly distinguish between different players by describing each player's area separately, including their cards, hands, and actions.
    3. Explain in a way that the LLM can easily understand.
    4. If there is no information, set the field to ("No information available").
    5. Strictly adhere to the String format.

    Additional instructions:
    Carefully analyze one or multiple images to provide accurate information.
    It is very important to determine the number of players. Carefully judge the objects, such as the number of card piles, game pieces, and the positions of the players, to accurately determine the number of players, considering the typical setup and rules of the {game_name} board game.

    '''
    
    result = extract_info_from_image(image_path, prompt, game_name)
    
    return result

if __name__ == "__main__":
    current_directory = os.getcwd()
    search_folder = os.path.join(current_directory, 'data', 'photo')
    image_path = os.path.join(search_folder, "rummikub.jpg")
    game_name = "rummikub"
    
    results = img_model(image_path, game_name)
    print(results)

# def img_model(image_path: str, max_size=(800, 800), quality=85) -> str:
#     with Image.open(image_path) as img:
#         img = img.convert("RGB")
#         img.thumbnail(max_size)
#         buffer = io.BytesIO()
#         img.save(buffer, format="JPEG", quality=quality)  # Save the image to a buffer with JPEG compression
#         buffer.seek(0)
#         encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
#     return encoded_image

# def img_model(img_file_path : str) -> str:
#     load_dotenv()

#     def encode_image(img_file_path):
#         with open(img_file_path, "rb") as image_file:
#             return base64.b64encode(image_file.read()).decode('utf-8')
    
#     if not img_file_path:
#         raise FileNotFoundError("No image files found in the specified directory.")

#     # 이미지 파일 인코딩
#     encoded_image = encode_image(img_file_path)
        
#     return encoded_image

