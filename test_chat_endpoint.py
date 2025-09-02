#!/usr/bin/env python3
"""
Test script for the /api/chat endpoint
"""

import requests
import json
import os
import sys

def test_chat_endpoint():
    """Test the /api/chat endpoint with authentication"""
    
    # Configuration
    BASE_URL = "http://localhost:5000"
    TEST_EMAIL = "paggio@gmail.com"  # Update with your test user
    TEST_PASSWORD = "your_password"  # Update with your password
    
    print("🧪 Testing /api/chat endpoint")
    print("=" * 50)
    
    # Step 1: Authentication
    print("1. Authenticating user...")
    auth_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        auth_response = requests.post(f"{BASE_URL}/api/auth/login", json=auth_data)
        
        if auth_response.status_code != 200:
            print(f"   ❌ Authentication failed: {auth_response.status_code}")
            print(f"   Response: {auth_response.text}")
            return
        
        auth_result = auth_response.json()
        access_token = auth_result.get("access_token")
        
        if not access_token:
            print("   ❌ No access token in response")
            return
        
        print(f"   ✅ Authentication successful")
        print(f"   Token: {access_token[:30]}...")
        
    except Exception as e:
        print(f"   ❌ Authentication error: {e}")
        return
    
    # Step 2: Create or get a flow for testing
    print("\n2. Getting user flows...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        flows_response = requests.get(f"{BASE_URL}/api/flows", headers=headers)
        
        if flows_response.status_code != 200:
            print(f"   ❌ Failed to get flows: {flows_response.status_code}")
            print(f"   Response: {flows_response.text}")
            return
        
        flows = flows_response.json()
        
        if not flows or len(flows) == 0:
            print("   📋 No flows found, creating a test flow...")
            
            # Create a test flow
            flow_data = {
                "name": "Chat Test Flow",
                "yaml_content": "name: Test Flow\nstart_state: start\nstates:\n  start:\n    state_type: end"
            }
            
            create_response = requests.post(f"{BASE_URL}/api/flows", json=flow_data, headers=headers)
            
            if create_response.status_code != 201:
                print(f"   ❌ Failed to create flow: {create_response.status_code}")
                print(f"   Response: {create_response.text}")
                return
            
            flow = create_response.json()
            flow_id = flow.get("id")
        else:
            flow = flows[0]
            flow_id = flow.get("id")
        
        print(f"   ✅ Using flow: {flow.get('name')} (ID: {flow_id})")
        
    except Exception as e:
        print(f"   ❌ Flows error: {e}")
        return
    
    # Step 3: Test the chat endpoint
    print("\n3. Testing /api/chat endpoint...")
    
    chat_data = {
        "message": "Create a simple automation that sends a notification when a file is uploaded",
        "flow_id": flow_id
    }
    
    try:
        print(f"   📤 Sending message: {chat_data['message'][:60]}...")
        
        chat_response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers)
        
        print(f"   📊 Status Code: {chat_response.status_code}")
        print(f"   📊 Content Type: {chat_response.headers.get('Content-Type', 'N/A')}")
        
        if chat_response.status_code == 200:
            # The response should be YAML content as plain text
            yaml_content = chat_response.text
            print(f"   ✅ Chat request successful!")
            print(f"   📋 Response length: {len(yaml_content)} characters")
            print(f"   📋 First 200 characters:")
            print(f"   {yaml_content[:200]}...")
            
        else:
            print(f"   ❌ Chat request failed: {chat_response.status_code}")
            try:
                error_data = chat_response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Raw response: {chat_response.text[:500]}...")
        
    except Exception as e:
        print(f"   ❌ Chat endpoint error: {e}")
        return
    
    # Step 4: Test the chat status endpoint
    print("\n4. Testing /api/chat/status endpoint...")
    
    try:
        status_response = requests.get(f"{BASE_URL}/api/chat/status", headers=headers)
        
        print(f"   📊 Status Code: {status_response.status_code}")
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"   ✅ Chat status retrieved successfully!")
            print(f"   📋 Status: {json.dumps(status_data, indent=2)}")
        else:
            print(f"   ❌ Status request failed: {status_response.status_code}")
            print(f"   Response: {status_response.text}")
        
    except Exception as e:
        print(f"   ❌ Status endpoint error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Chat endpoint testing completed!")

def show_usage_examples():
    """Show curl examples for testing the chat endpoint"""
    
    print("\n📖 CURL Examples for /api/chat endpoint:")
    print("=" * 50)
    
    print("\n1. Authentication:")
    print("""curl -X POST http://localhost:5000/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "your_email@example.com",
    "password": "your_password"
  }'""")
    
    print("\n2. Chat Request:")
    print("""curl -X POST http://localhost:5000/api/chat \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "Create an automation that monitors RSS feeds and sends Telegram notifications",
    "flow_id": "your-flow-uuid-here"
  }'""")
    
    print("\n3. Chat Status:")
    print("""curl -X GET http://localhost:5000/api/chat/status \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN\"""")
    
    print("\n📋 Expected Response Format:")
    print("The /api/chat endpoint returns YAML content directly as plain text:")
    print("""
Content-Type: text/plain; charset=utf-8

name: RSS Telegram Notifier
start_state: check_rss
states:
  check_rss:
    state_type: rss
    url: '{rss_feed_url}'
    transition: send_notification
  send_notification:
    state_type: telegram
    bot_token: '{telegram_bot_token}'
    chat_id: '{telegram_chat_id}'
    message: 'New article: {title}'
    transition: end
  end:
    state_type: end
""")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--examples":
        show_usage_examples()
    else:
        test_chat_endpoint()
        show_usage_examples()