import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
Jesteś Senior Software Architectem i ekspertem od Code Review. 
Twoim zadaniem jest analiza dostarczonego kodu źródłowego projektu.

Wykonaj następujące zadania:
1. **Analiza Architektury:** Opisz ogólną strukturę i wzorce projektowe użyte w kodzie.
2. **Diagram:** Wygeneruj kod diagramu w formacie Mermaid.js (np. classDiagram lub graph TD), który wizualizuje zależności między modułami.
3. **Analiza SOLID/Clean Code:** Wskaż 3 główne obszary, które łamią zasady SOLID lub są trudne w utrzymaniu. Podaj sugestie poprawek.
4. **Dokumentacja:** Wygeneruj krótki, profesjonalny tekst do pliku README.md opisujący co ten projekt robi (na podstawie analizy kodu).

Formatuj odpowiedź używając Markdown. Kod Mermaid umieść w bloku kodu ```mermaid.
"""

def analyze_code(context: str):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    full_prompt = f"{SYSTEM_PROMPT}\n\nOto kod projektu do analizy:\n{context}"
    
    response = model.generate_content(full_prompt)
    return response.text