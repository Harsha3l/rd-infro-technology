#!/usr/bin/env python3
"""
Quick test to verify the server is working
"""

import requests
import time
import sys

def test_server():
    """Test if the server is running and responding"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing ECHOAL Server...")
    print("=" * 40)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health check passed")
            print(f"   📊 Response: {response.json()}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
        
        # Test root endpoint
        print("\n2. Testing root endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Root endpoint working")
            print(f"   📊 Response: {response.json()}")
        else:
            print(f"   ❌ Root endpoint failed: {response.status_code}")
            return False
        
        # Test settings endpoint
        print("\n3. Testing settings endpoint...")
        response = requests.get(f"{base_url}/api/settings", timeout=5)
        if response.status_code == 200:
            print("   ✅ Settings endpoint working")
            settings = response.json()
            print(f"   🎨 Theme: {settings.get('theme')}")
            print(f"   🌍 Language: {settings.get('language')}")
        else:
            print(f"   ❌ Settings endpoint failed: {response.status_code}")
            return False
        
        print("\n🎉 All tests passed! Server is working correctly.")
        print(f"🌐 Server is running at: {base_url}")
        print("📚 API Documentation: http://127.0.0.1:8000/docs")
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server. Is it running?")
        print("   💡 Try running: python start_server.py")
        return False
    except Exception as e:
        print(f"   ❌ Error testing server: {e}")
        return False

if __name__ == "__main__":
    success = test_server()
    if not success:
        sys.exit(1)
