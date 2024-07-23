import os
import logging
from typing import List, Any
import asyncio
from functools import lru_cache
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

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

async def contextualize_query(query: str, memory) -> str:
    """
    주어진 쿼리를 대화 기록에 기반하여 비동기적으로 컨텍스트화합니다.
    """
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
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        # Load context
        load_context_runnable = RunnablePassthrough().assign(
            chat_history=RunnableLambda(lambda x: memory.chat_memory.messages)
        )

        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            azure_model, retriever=None, prompt=contextualize_q_prompt
        )

        # Run context retrieval chain
        contextualize_chain = load_context_runnable | history_aware_retriever
        result = await asyncio.to_thread(contextualize_chain.invoke, {"input": query})

        return result["output"]
    except Exception as e:
        logger.error(f"Error contextualizing query: {str(e)}")
        raise

async def index_reply(faiss_index: FAISS, query: str, k: int, memory) -> List[Document]:
    """
    주어진 쿼리와 대화 기록에 대해 유사한 문서를 비동기적으로 검색합니다.
    """
    try:
        contextualized_query = await contextualize_query(query, memory)
        logger.info(f"Contextualized query: {contextualized_query}")
        return await asyncio.to_thread(faiss_index.similarity_search, contextualized_query, k=k)
    except Exception as e:
        logger.error(f"유사성 검색 중 오류 발생: {str(e)}")
        raise

def init_chain(faiss_index: FAISS) -> RetrievalQA:
    # 언어 모델 초기화
    llm = AzureChatOpenAI(
        azure_deployment=CONFIG["azure_deployment"],
        openai_api_version=CONFIG["openai_api_version"],
        temperature=0.7
    )

    # 리트리버 생성
    retriever = faiss_index.as_retriever(search_kwargs={"k": 4})

    # 프롬프트 템플릿 설정
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer: """
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )

    # RAG 체인 구성
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    return qa_chain

async def main():
    current_directory = os.getcwd()
    search_folder = os.path.join(current_directory, 'data')
    target_file_name = "Bang.pdf"
    query = "What happens if the sheriff kills the deputy?"

    try:
        # Memory initialization
        memory = ConversationBufferMemory(
            chat_memory=InMemoryChatMessageHistory(),
            return_messages=True
        )

        faiss_index = get_faiss_index(os.path.join(search_folder, target_file_name))
        docs = await index_reply(faiss_index, query, 4, memory)

        for i, doc in enumerate(docs, 1):
            print(f"\n--- Document {i} {'=' * 50}")
            print(doc.page_content)
        print("-" * 100)

        qa_chain = init_chain(faiss_index)

        # Save context
        def save_context(chain_output):
            memory.chat_memory.add_user_message(chain_output["input"])
            memory.chat_memory.add_ai_message(chain_output["answer"])
            return chain_output["answer"]

        # 체인을 사용하여 질문에 답변
        result = qa_chain({"query": query})
        print(result["result"])

        # Save the context after querying
        save_context(result)

    except Exception as e:
        logger.error(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
