import os
from dotenv import load_dotenv
from .gemini_client import generate_analysis

load_dotenv()

SYSTEM_PROMPT = """
You are a Senior Software Architect and an expert in Code Review.
Your task is to analyze the provided source code of a project.

Perform the following tasks:
1. Architectural Analysis: Describe the overall structure and design patterns.
2. Diagram: If possible, generate a diagram in Mermaid.js format.
3. SOLID/Clean Code Analysis: Identify the main areas for improvement with a brief justification.
4. Documentation: Generate a short description for README.md (sections "What it is" and "How to run").

In your response, use a clear Markdown format with headings and lists.
"""


def analyze_code(context: str, model: str) -> str:
    try:
        report = generate_analysis(SYSTEM_PROMPT, context, model=model)
        return report
    except Exception as e:
        return f"ERROR: {e}"