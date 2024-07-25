import os
import asyncio
from dotenv import load_dotenv
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from indexing import get_faiss_index

# Load environment variables
load_dotenv()

CONFIG = {
    "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    "openai_api_version": os.getenv("OPENAI_API_VERSION")
}

def init_chain(faiss_index, game_name):
    llm = AzureChatOpenAI(
        azure_deployment=CONFIG["azure_deployment"],
        openai_api_version=CONFIG["openai_api_version"],
        temperature=0.7
    )

    retriever = faiss_index.as_retriever(search_kwargs={"k": 2})

    prompt = PromptTemplate(
        input_variables=["game_name", "image_path", "query", "context"],
        template="""You are an expert board game analyst. Analyze the following:
            Game: {game_name}

            Image Path: {image_path}

            User Query: {query}

            Relevant Game Rules and Context:
            {context}

            Based on the image path, user query, and provided context, please provide a detailed analysis of the game situation. 
            Focus on answering the user's query while considering both the visual information from the image path and the textual information from the game rules.

            Analysis:"""
    )

    chain = RunnableSequence(prompt | llm)
    return chain, retriever

async def process_image_and_index(file_path, img_file_path, game_name):
    index_task = asyncio.create_task(asyncio.to_thread(get_faiss_index, file_path))
    # 이미지 파일 경로를 반환합니다.
    image_desc = img_file_path
    
    faiss_index = await index_task
    return faiss_index, image_desc

async def reply(text: str, target_file_name: str, img_file_path: str) -> str:
    current_directory = os.getcwd()
    search_folder = os.path.join(current_directory, 'data')
    file_path = os.path.join(search_folder, target_file_name)
    game_name = target_file_name.rsplit('.', 1)[0]
    
    faiss_index, image_desc = await process_image_and_index(file_path, img_file_path, game_name)
    
    chain, retriever = init_chain(faiss_index, game_name)
    
    # Use retriever invoke method instead of get_relevant_documents
    docs = await retriever.ainvoke(text)
    context = "\n".join([doc.page_content for doc in docs])
    
    input_data = {
        "game_name": game_name,
        "image_path": image_desc,  # 이미지 파일 경로를 입력합니다.
        "query": text,
        "context": context
    }

    response = await chain.ainvoke(input_data)
    
    # 메타데이터 제거
    if isinstance(response, dict) and 'text' in response:
        response_text = response['text']
    else:
        response_text = response
    
    return response_text

def main():
    target_file_name = "halligalli.pdf"
    current_directory = os.getcwd()
    search_folder = os.path.join(current_directory, 'data', 'photo')
    img_file_path = os.path.join(search_folder, "boardgame_ex.png")

    print("Welcome! Ask me anything about the content of the document.")
    print("Type 'exit' to end the conversation.")

    while True:
        user_input = input("\nYour question: ")
        
        if user_input.lower() == 'exit':
            print("Thank you for using the QA system. Goodbye!")
            break

        answer = asyncio.run(reply(user_input, target_file_name, img_file_path))
        
        print("\nAnswer:", answer)

if __name__ == "__main__":
    main()
