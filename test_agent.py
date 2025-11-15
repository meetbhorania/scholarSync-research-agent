"""
Final working test with correct model name
"""

import requests
import json

API_KEY = 'AIzaSyCBrGHV-DEX9tdaA_6IV7cCOJvf4nx30PE'  # Your actual key

print("🚀 Testing Gemini API with correct model...\n")

# Use the correct model name from the list
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'

headers = {'Content-Type': 'application/json'}

data = {
    'contents': [{
        'parts': [{
            'text': 'Say hello and confirm you are working!'
        }]
    }]
}

try:
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        print("✅ SUCCESS! Your setup is working!\n")
        print("📝 Agent Response:")
        print(text)
        print("\n🎉 Perfect! You're ready to build the research agent!")

    else:
        print(f"❌ Error {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")