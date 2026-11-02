from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Import our RAG agent function from agent.py
from backend.agent import ask_question

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Finnish Bureaucracy & Benefit Assistant API",
    version="1.0.0"
)

# Define the structure of incoming requests using Pydantic
class QuestionRequest(BaseModel):
    question: str

# Root route
@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Finnish Bureaucracy & Benefit Assistant API!"
    }

# Health check route
@app.get("/health")
def health_check():
    api_key_configured = bool(os.getenv("GOOGLE_API_KEY"))
    return {
        "status": "healthy",
        "gemini_api_key_configured": api_key_configured
    }

# The main RAG query endpoint
@app.post("/ask")
def ask_benefit_assistant(payload: QuestionRequest):
    try:
        if not payload.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
        # Run our agent
        result = ask_question(payload.question)
        return {
            "question": payload.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))