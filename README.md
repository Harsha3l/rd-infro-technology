# ECHOAL Backend API

A Python FastAPI backend for the ECHOAL AI Assistant frontend application.

## Features

- 🤖 AI-powered chat responses (OpenAI integration)
- 💬 Conversation management
- 📝 Message history
- ⚙️ Settings management
- 🔄 CORS support for frontend integration
- 🗄️ SQLite database (easily upgradeable to PostgreSQL/MySQL)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=sqlite:///./echoal.db

# OpenAI Configuration (Optional - will use simple AI if not provided)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173
```

### 3. Run the Server

**Option A: Simple version (in-memory storage)**
```bash
python main.py
```

**Option B: Database version (recommended)**
```bash
python main_with_db.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Chat
- `POST /api/chat/send` - Send a message and get AI response
- `GET /api/conversations` - Get all conversations
- `GET /api/conversations/{id}/messages` - Get messages for a conversation
- `DELETE /api/conversations/{id}` - Delete a conversation
- `PUT /api/conversations/{id}/title` - Update conversation title

### Settings
- `GET /api/settings` - Get current settings
- `PUT /api/settings` - Update settings

### Health
- `GET /` - Root endpoint
- `GET /health` - Health check

## API Usage Examples

### Send a Message
```bash
curl -X POST "http://localhost:8000/api/chat/send" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello, how are you?",
    "conversation_id": null
  }'
```

### Get Conversations
```bash
curl -X GET "http://localhost:8000/api/conversations"
```

### Get Messages for a Conversation
```bash
curl -X GET "http://localhost:8000/api/conversations/{conversation_id}/messages"
```

## Frontend Integration

The API is configured with CORS to work with your frontend. Update your frontend to make requests to:

- Base URL: `http://localhost:8000`
- API endpoints: `/api/*`

### Example Frontend Integration

```javascript
// Send a message
const sendMessage = async (content, conversationId = null) => {
  const response = await fetch('http://localhost:8000/api/chat/send', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      content,
      conversation_id: conversationId
    })
  });
  return await response.json();
};

// Get conversations
const getConversations = async () => {
  const response = await fetch('http://localhost:8000/api/conversations');
  return await response.json();
};
```

## Database

The application uses SQLite by default, but can be easily configured to use PostgreSQL or MySQL by updating the `DATABASE_URL` in your `.env` file.

### Database Schema

- **Conversations**: Store conversation metadata
- **Messages**: Store individual messages
- **UserSettings**: Store user preferences

## AI Integration

The backend supports two AI modes:

1. **OpenAI Integration** (if API key provided): Uses GPT models for responses
2. **Simple AI** (fallback): Uses predefined response templates

To use OpenAI:
1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Add it to your `.env` file
3. Restart the server

## Development

### Project Structure
```
├── main.py              # Simple FastAPI app (in-memory)
├── main_with_db.py      # Full FastAPI app with database
├── models.py            # SQLAlchemy database models
├── database.py          # Database configuration
├── ai_service.py        # AI integration service
├── config.py            # Application configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Features

1. **New API Endpoints**: Add to `main_with_db.py`
2. **Database Changes**: Update `models.py` and run migrations
3. **AI Improvements**: Modify `ai_service.py`

## Deployment

### Using Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main_with_db.py"]
```

### Environment Variables for Production

```env
DATABASE_URL=postgresql://user:password@localhost/echoal
OPENAI_API_KEY=your_production_key
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure your frontend URL is in `ALLOWED_ORIGINS`
2. **Database Errors**: Ensure the database file is writable
3. **AI Not Working**: Check your OpenAI API key and internet connection

### Logs

The server logs are displayed in the console. For production, consider using a proper logging solution.

## License

This project is open source and available under the MIT License.
