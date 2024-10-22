from PIL import Image
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
# import cv2
import io
import os
import base64
import numpy as np
import matplotlib.pyplot as plt

def img_model(image_path: str, game_name: str, player_num: str) -> str:
    load_dotenv()
    
    # Azure OpenAI 클라이언트 설정
    client = AzureChatOpenAI(
        openai_api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version = "2023-05-15",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )
    
    # 사진 압축 함수
    def compress_model(image_path: str, max_size=(1000, 600), quality=90) -> str:
        
        # current_directory = os.getcwd()
        # output_dir = os.path.join(current_directory, 'data', 'photo_enhanced')
        #  # 이미지 경로 확인
        # if not os.path.exists(image_path):
        #     raise FileNotFoundError(f"Image file not found at path: {image_path}")
        
        # img = cv2.imread(image_path)
        # # 라플라시안 필터를 사용하여 이미지 샤프닝
        # kernel = np.array([[0, -1, 0],
        #                 [-1, 5,-1],
        #                 [0, -1, 0]])
        # sharpened = cv2.filter2D(img, -1, kernel)

        # # 결과 이미지를 저장
        # output_image_path = os.path.join(output_dir, os.path.basename(image_path).rsplit('.', 1)[0] + "_sharpened.jpg")
        # cv2.imwrite(output_image_path, sharpened, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        
        with Image.open(image_path) as img:
            enhanced_img = img.convert("RGB")
            enhanced_img.thumbnail(max_size)
            
            # 이미지 크기를 출력
            width, height = enhanced_img.size
            print(f"Compressed image size: {width}x{height}")
            
            buffer = io.BytesIO()
            enhanced_img.save(buffer, format="JPEG", quality=quality)  # Save the image to a buffer with JPEG compression
            print("해상도 낮추기 완료")
                
            buffer.seek(0)
            encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
            print("인코딩 완료")
        return encoded_image
    
    base64_image = compress_model(image_path)
    return base64_image
    
    # def encode_image(image_path: str) -> str:
    #     with open(image_path, "rb") as image_file:
    #         encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    #         print("인코딩 완료")
    #     return encoded_image

    # def extract_info_from_image(image_path, prompt, game_name):
        
    #     base64_image = compress_model(image_path)

    #     messages = [
    #         SystemMessage(content=prompt),
    #         HumanMessage(content=[
    #             {
    #                 "type": "image_url",
    #                 "image_url": {
    #                     "url": f"data:image/jpeg;base64,{base64_image}"
    #                 }
    #             },
    #             {
    #                 "type": "text",
    #                 "text": "A situation like the one in the photo has occurred during a board game. Please explain the situation that has unfolded in the board game {game_name}. The number of players is {player_num}. Please refer to the number of players if necessary."
    #             },
    #         ])
    #     ]

    #     response = client.invoke(messages)
    #     return response.content
    
    # # 프롬프트 템플릿
    # prompt = f'''
    # As a {game_name} expert, analyze the image and describe only the most crucial game elements:

    # 1. Cards/tiles in play
    # 2. Player pieces or tokens
    # 3. Central game board or play area
    # 4. Any special items (e.g., dice, timer, special cards)

    # Describe these elements briefly but precisely. Ignore background details or non-game objects. Confirm the {player_num} player count if possible.

    # Note:
    # - Focus solely on {game_name}-specific items
    # - Provide a concise yet clear description in 8 lines or fewer. Each line should contain a key observation about the game state.
    # - Use "Not visible" for missing key elements
    # '''
    
    # result = extract_info_from_image(image_path, prompt, game_name)
    
    # return result

if __name__ == "__main__":
    current_directory = os.getcwd()
    search_folder = os.path.join(current_directory, 'data', 'photo')
    image_path = os.path.join(search_folder, "halli.jpg")
    game_name = "halligalli"
    
    results = img_model(image_path, game_name, "4")
    print(results)

