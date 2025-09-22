#!/usr/bin/env python3
"""
ECHOAL Backend Server Runner
This script provides an easy way to run the ECHOAL backend server.
"""

import sys
import os
import uvicorn
from config import settings

def main():
    """Main function to run the server"""
    print("🚀 Starting ECHOAL Backend Server...")
    print(f"📍 Server will run on: http://{settings.HOST}:{settings.PORT}")
    print(f"🔧 Debug mode: {settings.DEBUG}")
    print(f"🌐 CORS origins: {', '.join(settings.ALLOWED_ORIGINS)}")
    print("\n" + "="*50)
    
    try:
        uvicorn.run(
            "main_with_db:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
