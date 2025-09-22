from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Default settings
default_settings = {
    "ai_model": "ECHOAL Assistant",
    "theme": "light",
    "language": "en",
    "max_tokens": 500,
    "temperature": 0.7,
    "auto_save": True,
    "notifications": True,
    "version": "1.0.0",
    "features": ["chat", "conversations", "settings", "themes", "languages"]
}

# Current settings (in production, this would be in database)
current_settings = default_settings.copy()

# Pydantic models
class MessageRequest(BaseModel):
    content: str
    conversation_id: Optional[str] = None

class MessageResponse(BaseModel):
    id: str
    content: str
    role: str
    timestamp: datetime
    conversation_id: str

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int

class NewConversationResponse(BaseModel):
    conversation_id: str
    message: MessageResponse

class SettingsRequest(BaseModel):
    ai_model: Optional[str] = None
    theme: Optional[str] = None
    language: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    auto_save: Optional[bool] = None
    notifications: Optional[bool] = None

class SettingsResponse(BaseModel):
    ai_model: str
    theme: str
    language: str
    max_tokens: int
    temperature: float
    auto_save: bool
    notifications: bool
    version: str
    features: List[str]

# AI Response Generator (placeholder - integrate with your preferred AI service)
class AIResponseGenerator:
    def __init__(self):
        self.responses = [
            "I understand you're asking about {topic}. Let me help you with that.",
            "That's an interesting question! Here's what I think about {topic}...",
            "I'd be happy to assist you with {topic}. Let me provide some insights.",
            "Great question! Regarding {topic}, here's my perspective...",
            "I can definitely help you explore {topic}. Let me share some thoughts on this."
        ]
    
    def generate_response(self, user_message: str) -> str:
        # Simple keyword extraction for demo
        keywords = user_message.lower().split()[:3]
        topic = " ".join(keywords)
        
        # In production, replace this with actual AI API call
        import random
        response_template = random.choice(self.responses)
        return response_template.format(topic=topic)

ai_generator = AIResponseGenerator()

# API Endpoints
@app.get("/")
async def root():
    return {"message": "ECHOAL Backend API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/debug/conversations")
async def debug_conversations():
    """Debug endpoint to see all conversations and messages"""
    return {
        "conversations": conversations,
        "messages": messages,
        "conversation_count": len(conversations),
        "message_count": sum(len(msgs) for msgs in messages.values())
    }

