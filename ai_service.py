import openai
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        # Initialize OpenAI client
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    def generate_response(self, user_message: str, conversation_history: list = None) -> str:
        """
        Generate AI response using OpenAI API
        """
        try:
            # Prepare conversation history
            messages = []
            
            # Add system message
            messages.append({
                "role": "system",
                "content": "You are ECHOAL, a helpful AI assistant. Be friendly, informative, and engaging in your responses. Keep responses concise but helpful."
            })
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-10:]:  # Limit to last 10 messages
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Fallback response if AI service fails
            return f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}"
    
    def generate_conversation_title(self, first_message: str) -> str:
        """
        Generate a title for the conversation based on the first message
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Generate a short, descriptive title (max 50 characters) for a conversation that starts with this message. Return only the title, no quotes or extra text."
                    },
                    {
                        "role": "user",
                        "content": first_message
                    }
                ],
                max_tokens=20,
                temperature=0.5
            )
            
            title = response.choices[0].message.content.strip()
            # Remove quotes if present
            title = title.strip('"\'')
            return title[:50]  # Ensure max 50 characters
            
        except Exception as e:
            # Fallback title
            return first_message[:50] + "..." if len(first_message) > 50 else first_message

# Alternative simple AI service for testing without OpenAI
class SimpleAIService:
    def __init__(self):
        self.responses = [
            "I understand you're asking about {topic}. Let me help you with that.",
            "That's an interesting question! Here's what I think about {topic}...",
            "I'd be happy to assist you with {topic}. Let me provide some insights.",
            "Great question! Regarding {topic}, here's my perspective...",
            "I can definitely help you explore {topic}. Let me share some thoughts on this.",
            "Thanks for sharing that with me. I'd be glad to help you with {topic}.",
            "That's a great point about {topic}. Let me elaborate on that for you.",
            "I appreciate you asking about {topic}. Here's what I can tell you...",
            "Interesting! When it comes to {topic}, I have some thoughts to share.",
            "I'm here to help with {topic}. Let me provide some guidance on this."
        ]
    
    def generate_response(self, user_message: str, conversation_history: list = None) -> str:
        import random
        keywords = user_message.lower().split()[:3]
        topic = " ".join(keywords) if keywords else "your question"
        
        response_template = random.choice(self.responses)
        return response_template.format(topic=topic)
    
    def generate_conversation_title(self, first_message: str) -> str:
        return first_message[:50] + "..." if len(first_message) > 50 else first_message

# Use simple AI service if OpenAI API key is not available
def get_ai_service():
    if os.getenv("OPENAI_API_KEY"):
        return AIService()
    else:
        return SimpleAIService()
