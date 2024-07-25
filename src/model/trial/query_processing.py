import os
import logging
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableMap

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG = {
    "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    "openai_api_version": os.getenv("OPENAI_API_VERSION")
}

async def contextualize_query(query: str, memory) -> str:
    try:
        azure_model = AzureChatOpenAI(
            azure_deployment=CONFIG["azure_deployment"],
            openai_api_version=CONFIG["openai_api_version"]
        )

        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ]
        )

        # 메모리에서 채팅 기록 추출
        chat_history = memory.chat_memory.messages

        # 체인 실행
        chain = contextualize_q_prompt | azure_model
        result = await chain.ainvoke({"chat_history": chat_history, "input": query})
        return result.content.strip()

    except Exception as e:
        logger.error(f"쿼리 컨텍스트화 중 오류 발생: {str(e)}")
        raise

async def index_reply(faiss_index: FAISS, query: str, k: int, memory) -> List[Document]:
    """
    주어진 쿼리와 대화 기록에 대해 유사한 문서를 비동기적으로 검색합니다.
    """
    try:
        contextualized_query = await contextualize_query(query, memory)
        logger.info(f"컨텍스트화된 쿼리: {contextualized_query}")
        return faiss_index.similarity_search(contextualized_query, k=k)
    except Exception as e:
        logger.error(f"유사성 검색 중 오류 발생: {str(e)}")
        raise