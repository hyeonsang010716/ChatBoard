import os
import asyncio
from dotenv import load_dotenv
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from indexing import get_faiss_index
from img_model import img_model

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

    prompt = PromptTemplate(
        input_variables=["game_name", "image_desc", "query", "context"],
        template="""You are an expert board game analyst. Analyze the following:
            Game: {game_name}

            Image Description: {image_desc}

            User Query: {query}

            Relevant Game Rules and Context:
            {context}

            Based on the image description, user query, and provided context, please provide a detailed analysis of the game situation. 
            Focus on answering the user's query while considering both the visual information from the image description and the textual information from the game rules.
            
            Please provide your response in Korean.

            Keep your response concise and to the point. Include only the most critical information and your conclusion.

            Analysis:"""
    )
    
    retriever = faiss_index.as_retriever(search_kwargs={"k": 4})

    chain = RunnableSequence(prompt | llm)
    return chain, retriever

async def process_image_and_index(file_path, img_file_path, game_name):
    index_task = asyncio.create_task(asyncio.to_thread(get_faiss_index, file_path))
    image_task = asyncio.create_task(asyncio.to_thread(img_model, img_file_path, game_name))
    
    faiss_index, image_desc = await asyncio.gather(index_task, image_task)
    return faiss_index, image_desc

async def reply(text: str, target_file_name: str, img_file_path: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    p = os.path.abspath(os.path.join(current_dir , '..' , '..'))
    search_folder = os.path.join(p, 'data')
    file_path = os.path.join(search_folder, target_file_name)
    
    game_name = target_file_name.rsplit('.', 1)[0]
    
    faiss_index, image_desc = await process_image_and_index(file_path, img_file_path, game_name)
    
    chain, retriever = init_chain(faiss_index, game_name)
    
    docs = await retriever.ainvoke(text)
    context = "\n".join([doc.page_content for doc in docs])
    
    input_data = {
        "game_name": game_name,
        "image_desc": image_desc,
        "query": text,
        "context": context
    }

    response = await chain.ainvoke(input_data)
    
    # 메타데이터 제거
    if isinstance(response, AIMessage):
        response_text = response.content
    else:
        response_text = response
    
    return response_text

# test ------------------------------------------------

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

# import os
# import asyncio
# from dotenv import load_dotenv
# from langchain.schema import HumanMessage, AIMessage, SystemMessage
# from langchain_openai import AzureChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain_core.runnables import RunnableSequence
# from indexing import get_faiss_index
# from img_model import img_model

# # Load environment variables
# load_dotenv()

# CONFIG = {
#     "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
#     "openai_api_version": os.getenv("OPENAI_API_VERSION")
# }

# def init_chain(faiss_index, game_name, input_data):
#     llm = AzureChatOpenAI(
#         azure_deployment=CONFIG["azure_deployment"],
#         openai_api_version=CONFIG["openai_api_version"],
#         temperature=0.7
#     )

#     retriever = faiss_index.as_retriever(search_kwargs={"k": 2})

#     prompt = PromptTemplate(
#         input_variables=["game_name", "image_desc", "query", "context"],
#         template="""You are an expert board game analyst. Analyze the following:
#             Game: {game_name}

#             Image Description: {image_desc}

#             User Query: {query}

#             Relevant Game Rules and Context:
#             {context}

#             Based on the image description, user query, and provided context, please provide a detailed analysis of the game situation. 
#             Focus on answering the user's query while considering both the visual information from the image description and the textual information from the game rules.
            
#             Please provide your response in Korean.

#             Keep your response concise and to the point. Include only the most critical information and your conclusion.

#             Analysis:"""
#     )

#     # 체인 설정
#     def create_prompt_with_context(docs):
#         context = "\n".join([doc.page_content for doc in docs])
#         return prompt.format_prompt(
#             game_name=input_data["game_name"],
#             image_desc=input_data["image_desc"],
#             query=input_data["query"],
#             context=context
#         )

#     chain = RunnableSequence(retriever | create_prompt_with_context | llm)
    
#     return chain

# async def process_image_and_index(file_path, img_file_path, game_name):
#     index_task = asyncio.create_task(asyncio.to_thread(get_faiss_index, file_path))
#     image_task = asyncio.create_task(asyncio.to_thread(img_model, img_file_path, game_name))
    
#     faiss_index, image_desc = await asyncio.gather(index_task, image_task)
#     return faiss_index, image_desc

# async def reply(text: str, target_file_name: str, img_file_path: str) -> str:
#     current_directory = os.getcwd()
#     search_folder = os.path.join(current_directory, 'data')
#     file_path = os.path.join(search_folder, target_file_name)
#     game_name = target_file_name.rsplit('.', 1)[0]
    
#     faiss_index, image_desc = await process_image_and_index(file_path, img_file_path, game_name)
    
#     # input_data 생성
#     input_data = {
#         "game_name": game_name,
#         "image_desc": image_desc,
#         "query": text,
#         "context": ""  # 초기화
#     }
    
#     chain = init_chain(faiss_index, game_name, input_data)

#     # 체인 실행 및 결과 얻기
#     response = await chain.ainvoke(input_data)
    
#     # 메타데이터 제거
#     if isinstance(response, AIMessage):
#         response_text = response.content
#     else:
#         response_text = response
    
#     return response_text

# def main():
#     target_file_name = "halligalli.pdf"
#     current_directory = os.getcwd()
#     search_folder = os.path.join(current_directory, 'data', 'photo')
#     img_file_path = os.path.join(search_folder, "boardgame_ex.png")

#     print("Welcome! Ask me anything about the content of the document.")
#     print("Type 'exit' to end the conversation.")

#     while True:
#         user_input = input("\nYour question: ")
        
#         if user_input.lower() == 'exit':
#             print("Thank you for using the QA system. Goodbye!")
#             break

#         answer = asyncio.run(reply(user_input, target_file_name, img_file_path))
        
#         print("\nAnswer:", answer)

# if __name__ == "__main__":
#     main()
