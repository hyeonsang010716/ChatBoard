import os
import logging
from functools import lru_cache
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 환경 변수 로드
load_dotenv()

CONFIG = {
    "chunk_size": 400,
    "chunk_overlap": 20,
    "embedding_model": "text-embedding-3-large",
    "separators": ["\n\n", ".", ","],
    "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    "openai_api_version": os.getenv("OPENAI_API_VERSION")
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
