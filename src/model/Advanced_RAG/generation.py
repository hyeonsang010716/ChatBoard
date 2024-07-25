from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
from img_model import img_model
from retrieval import async_retrieval_chain_rag_fusion

def find_file_path(game_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(current_dir , '..' , '..', '..'))
    search_folder = os.path.join(file_path, 'data')
    game_file_path = os.path.join(search_folder, game_name)
    return game_file_path

async def generate_reply(query, game_name_file, image_path: str):
    file_path = find_file_path(game_name_file)
    game_name = game_name_file.rsplit('.', 1)[0]

    load_dotenv()

    azure_model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )

    system_prompt_str = """
    You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.
    Answer the question in Korean.""".strip()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt_str),
            ("human", "Image: {image_desc}"),
            ("human", "Question: {question}"),
            ("human", "Context: {context}"),
            ("assistant", "Answer:")
        ]
    )

    docs = await async_retrieval_chain_rag_fusion(query, file_path)
    
    # Run image analysis only if you have an image file
    if image_path != "":
        image_desc = img_model(image_path, game_name)
    else: image_desc = "No image information"
    
    # Prepare the context by joining the content of retrieved documents
    context = "\n".join([doc.page_content for doc, _ in docs[:3]])  # Using top 3 documents

    question_answer_chain = prompt | azure_model

    # Generate the response
    response = await question_answer_chain.ainvoke({
        "image_desc": image_desc,
        "question": query,
        "context": context
    })

    return response.content

# Example usage
async def main():
    game_name = "Bang.pdf"
    question = "무법자들이 모두 죽으면 어떻게 돼?"
    
    answer = await generate_reply(question, game_name)
    print(f"Question: {question}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())