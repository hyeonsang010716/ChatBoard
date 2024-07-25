from kor_to_eng import kor_to_eng
from search_rule import search_rule
from img_model import img_model
from load_pdf import get_faiss_index, index_reply
from langchain_openai import AzureChatOpenAI
import os
import asyncio

async def rag_to_llm(user_query: str, game_name: str) -> str:
    # 한국어 질문을 영어로 번역
    english_query = kor_to_eng(user_query)

    # 게임 룰북 파일 찾기
    rule_file_path = search_rule(game_name)
    if not rule_file_path:
        return "해당 게임의 룰북을 찾을 수 없습니다."

    # FAISS 인덱스 가져오기
    faiss_index = get_faiss_index(rule_file_path)

    # 관련 문서 검색
    relevant_docs = await index_reply(faiss_index, english_query, k=4)
    
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )

    # 프롬프트 구성 및 LLM 호출
    prompt = f"""
    질문: {user_query}
    관련 규칙:
    {' '.join([doc.page_content for doc in relevant_docs])}
    
    위의 정보를 바탕으로 질문에 대한 답변을 한국어로 작성해주세요. 
    규칙에 명시되지 않은 내용은 추측하지 말고, 알 수 없다고 답변해주세요.
    """

    response = llm.invoke(prompt)

    return response.content

async def main():
    user_query = "보안관이 부관을 죽이면 어떻게 돼?"
    game_name = "Bang"
    answer = await rag_to_llm(user_query, game_name)
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())