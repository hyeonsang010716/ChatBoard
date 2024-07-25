from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
from .img_model import img_model
from .retrieval import async_retrieval_chain_rag_fusion
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage

def find_file_path(game_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(current_dir , '..' , '..', '..'))
    search_folder = os.path.join(file_path, 'data')
    game_file_path = os.path.join(search_folder, game_name)
    return game_file_path

class Conversation:
    def __init__(self):
        self.memory = ConversationBufferMemory(return_messages=True)

    async def generate_reply(self, query, game_name_file, image_path: str, player_num: str):
        file_path = find_file_path(game_name_file)
        game_name = game_name_file.rsplit('.', 1)[0]

        load_dotenv()

        azure_model = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            openai_api_version=os.getenv("OPENAI_API_VERSION")
        )

        system_prompt_str = f"""
        You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Use five sentences maximum and keep the answer concise.
        Please provide your response in Korean.
        If an image description is provided, include the image description in your answer to the question.
        Briefly explain the reasoning behind your answer.
        A situation like the one in the photo has occurred during a board game. Please explain the situation that has unfolded in the board game {game_name}. The number of players is {player_num}. Please refer to the number of players if necessary.
        
        Board game rules: {{context}}
        """.strip()
        
        # 이미지 파일이 있는 경우에만 이미지 분석 실행
        base64_image = []
        if image_path != "":
            base64_image = [{
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_model(image_path, game_name, player_num)}"
                }
            }]

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt_str),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessage(content=[
                    *base64_image,
                    {
                        "type": "text",
                        "text": f"Question: {query}"
                    },
                ]),
                ("assistant", "Answer:")
            ]
        )

        docs = await async_retrieval_chain_rag_fusion(query, file_path)
        
        # 검색된 문서의 내용을 결합하여 컨텍스트 준비
        context = "\n".join([doc.page_content for doc, _ in docs[:4]])  # 상위 4개의 문서를 사용

        question_answer_chain = prompt | azure_model

        # 응답 생성
        response = await question_answer_chain.ainvoke({
            "chat_history": self.memory.chat_memory.messages,
            "query": query,
            "context": context
        })

        # 새 상호작용을 메모리에 추가
        self.memory.chat_memory.add_user_message(query)
        self.memory.chat_memory.add_ai_message(response.content)

        return response.content

# 사용 예시
async def main():
    current_directory = os.getcwd()
    search_folder = os.path.join(current_directory, 'data', 'photo')
    img_file_path = os.path.join(search_folder, "boardgame_ex.png")
    game_name = "halligalli.pdf"
    player_num = "3"
    
    conversation = Conversation()
    
    questions = [
        "사진에서 라임이 총 몇개야?",
        "할리갈리 게임의 목표는 무엇인가요?",
        "이전 질문에서 언급된 과일의 이름이 뭐였지?"
    ]
    
    for question in questions:
        answer = await conversation.generate_reply(question, game_name, img_file_path, player_num)
        print(f"Question: {question}")
        print(f"Answer: {answer}")
        # print("-" * 50)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
