from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

file_path = "PROJECT/ChatBoard/data/Bang.pdf"  

loader = PyPDFLoader(file_path)
pages = loader.load_and_split()

recursive_text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n",".",","],
    chunk_size=200,
    chunk_overlap=20,
    length_function=len,
)

# 개별 페이지를 쪼개서 하나의 리스트로 결합
all_splitted_documents = []
for page in pages:
    splitted_documents = recursive_text_splitter.split_documents([page])
    all_splitted_documents.extend(splitted_documents)

from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings

# Embedding
embedding_model = AzureOpenAIEmbeddings(
    model="text-embedding-3-large"
)

faiss_index = FAISS.from_documents(all_splitted_documents, embedding_model)

query = "What happens if the sheriff kills the deputy?"
docs = faiss_index.similarity_search(query, k=4)

for doc in docs:
    print("-" * 100)
    print(doc.page_content)
