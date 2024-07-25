from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
from retrieval import async_retrieval_chain_rag_fusion

async def generate_reply(query, file_path):
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
            ("human", "Question: {question}"),
            ("human", "Context: {context}"),
            ("assistant", "Answer:")
        ]
    )

    docs = await async_retrieval_chain_rag_fusion(query, file_path)
    
    # Prepare the context by joining the content of retrieved documents
    context = "\n".join([doc.page_content for doc, _ in docs[:3]])  # Using top 3 documents

    question_answer_chain = prompt | azure_model

    # Generate the response
    response = await question_answer_chain.ainvoke({
        "question": query,
        "context": context
    })

    return response.content

# Example usage
async def main():
    file_path = "/root/LLM_Bootcamp/pythonProject/data/Bang.pdf"
    question = "무법자들이 모두 죽으면 어떻게 돼?"
    
    answer = await generate_reply(question, file_path)
    print(f"Question: {question}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())