@app.post("/api/chat/send", response_model=NewConversationResponse)
async def send_message(request: MessageRequest):
    try:
        print(f"Received message: {request.content}")
        print(f"Conversation ID: {request.conversation_id}")
        print(f"Current conversations: {list(conversations.keys())}")
        
        # Generate or get conversation ID
        if request.conversation_id and request.conversation_id in conversations:
            conversation_id = request.conversation_id
            print(f"Using existing conversation: {conversation_id}")
        else:
            conversation_id = str(uuid.uuid4())
            print(f"Creating new conversation: {conversation_id}")
            conversations[conversation_id] = {
                "id": conversation_id,
                "title": request.content[:50] + "..." if len(request.content) > 50 else request.content,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "message_count": 0
            }
        
        # Create user message
        user_message_id = str(uuid.uuid4())
        user_message = {
            "id": user_message_id,
            "content": request.content,
            "role": "user",
            "timestamp": datetime.now(),
            "conversation_id": conversation_id
        }
        
        # Store user message
        if conversation_id not in messages:
            messages[conversation_id] = []
        messages[conversation_id].append(user_message)
        
        # Generate AI response
        ai_response_content = ai_generator.generate_response(request.content)
        ai_message_id = str(uuid.uuid4())
        ai_message = {
            "id": ai_message_id,
            "content": ai_response_content,
            "role": "assistant",
            "timestamp": datetime.now(),
            "conversation_id": conversation_id
        }
        
        # Store AI message
        messages[conversation_id].append(ai_message)
        
        # Update conversation
        conversations[conversation_id]["updated_at"] = datetime.now()
        conversations[conversation_id]["message_count"] = len(messages[conversation_id])
        
        return NewConversationResponse(
            conversation_id=conversation_id,
            message=MessageResponse(**ai_message)
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

@app.get("/api/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: str):
    try:
        # Debug information
        print(f"Looking for conversation_id: {conversation_id}")
        print(f"Available conversations: {list(conversations.keys())}")
        print(f"Available messages: {list(messages.keys())}")
        
        if conversation_id not in messages:
            raise HTTPException(
                status_code=404, 
                detail=f"Conversation not found. Available conversations: {list(conversations.keys())}"
            )
        
        message_list = []
        for msg in messages[conversation_id]:
            message_list.append(MessageResponse(**msg))
        
        # Sort by timestamp
        message_list.sort(key=lambda x: x.timestamp)
        return message_list
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
        if conversation_id in messages:
            del messages[conversation_id]
        
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

@app.put("/api/conversations/{conversation_id}/title")
async def update_conversation_title(conversation_id: str, title: str):
    try:
        if conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversations[conversation_id]["title"] = title
        conversations[conversation_id]["updated_at"] = datetime.now()
        
        return {"message": "Title updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating title: {str(e)}")

# Settings endpoints
@app.get("/api/settings", response_model=SettingsResponse)
async def get_settings():
    """Get current application settings"""
    try:
        return SettingsResponse(**current_settings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching settings: {str(e)}")

@app.put("/api/settings")
async def update_settings(settings_request: SettingsRequest):
    """Update application settings"""
    try:
        # Update only provided settings
        updated_fields = []
        for field, value in settings_request.dict(exclude_unset=True).items():
            if value is not None:
                current_settings[field] = value
                updated_fields.append(field)
        
        # Validate settings
        if "temperature" in updated_fields:
            if not 0.0 <= current_settings["temperature"] <= 2.0:
                raise HTTPException(status_code=400, detail="Temperature must be between 0.0 and 2.0")
        
        if "max_tokens" in updated_fields:
            if not 1 <= current_settings["max_tokens"] <= 4000:
                raise HTTPException(status_code=400, detail="Max tokens must be between 1 and 4000")
        
        if "theme" in updated_fields:
            if current_settings["theme"] not in ["light", "dark", "auto"]:
                raise HTTPException(status_code=400, detail="Theme must be 'light', 'dark', or 'auto'")
        
        if "language" in updated_fields:
            if current_settings["language"] not in ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko"]:
                raise HTTPException(status_code=400, detail="Unsupported language")
        
        return {
            "message": "Settings updated successfully",
            "updated_fields": updated_fields,
            "settings": SettingsResponse(**current_settings)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating settings: {str(e)}")

@app.post("/api/settings/reset")
async def reset_settings():
    """Reset settings to default values"""
    try:
        global current_settings
        current_settings = default_settings.copy()
        return {
            "message": "Settings reset to default successfully",
            "settings": SettingsResponse(**current_settings)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting settings: {str(e)}")

@app.get("/api/settings/themes")
async def get_available_themes():
    """Get list of available themes"""
    return {
        "themes": [
            {"id": "light", "name": "Light", "description": "Clean light theme"},
            {"id": "dark", "name": "Dark", "description": "Elegant dark theme"},
            {"id": "auto", "name": "Auto", "description": "Follow system preference"}
        ]
    }

@app.get("/api/settings/languages")
async def get_available_languages():
    """Get list of available languages"""
    return {
        "languages": [
            {"code": "en", "name": "English", "native": "English"},
            {"code": "es", "name": "Spanish", "native": "Español"},
            {"code": "fr", "name": "French", "native": "Français"},
            {"code": "de", "name": "German", "native": "Deutsch"},
            {"code": "it", "name": "Italian", "native": "Italiano"},
            {"code": "pt", "name": "Portuguese", "native": "Português"},
            {"code": "ru", "name": "Russian", "native": "Русский"},
            {"code": "zh", "name": "Chinese", "native": "中文"},
            {"code": "ja", "name": "Japanese", "native": "日本語"},
            {"code": "ko", "name": "Korean", "native": "한국어"}
        ]
    }

@app.get("/api/settings/ai-models")
async def get_available_ai_models():
    """Get list of available AI models"""
    return {
        "models": [
            {"id": "ECHOAL Assistant", "name": "ECHOAL Assistant", "description": "Default ECHOAL model"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and efficient"},
            {"id": "gpt-4", "name": "GPT-4", "description": "Most capable model"},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "description": "Latest GPT-4 model"}
        ]
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0" if os.environ.get("RENDER") else "127.0.0.1"
    
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=False,  # Disable reload for stability
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
