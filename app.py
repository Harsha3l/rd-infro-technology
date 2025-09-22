#!/usr/bin/env python3
"""
ECHOAL Backend API - Render Optimized Version
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

# In-memory storage (replace with database in production)
conversations = {}
messages = {}

# Pydantic models
class MessageRequest(BaseModel):
    content: str
    conversation_id: Optional[str] = None

class MessageResponse(BaseModel):
    message: Dict[str, Any]
    conversation_id: str

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str

class SettingsRequest(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    ai_model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    auto_save: Optional[bool] = None
    notifications: Optional[bool] = None

class SettingsResponse(BaseModel):
    theme: str
    language: str
    ai_model: str
    temperature: float
    max_tokens: int
    auto_save: bool
    notifications: bool

# Default settings
default_settings = {
    "theme": "light",
    "language": "en",
    "ai_model": "ECHOAL Assistant",
    "temperature": 0.7,
    "max_tokens": 500,
    "auto_save": True,
    "notifications": True
}

current_settings = default_settings.copy()

# Simple AI response function
def get_ai_response(message: str) -> str:
    """Generate a simple AI response"""
    responses = [
        f"I understand you said: '{message}'. How can I help you further?",
        f"That's interesting! You mentioned: '{message}'. Tell me more about it.",
        f"Thanks for sharing: '{message}'. What would you like to know?",
        f"I see you're asking about: '{message}'. Let me help you with that.",
        f"Great question about: '{message}'. Here's what I think..."
    ]
    import random
    return random.choice(responses)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "ECHOAL Backend API is running!",
        "status": "healthy",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "chat": "/api/chat/send",
            "conversations": "/api/conversations",
            "settings": "/api/settings"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "ECHOAL Backend is running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Chat endpoints
@app.post("/api/chat/send", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Create conversation if it doesn't exist
        if conversation_id not in conversations:
            conversations[conversation_id] = {
                "id": conversation_id,
                "title": request.content[:50] + "..." if len(request.content) > 50 else request.content,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            messages[conversation_id] = []
        
        # Generate AI response
        ai_response = get_ai_response(request.content)
        
        # Create user message
        user_message = {
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": request.content,
            "timestamp": datetime.now().isoformat()
        }
        
        # Create AI message
        ai_message = {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        }
        
        # Store messages
        messages[conversation_id].extend([user_message, ai_message])
        
        # Update conversation timestamp
        conversations[conversation_id]["updated_at"] = datetime.now().isoformat()
        
        return MessageResponse(
            message=ai_message,
            conversation_id=conversation_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/api/conversations", response_model=List[ConversationResponse])
async def get_conversations():
    try:
        conversation_list = []
        for conv in conversations.values():
            conversation_list.append(ConversationResponse(**conv))
        
        # Sort by updated_at descending
        conversation_list.sort(key=lambda x: x.updated_at, reverse=True)
        return conversation_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")

@app.get("/api/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: str):
    try:
        if conversation_id not in messages:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "conversation_id": conversation_id,
            "messages": messages[conversation_id]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    try:
        if conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        del conversations[conversation_id]
        del messages[conversation_id]
        
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

@app.put("/api/conversations/{conversation_id}/title")
async def update_conversation_title(conversation_id: str, title_data: dict):
    try:
        if conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversations[conversation_id]["title"] = title_data.get("title", "Untitled")
        conversations[conversation_id]["updated_at"] = datetime.now().isoformat()
        
        return {"message": "Title updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating title: {str(e)}")

# Settings endpoints
@app.get("/api/settings", response_model=SettingsResponse)
async def get_settings():
    return SettingsResponse(**current_settings)

@app.put("/api/settings", response_model=SettingsResponse)
async def update_settings(settings: SettingsRequest):
    try:
        # Update only provided settings
        for key, value in settings.dict(exclude_unset=True).items():
            if key in current_settings:
                current_settings[key] = value
        
        return SettingsResponse(**current_settings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating settings: {str(e)}")

@app.post("/api/settings/reset")
async def reset_settings():
    global current_settings
    current_settings = default_settings.copy()
    return {"message": "Settings reset to default"}

@app.get("/api/settings/themes")
async def get_themes():
    return {
        "themes": [
            {"id": "light", "name": "Light", "description": "Clean light theme"},
            {"id": "dark", "name": "Dark", "description": "Easy on the eyes dark theme"},
            {"id": "auto", "name": "Auto", "description": "Follow system preference"}
        ]
    }

@app.get("/api/settings/languages")
async def get_languages():
    return {
        "languages": [
            {"id": "en", "name": "English", "flag": "🇺🇸"},
            {"id": "es", "name": "Español", "flag": "🇪🇸"},
            {"id": "fr", "name": "Français", "flag": "🇫🇷"},
            {"id": "de", "name": "Deutsch", "flag": "🇩🇪"},
            {"id": "it", "name": "Italiano", "flag": "🇮🇹"},
            {"id": "pt", "name": "Português", "flag": "🇵🇹"},
            {"id": "ru", "name": "Русский", "flag": "🇷🇺"},
            {"id": "ja", "name": "日本語", "flag": "🇯🇵"},
            {"id": "ko", "name": "한국어", "flag": "🇰🇷"},
            {"id": "zh", "name": "中文", "flag": "🇨🇳"}
        ]
    }

@app.get("/api/settings/ai-models")
async def get_ai_models():
    return {
        "models": [
            {"id": "echoal", "name": "ECHOAL Assistant", "description": "Default AI assistant"},
            {"id": "gpt-3.5", "name": "GPT-3.5 Turbo", "description": "Fast and efficient"},
            {"id": "gpt-4", "name": "GPT-4", "description": "Most capable model"},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "description": "Latest GPT-4 model"}
        ]
    }

# Debug endpoint
@app.get("/debug/conversations")
async def debug_conversations():
    return {
        "conversations": conversations,
        "messages": messages,
        "total_conversations": len(conversations),
        "total_messages": sum(len(msgs) for msgs in messages.values())
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
