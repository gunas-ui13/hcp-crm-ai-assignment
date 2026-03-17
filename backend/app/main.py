from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from . import models
from .database import engine
from .agent import process_chat

# Create the database tables automatically
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(title="HCP CRM AI Backend")

# Allow the React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-First HCP CRM API!"}

# --- AI CHAT ENDPOINT ---

# Define the format of the incoming chat request
class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
def chat_with_agent(request: ChatRequest):
    try:
        # result must be the dictionary from process_chat
        result = process_chat(request.message)
        return {"response": result}
    except Exception as e:
        print(f"Server Error: {e}")
        return {"error": str(e)}