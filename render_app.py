#!/usr/bin/env python3
"""
ECHOAL Backend API - Render Optimized Version
Minimal working version for Render deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import os
import uuid
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="ECHOAL Backend API",
    description="Backend API for ECHOAL AI Assistant",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173", 
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:5173",
        "https://echoai-git-main-harsha-tri-lakshmis-projects.vercel.app",
        "https://echoai-5n2z.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class MessageRequest(BaseModel):
    content: str
    conversation_id: Optional[str] = None

class MessageResponse(BaseModel):
    id: str
    content: str
    timestamp: str
    role: str

class ChatResponse(BaseModel):
    conversation_id: str
    message: MessageResponse

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str

# In-memory storage (for development)
conversations = {}
messages = {}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "ECHOAL Backend API is running!",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "echoal-backend"
    }

# Chat endpoint
@app.post("/api/chat/send", response_model=ChatResponse)
async def send_message(request: MessageRequest):
    try:
        # Generate conversation ID if not provided
        if not request.conversation_id:
            conversation_id = str(uuid.uuid4())
        else:
            conversation_id = request.conversation_id
        
        # Create message
        message_id = str(uuid.uuid4())
        message = MessageResponse(
            id=message_id,
            content=f"Echo: {request.content}",
            timestamp=datetime.now().isoformat(),
            role="assistant"
        )
        
        # Store message
        if conversation_id not in messages:
            messages[conversation_id] = []
        messages[conversation_id].append(message.dict())
        
        # Store conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = {
                "id": conversation_id,
                "title": request.content[:50] + "..." if len(request.content) > 50 else request.content,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        else:
            conversations[conversation_id]["updated_at"] = datetime.now().isoformat()
        
        return ChatResponse(
            conversation_id=conversation_id,
            message=message
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

# Get conversations
@app.get("/api/conversations", response_model=List[ConversationResponse])
async def get_conversations():
    try:
        return list(conversations.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")

# Get messages for a conversation
@app.get("/api/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: str):
    try:
        if conversation_id not in messages:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return messages[conversation_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

# Delete conversation
@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    try:
        if conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        del conversations[conversation_id]
        if conversation_id in messages:
            del messages[conversation_id]
        
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

# Settings endpoints
@app.get("/api/settings")
async def get_settings():
    return {
        "temperature": 0.7,
        "max_tokens": 1000,
        "theme": "light",
        "language": "en",
        "ai_model": "gpt-3.5-turbo"
    }

@app.put("/api/settings")
async def update_settings(settings: dict):
    return {"message": "Settings updated successfully", "settings": settings}

@app.post("/api/settings/reset")
async def reset_settings():
    return {"message": "Settings reset to default"}

@app.get("/api/settings/themes")
async def get_themes():
    return ["light", "dark", "auto"]

@app.get("/api/settings/languages")
async def get_languages():
    return ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko"]

@app.get("/api/settings/ai-models")
async def get_ai_models():
    return ["gpt-3.5-turbo", "gpt-4", "claude-3-sonnet", "claude-3-opus"]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    uvicorn.run(
        "render_app:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
