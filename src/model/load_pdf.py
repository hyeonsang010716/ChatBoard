import os
import logging
from typing import List
import asyncio
from functools import lru_cache
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever


# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 환경 변수 로드
load_dotenv()

# 설정
CONFIG = {
    "chunk_size": 200,
    "chunk_overlap": 20,
    "embedding_model": "text-embedding-3-large",
    "separators": ["\n\n", ".", ","],
}

@lru_cache(maxsize=None)
def get_faiss_index(file_path: str) -> FAISS:
    """
    PDF 파일을 로드하고 인덱싱하여 FAISS 인덱스를 반환합니다.
    이 함수는 동일한 파일을 재처리하지 않도록 캐싱됩니다.
    """
    try:
        logger.info(f"파일 인덱싱 중: {file_path}")
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        text_splitter = RecursiveCharacterTextSplitter(
            separators=CONFIG["separators"],
            chunk_size=CONFIG["chunk_size"],
            chunk_overlap=CONFIG["chunk_overlap"],
            length_function=len,
        )

        all_split_docs = []
        for page in pages:
            split_docs = text_splitter.split_documents([page])
            all_split_docs.extend(split_docs)

        embedding_model = AzureOpenAIEmbeddings(model=CONFIG["embedding_model"])
        return FAISS.from_documents(all_split_docs, embedding_model)
    except Exception as e:
        logger.error(f"파일 인덱싱 중 오류 발생 {file_path}: {str(e)}")
        raise

def contextualize_query(query, retriever):
# Azure OpenAI 모델 초기화
    azure_model = AzureChatOpenAI(
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version = os.getenv("OPENAI_API_VERSION")
    )

    # 히스토리 기반 리트리버 생성
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
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        azure_model, retriever, contextualize_q_prompt
    )    


async def index_reply(faiss_index: FAISS, query: str, k: int) -> List[Document]:
    """
    주어진 쿼리에 대해 유사한 문서를 비동기적으로 검색합니다.
    """
    try:
        return await asyncio.to_thread(faiss_index.similarity_search, query, k=k)
    except Exception as e:
        logger.error(f"유사성 검색 중 오류 발생: {str(e)}")
        raise

async def main():
    file_path = "pythonProject/ChatBoard/data/Bang.pdf"
    query = "What happens if the sheriff kills the deputy?"

    try:
        faiss_index = get_faiss_index(file_path)
        docs = await index_reply(faiss_index, query, 4)

        for i, doc in enumerate(docs, 1):
            print(f"\n--- Document {i} {'=' * 50}")
            print(doc.page_content)

    except Exception as e:
        logger.error(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())

