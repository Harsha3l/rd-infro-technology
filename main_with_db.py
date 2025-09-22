from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
import uvicorn
from sqlalchemy.orm import Session

from database import get_db, create_tables
from models import Conversation, Message, UserSettings
from ai_service import get_ai_service
from config import settings

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

# Initialize AI service
ai_service = get_ai_service()

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

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int

    class Config:
        from_attributes = True

class NewConversationResponse(BaseModel):
    conversation_id: str
    message: MessageResponse

class SettingsResponse(BaseModel):
    ai_model: str
    version: str
    features: List[str]

# API Endpoints
@app.get("/")
async def root():
    return {"message": "ECHOAL Backend API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/chat/send", response_model=NewConversationResponse)
async def send_message(request: MessageRequest, db: Session = Depends(get_db)):
    try:
        # Get or create conversation
        if request.conversation_id:
            conversation = db.query(Conversation).filter(Conversation.id == request.conversation_id).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(
                title=ai_service.generate_conversation_title(request.content),
                message_count=0
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Create user message
        user_message = Message(
            content=request.content,
            role="user",
            conversation_id=conversation.id
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # Get conversation history for context
        conversation_history = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.timestamp).all()
        
        # Convert to dict format for AI service
        history_dicts = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation_history
        ]
        
        # Generate AI response
        ai_response_content = ai_service.generate_response(request.content, history_dicts)
        
        # Create AI message
        ai_message = Message(
            content=ai_response_content,
            role="assistant",
            conversation_id=conversation.id
        )
        db.add(ai_message)
        
        # Update conversation
        conversation.updated_at = datetime.utcnow()
        conversation.message_count = len(conversation_history) + 2  # +2 for user and AI messages
        
        db.commit()
        db.refresh(ai_message)
        
        return NewConversationResponse(
            conversation_id=conversation.id,
            message=MessageResponse.from_orm(ai_message)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/api/conversations", response_model=List[ConversationResponse])
async def get_conversations(db: Session = Depends(get_db)):
    try:
        conversations = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
        return [ConversationResponse.from_orm(conv) for conv in conversations]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")

@app.get("/api/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: str, db: Session = Depends(get_db)):
    try:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp).all()
        
        return [MessageResponse.from_orm(msg) for msg in messages]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    try:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        db.delete(conversation)
        db.commit()
        
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

@app.put("/api/conversations/{conversation_id}/title")
async def update_conversation_title(conversation_id: str, title: str, db: Session = Depends(get_db)):
    try:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversation.title = title
        conversation.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Title updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating title: {str(e)}")

@app.get("/api/settings", response_model=SettingsResponse)
async def get_settings():
    return SettingsResponse(
        ai_model="ECHOAL Assistant",
        version="1.0.0",
        features=["chat", "conversations", "settings"]
    )

@app.put("/api/settings")
async def update_settings(settings_data: dict, db: Session = Depends(get_db)):
    try:
        # In a real app, you'd save user-specific settings
        # For now, just return success
        return {"message": "Settings updated successfully", "settings": settings_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating settings: {str(e)}")

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

if __name__ == "__main__":
    uvicorn.run(
        "main_with_db:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
