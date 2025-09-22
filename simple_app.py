#!/usr/bin/env python3
"""
Ultra-simple FastAPI app for Render
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ECHOAL Backend is running!", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/chat/send")
def send_message(data: dict):
    return {
        "conversation_id": "test-123",
        "message": {
            "id": "msg-123",
            "content": f"Echo: {data.get('content', 'Hello!')}",
            "timestamp": "2025-09-22T20:00:00Z",
            "role": "assistant"
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
