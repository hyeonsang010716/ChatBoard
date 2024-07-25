import os
from functools import lru_cache
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.load import dumps, loads
from langchain_community.callbacks.manager import get_openai_callback

load_dotenv()

#### 인덱싱 ####

@lru_cache(maxsize=None)
def index_pdf(file_path):

    # PDF 파일 로드
    loader = PyPDFLoader(file_path)
    pdf_docs = loader.load()

    # 텍스트 분할
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=400, 
        chunk_overlap=50
    )

    # 분할 작업 수행
    splits = text_splitter.split_documents(pdf_docs)

    # 인덱싱
    embedding_model = AzureOpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embedding_model)

    return vectorstore.as_retriever()

### Prompt ###

def setup_query_generator():
    """
    하나의 질문에서 여러 쿼리 버전을 생성하는 함수를 설정하고 반환합니다.
    
    :return: 질문을 받아 여러 쿼리 버전을 반환하는 함수
    """
    template = """You are an AI language model assistant. Your task is to generate five 
    different versions of the given user question to retrieve relevant documents from a vector 
    database. The five different versions of the question must be written in English.
    The user will primarily ask about the rules of board games or card games. 
    By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions separated by newlines. Original question: {question}"""

    prompt_perspectives = ChatPromptTemplate.from_template(template)

    azure_model = AzureChatOpenAI(
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version = os.getenv("OPENAI_API_VERSION")
    )

    generate_queries = (
        prompt_perspectives 
        | azure_model 
        | StrOutputParser() 
        | (lambda x: x.split("\n"))
    )

    return generate_queries

