import os
import logging
import asyncio
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores import FAISS
from indexing import get_faiss_index
from query_processing import index_reply

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 환경 변수 로드
load_dotenv()

CONFIG = {
    "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    "openai_api_version": os.getenv("OPENAI_API_VERSION")
}

def init_chain(faiss_index: FAISS) -> RetrievalQA:
    # 1. 언어 모델 초기화
    llm = AzureChatOpenAI(
        azure_deployment=CONFIG["azure_deployment"],
        openai_api_version=CONFIG["openai_api_version"],
        temperature=0.7  # 필요에 따라 조정
    )

    # 2. 벡터 스토어로부터 리트리버 생성
    retriever = faiss_index.as_retriever(search_kwargs={"k": 4})

    # 3. 답변 생성을 위한 프롬프트 템플릿 설정
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer: """
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )

    # 4. RAG 체인 구성
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

    # 대화 내용을 저장할 메모리 초기화
    memory = ConversationBufferMemory(
        chat_memory=InMemoryChatMessageHistory(),        
        return_messages=True
    )

    try:
        faiss_index = get_faiss_index(os.path.join(search_folder, target_file_name))
        docs = await index_reply(faiss_index, query, 4, memory)

        for i, doc in enumerate(docs, 1):
            print(f"\n--- Document {i} {'=' * 50}")
            print(doc.page_content)
        print("-"*100)

        qa_chain = init_chain(faiss_index)
        # 체인을 사용하여 질문에 답변
        query = "What happens if the sheriff kills the deputy?"
        result = qa_chain({"query": query})
        print(result["result"])

    except Exception as e:
        logger.error(f"오류 발생: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
