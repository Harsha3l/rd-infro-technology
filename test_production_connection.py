#!/usr/bin/env python3
"""
Test script to verify the connection between Vercel frontend and Render backend
"""

import requests
import time
import json

# Production URLs
FRONTEND_URL = "https://echoai-git-main-harsha-tri-lakshmis-projects.vercel.app"
BACKEND_URL = "https://echoai-5n2z.onrender.com"

def test_backend_health():
    """Test if the backend is responding"""
    print("🔍 Testing Backend Health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is healthy!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_cors_headers():
    """Test CORS headers for frontend access"""
    print("\n🌐 Testing CORS Headers...")
    try:
        # Test with frontend origin
        headers = {
            'Origin': FRONTEND_URL,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options(f"{BACKEND_URL}/api/chat/send", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ CORS preflight successful!")
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            print(f"   CORS Headers: {cors_headers}")
            return True
        else:
            print(f"❌ CORS preflight failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    print("\n🔧 Testing API Endpoints...")
    
    endpoints = [
        ("/", "Root endpoint"),
        ("/api/settings", "Settings endpoint"),
        ("/api/settings/themes", "Themes endpoint"),
        ("/api/settings/languages", "Languages endpoint")
    ]
    
    success_count = 0
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {description}: OK")
                success_count += 1
            else:
                print(f"❌ {description}: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    return success_count == len(endpoints)

def test_chat_functionality():
    """Test chat functionality"""
    print("\n💬 Testing Chat Functionality...")
    try:
        payload = {
            "content": "Hello from production test!",
            "conversation_id": None
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/chat/send",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat functionality working!")
            print(f"   Conversation ID: {data.get('conversation_id')}")
            print(f"   AI Response: {data.get('message', {}).get('content', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Chat functionality failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    print("\n🌐 Testing Frontend Accessibility...")
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible!")
            return True
        else:
            print(f"❌ Frontend access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 ECHOAL Production Connection Test")
    print("=" * 50)
    print(f"Frontend: {FRONTEND_URL}")
    print(f"Backend: {BACKEND_URL}")
    print("=" * 50)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("CORS Headers", test_cors_headers),
        ("API Endpoints", test_api_endpoints),
        ("Chat Functionality", test_chat_functionality),
        ("Frontend Accessibility", test_frontend_accessibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your frontend and backend are properly connected!")
    else:
        print("⚠️  Some tests failed. Check the issues above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
