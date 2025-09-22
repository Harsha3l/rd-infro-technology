#!/usr/bin/env python3
"""
Test script for ECHOAL API
This script helps test the API endpoints and debug issues.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    """Test the API endpoints"""
    print("🧪 Testing ECHOAL API...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Debug conversations
    print("2. Checking debug conversations...")
    try:
        response = requests.get(f"{BASE_URL}/debug/conversations")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Conversations: {data.get('conversation_count', 0)}")
        print(f"   Messages: {data.get('message_count', 0)}")
        if data.get('conversations'):
            print(f"   Conversation IDs: {list(data['conversations'].keys())}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: Send a message
    print("3. Sending a test message...")
    try:
        payload = {
            "content": "Hello, this is a test message",
            "conversation_id": None
        }
        response = requests.post(f"{BASE_URL}/api/chat/send", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Conversation ID: {data['conversation_id']}")
            print(f"   AI Response: {data['message']['content']}")
            return data['conversation_id']
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 4: Get conversations
    print("4. Getting all conversations...")
    try:
        response = requests.get(f"{BASE_URL}/api/conversations")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            conversations = response.json()
            print(f"   Found {len(conversations)} conversations")
            for conv in conversations:
                print(f"   - {conv['id']}: {conv['title']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 5: Test settings
    print("5. Testing settings...")
    try:
        # Get current settings
        response = requests.get(f"{BASE_URL}/api/settings")
        print(f"   Get settings status: {response.status_code}")
        if response.status_code == 200:
            settings = response.json()
            print(f"   Current theme: {settings.get('theme')}")
            print(f"   Current language: {settings.get('language')}")
            print(f"   Current AI model: {settings.get('ai_model')}")
        
        # Update settings
        update_data = {
            "theme": "dark",
            "language": "en",
            "temperature": 0.8
        }
        response = requests.put(f"{BASE_URL}/api/settings", json=update_data)
        print(f"   Update settings status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Updated fields: {result.get('updated_fields')}")
        
        # Get available themes
        response = requests.get(f"{BASE_URL}/api/settings/themes")
        print(f"   Get themes status: {response.status_code}")
        if response.status_code == 200:
            themes = response.json()
            print(f"   Available themes: {[t['name'] for t in themes['themes']]}")
        
        # Get available languages
        response = requests.get(f"{BASE_URL}/api/settings/languages")
        print(f"   Get languages status: {response.status_code}")
        if response.status_code == 200:
            languages = response.json()
            print(f"   Available languages: {len(languages['languages'])}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 6: Get messages for a conversation
    print("6. Testing get messages...")
    try:
        # First get conversations to find a valid ID
        response = requests.get(f"{BASE_URL}/api/conversations")
        if response.status_code == 200:
            conversations = response.json()
            if conversations:
                conv_id = conversations[0]['id']
                print(f"   Testing with conversation ID: {conv_id}")
                response = requests.get(f"{BASE_URL}/api/conversations/{conv_id}/messages")
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    messages = response.json()
                    print(f"   Found {len(messages)} messages")
                    for msg in messages:
                        print(f"   - {msg['role']}: {msg['content'][:50]}...")
                else:
                    print(f"   Error: {response.text}")
            else:
                print("   No conversations found to test with")
        else:
            print(f"   Error getting conversations: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_api()
