import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables (API key)
load_dotenv()

DB_PATH = "backend/chroma_db"
DATA_DIR = "data"

def ingest_data():
    print(f"Loading all guideline documents from '{DATA_DIR}/'...")
    
    # DirectoryLoader automatically grabs all .txt files in the data folder
    loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    print(f"Loaded {len(documents)} raw document files.")
    
    # Split the documents into smaller, manageable chunks for the vector store
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    
    print(f"Split into {len(docs)} text chunks. Generating embeddings...")
    
    # Initialize Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    # Create and persist the ChromaDB vector store
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    print(f"✅ Successfully ingested all files into ChromaDB at '{DB_PATH}'!")

if __name__ == "__main__":
    ingest_data()