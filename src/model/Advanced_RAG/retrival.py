import asyncio
from query_translation import index_pdf, setup_query_generator
from langchain.load import dumps, loads
from langchain_community.callbacks.manager import get_openai_callback

# Retrieve

def reciprocal_rank_fusion(results: list[list], k=60):
    """ Reciprocal_rank_fusion that takes multiple lists of ranked documents 
        and an optional parameter k used in the RRF formula """
    
    # Initialize a dictionary to hold fused scores for each unique document
    fused_scores = {}

    # Iterate through each list of ranked documents
    for docs in results:
        # Iterate through each document in the list, with its rank (position in the list)
        for rank, doc in enumerate(docs):
            # Convert the document to a string format to use as a key (assumes documents can be serialized to JSON)
            doc_str = dumps(doc)
            # If the document is not yet in the fused_scores dictionary, add it with an initial score of 0
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            # Retrieve the current score of the document, if any
            previous_score = fused_scores[doc_str]
            # Update the score of the document using the RRF formula: 1 / (rank + k)
            fused_scores[doc_str] += 1 / (rank + k)

    # Sort the documents based on their fused scores in descending order to get the final reranked results
    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    # Return the reranked results as a list of tuples, each containing the document and its fused score
    return reranked_results


async def async_retrieve(query, retriever):
    return await retriever.ainvoke(query)


async def async_retrieval_chain_rag_fusion(question, generate_queries, file_path):
    retriever = index_pdf(file_path)
    queries = await generate_queries.ainvoke({"question": question})
    tasks = [async_retrieve(query, retriever) for query in queries]
    results = await asyncio.gather(*tasks)
    return reciprocal_rank_fusion(results)


### TEST ###------------------------------------------------------------------------------------

async def main():
    file_path = "/root/LLM_Bootcamp/pythonProject/data/Bang.pdf"
    generate_queries = setup_query_generator()
    question1 = "무법자들이 모두 죽으면 어떻게 돼?"
    question2 = "배신자가 게임에서 이기는 방법은?"

    with get_openai_callback() as cb:
        docs = await async_retrieval_chain_rag_fusion(question1, generate_queries, file_path)

        # 페이지 내용 출력
        for doc, score in docs:
            print(doc.page_content)
            print("---")

        print("\n\n\n")

        docs = await async_retrieval_chain_rag_fusion(question2, generate_queries, file_path)

        # 페이지 내용 출력
        for doc, score in docs:
            print(doc.page_content)
            print("-"*80)

        # 문서 총 개수 출력
        print(f"Total number of documents: {len(docs)}")

        # OpenAI 사용량 출력
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

if __name__ == "__main__":
    asyncio.run(main())
