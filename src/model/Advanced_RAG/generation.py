from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
from retrival import async_retrieval_chain_rag_fusion

load_dotenv()


prompt = PromptTemplate(
    template="""system You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise user
    Question: {question} 
    Context: {context} 
    Answer: assistant""",
    input_variables=["question", "document"],
)

azure_model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    openai_api_version = os.getenv("OPENAI_API_VERSION")
)

