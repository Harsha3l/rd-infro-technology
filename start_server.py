#!/usr/bin/env python3
"""
Simple server starter for ECHOAL Backend
This script provides a more reliable way to start the server.
"""

import uvicorn
import sys
import os
from pathlib import Path

def main():
    """Start the ECHOAL backend server"""
    print("🚀 Starting ECHOAL Backend Server...")
    print("=" * 50)
    
    try:
        # Change to the script directory
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Start the server
        uvicorn.run(
            "main:app",
            host="127.0.0.1",  # Use localhost instead of 0.0.0.0
            port=8000,
            reload=False,  # Disable reload for stability
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
