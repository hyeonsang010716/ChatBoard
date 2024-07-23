import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from .indexing import get_faiss_index

# Load environment variables
load_dotenv()

CONFIG = {
    "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    "openai_api_version": os.getenv("OPENAI_API_VERSION")
}

def init_chain(faiss_index):
    # Initialize language model
    llm = AzureChatOpenAI(
        azure_deployment=CONFIG["azure_deployment"],
        openai_api_version=CONFIG["openai_api_version"],
        temperature=0.7
    )

    # Create retriever from vector store
    retriever = faiss_index.as_retriever(search_kwargs={"k": 4})

    # Set up prompt template for answer generation
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer: """
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )

    # Configure RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    return qa_chain

def reply(text: str, target_file_name: str) -> str:
    current_directory = os.getcwd()
    search_folder = os.path.join(current_directory, 'data')
    file_path = os.path.join(search_folder, target_file_name)

    # Initialize FAISS index
    faiss_index = get_faiss_index(file_path)
    
    # Initialize QA chain
    qa_chain = init_chain(faiss_index)

    # Get answer from QA chain
    result = qa_chain.invoke({"query": text})
    
    # Return the answer
    return result["result"]

def main():
    target_file_name = "Bang.pdf"

    print("Welcome! Ask me anything about the content of the document.")
    print("Type 'exit' to end the conversation.")

    while True:
        # Get user input
        user_input = input("\nYour question: ")
        
        # Check if user wants to exit
        if user_input.lower() == 'exit':
            print("Thank you for using the QA system. Goodbye!")
            break

        # Get answer using reply function
        answer = reply(user_input, target_file_name)
        
        # Print the answer
        print("\nAnswer:", answer)

if __name__ == "__main__":
    main()