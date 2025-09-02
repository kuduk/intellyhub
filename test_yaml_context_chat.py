#!/usr/bin/env python3
"""
Test script per verificare l'implementazione del context YAML nella chat
"""

import requests
import json
import os

# Configurazione
API_BASE_URL = "http://localhost:5000"
TEST_FLOW_ID = "test-flow-123"  # Flow ID di test
YAML_CONTEXT = """name: Test Automation
start_state: first_state
states:
  first_state:
    state_type: command
    command: echo "Hello World"
    transition: end_state
  end_state:
    state_type: end
"""

def test_chat_with_yaml_context():
    """Testa l'endpoint /api/chat con context YAML"""
    
    # Prima ottieni un token (simulato - in realtà dovrebbe essere ottenuto tramite login)
    # Per il test, usiamo un token fittizio
    test_token = "test-token-123"
    
    # Payload di test
    payload = {
        "message": "Aggiungi uno stato che salvi il risultato in un file",
        "flow_id": TEST_FLOW_ID,
        "yaml_context": YAML_CONTEXT
    }
    
    headers = {
        "Authorization": f"Bearer {test_token}",
        "Content-Type": "application/json"
    }
    
    print("Testing /api/chat endpoint with YAML context...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content: {response.text[:500]}...")  # Primi 500 caratteri
        
        if response.status_code == 200:
            print("✅ Chat request succeeded!")
        else:
            print(f"❌ Chat request failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_chat_without_yaml_context():
    """Testa l'endpoint /api/chat senza context YAML per confronto"""
    
    test_token = "test-token-123"
    
    payload = {
        "message": "Crea un'automazione che legge un file RSS",
        "flow_id": TEST_FLOW_ID
        # Nessun yaml_context
    }
    
    headers = {
        "Authorization": f"Bearer {test_token}",
        "Content-Type": "application/json"
    }
    
    print("\n" + "="*50)
    print("Testing /api/chat endpoint WITHOUT YAML context...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Content: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("✅ Chat request succeeded!")
        else:
            print(f"❌ Chat request failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing YAML Context in Chat Implementation")
    print("="*60)
    
    # Test con context YAML
    test_chat_with_yaml_context()
    
    # Test senza context YAML
    test_chat_without_yaml_context()
    
    print("\n" + "="*60)
    print("🎯 Test completed!")