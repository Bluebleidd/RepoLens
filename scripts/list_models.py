import os
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:
    print("   The `google-genai` library is not installed.")
    print("Please install it using: pip install google-genai")
    exit(1)

load_dotenv()

def list_available_models():
    if not os.getenv("GEMINI_API_KEY"):
        print("   Error: GEMINI_API_KEY not found in environment variables.")
        print("   Please add it to your .env file.")
        return

    try:
        client = genai.Client()

        print("   Fetching available models...")
        print("---------------------------------------------------------")
        
        count = 0
        for model in client.models.list():
            if "generateContent" in model.supported_actions:
                print(f" • {model.display_name} ({model.name})")
                count += 1
        
        print("---------------------------------------------------------")
        if count == 0:
            print("   No models found that support content generation. Check your API Key permissions.")
        else:
            print(f"   Found {count} usable models.")

    except Exception as e:
        print(f"   Error while listing models: {e}")
        print("   Make sure your API key is correct and valid.")

if __name__ == "__main__":
    list_available_models()