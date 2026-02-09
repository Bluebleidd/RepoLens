import os
import time
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

load_dotenv()

def generate_analysis(system_prompt: str, project_text: str, model: str = "gemini-2.0-flash") -> str:
    if genai is None:
        return (
            "# CRITICAL ERROR\n"
            "The `google-genai` library is not installed.\n"
            "Please run: pip install google-genai"
        )

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "# CRITICAL ERROR\nGEMINI_API_KEY environment variable is not set."

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return f"# CRITICAL ERROR\nFailed to initialize Gemini Client: {e}"

    full_prompt = f"{system_prompt}\n\nHere is the source code of the project:\n{project_text}"
    
    generate_config = types.GenerateContentConfig(
        temperature=0.15
    )

    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=full_prompt,
                config=generate_config
            )
            
            if response.text:
                return response.text
            else:
                return "ERROR: The model returned an empty response."

        except Exception as e:
            error_msg = str(e)
            
            if attempt < max_retries - 1:
                wait_time = 10
                print(f"API Error (attempt {attempt+1}/{max_retries}): {error_msg}")
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"API Error (attempt {attempt+1}/{max_retries}): {error_msg}")
                return f"# CRITICAL ERROR\nFailed to generate report after {max_retries} attempts.\nLast error: {error_msg}"

    return "# CRITICAL ERROR\nAn unexpected error occurred in the retry loop."