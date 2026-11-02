import os
import time
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Load our API key from .env
load_dotenv()

DB_PATH = "backend/chroma_db"

def get_qa_chain():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    # Switched to the faster, high-throughput flash-lite model
    llm = ChatGoogleGenerativeAI(model="models/gemini-3.5-flash-lite", temperature=0.2)
    
    system_prompt = (
        "You are an expert assistant for Finnish public benefits (Kela and Vero). "
        "Use the following pieces of retrieved context to answer "
        "the user's question accurately. If you don't know the answer, say that you "
        "don't know.\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return retrieval_chain

def ask_question(question: str, max_retries: int = 2):
    chain = get_qa_chain()
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Querying Gemini Flash-Lite (Attempt {attempt}/{max_retries})...")
            response = chain.invoke({"input": question})
            return {
                "answer": response["answer"],
                "sources": [doc.page_content for doc in response.get("context", [])]
            }
        except Exception as e:
            print(f"⚠️ Encountered error: {e}")
            if attempt < max_retries:
                print(f"Retrying...")
                time.sleep(1)
            else:
                raise e

if __name__ == "__main__":
    test_query = "What are the student earnings rules for housing allowance?"
    print(f"\n--- Testing Agent with Query: '{test_query}' ---\n")
    
    result = ask_question(test_query)
    
    print("\n🤖 AI Answer:")
    print(result["answer"])
    print("\n📚 Source Documents Referenced:")
    for i, source in enumerate(result["sources"], 1):
        print(f"[Source {i}]: {source}\n")