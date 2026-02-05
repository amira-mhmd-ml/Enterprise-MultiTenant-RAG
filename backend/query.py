import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_compressors import FlashrankRerank
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from qdrant_client import QdrantClient

# Load environment variables from .env file
load_dotenv()

def ask_enterprise_rag(query: str):
    # 1. Initialize LLM (Groq)
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    # 2. Initialize Embeddings model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 3. Connect to Qdrant Vector Database
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"), 
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
    # Fixed parameter: 'embedding' instead of 'embeddings'
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name="enterprise_docs",
        embedding=embeddings 
    )

    # 4. Setup Base Retriever (fetches top 10 candidates)
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    # 5. Setup Flashrank Reranker for better precision
    compressor = FlashrankRerank(model="ms-marco-MiniLM-L-12-v2")
    
    # 6. Create Contextual Compression Retriever
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )

    # --- Debugging Logs ---
    print(f"\n[INFO] Processing Query: {query}")
    
    # Retrieve and Rerank documents
    compressed_docs = compression_retriever.invoke(query)
    
    print(f"[INFO] Flashrank retrieved {len(compressed_docs)} relevant documents.")
    for i, doc in enumerate(compressed_docs):
        score = doc.metadata.get("re_score", 0.0)
        print(f"  Rank {i+1} | Score: {score:.4f} | Snippet: {doc.page_content[:60]}...")
    # --- End Debugging ---

    # 7. Construct the RAG Prompt
    context = "\n\n".join([doc.page_content for doc in compressed_docs])
    prompt = f"""
    You are an expert assistant. Use the provided context to answer the user's question accurately.
    If the context does not contain the answer, state that you do not know.
    
    Context:
    {context}
    
    Question: {query}
    Answer:"""

    # 8. Generate Final Response
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    # Internal Test Case
    test_query = "What information is available in the uploaded documents?"
    result = ask_enterprise_rag(test_query)
    print("\n[AI RESPONSE]:")
    print(result)