import os
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:
    print("❌ The `google-genai` library is not installed.")
    print("Please install it using: pip install google-genai")
    exit(1)

load_dotenv()

def list_available_models():
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables.")
        return

    try:
        client = genai.Client(api_key=api_key)

        print("🔍 Fetching available models using new `google-genai` SDK...")
        print("---------------------------------------------------------")
        
        count = 0
        for model in client.models.list():
            if "gemini" in model.name:
                print(f" • {model.name}")
                count += 1
        
        print("---------------------------------------------------------")
        if count == 0:
            print("⚠️ No 'gemini' models found. Check your API Key permissions.")
        else:
            print(f"✅ Found {count} Gemini models.")

    except Exception as e:
        print(f"❌ Error while listing models: {e}")
        print("Make sure your API key is correct and valid.")

if __name__ == "__main__":
    list_available_models()