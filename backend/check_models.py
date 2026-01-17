import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: No API Key found in .env file.")
else:
    print(f"✅ Key found: {api_key[:5]}... (hidden)")
    
    try:
        genai.configure(api_key=api_key)
        print("\n🔍 Asking Google for available models...")
        
        found_any = False
        for m in genai.list_models():
            # Only show models that can write text (generateContent)
            if 'generateContent' in m.supported_generation_methods:
                print(f" - {m.name}")
                found_any = True
        
        if not found_any:
            print("❌ No text-generation models found. Check your API Key permissions.")
            
    except Exception as e:
        print(f"❌ Error connecting to Google: {e}")