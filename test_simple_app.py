#!/usr/bin/env python3
"""
Simple test for the new app.py
"""

import requests
import json

def test_local_app():
    """Test the app locally"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing ECHOAL Backend (app.py)")
    print("=" * 50)
    
    try:
        # Test root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
        
        # Test health endpoint
        print("\n2. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test chat endpoint
        print("\n3. Testing chat endpoint...")
        chat_data = {
            "content": "Hello from test!",
            "conversation_id": None
        }
        response = requests.post(
            f"{base_url}/api/chat/send",
            json=chat_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Chat endpoint working")
            result = response.json()
            print(f"   Conversation ID: {result.get('conversation_id')}")
            print(f"   AI Response: {result.get('message', {}).get('content', 'N/A')}")
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test settings endpoint
        print("\n4. Testing settings endpoint...")
        response = requests.get(f"{base_url}/api/settings", timeout=5)
        if response.status_code == 200:
            print("✅ Settings endpoint working")
            print(f"   Settings: {response.json()}")
        else:
            print(f"❌ Settings endpoint failed: {response.status_code}")
            return False
        
        print("\n🎉 All tests passed! The app is working correctly.")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to local server. Make sure to run: python app.py")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_local_app()
    exit(0 if success else 1)
