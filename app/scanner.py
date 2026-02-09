import os
from pathlib import Path

IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', '.idea', '.vscode', 'dist', 'build'}
IGNORE_FILES = {'.DS_Store', 'package-lock.json', 'yarn.lock', '.env'}
ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.cs', '.go', '.rs', '.md'}

def get_project_context(root_path: str) -> str:
    context_buffer = []
    root = Path(root_path)

    if not root.exists():
        raise FileNotFoundError(f"Directory {root_path} does not exist.")

    context_buffer.append(f"Project Structure for: {root.name}\n")
    
    for path in root.rglob('*'):
        if any(ignored in path.parts for ignored in IGNORE_DIRS):
            continue
            
        if path.is_file():
            if path.name in IGNORE_FILES:
                continue
            if path.suffix not in ALLOWED_EXTENSIONS:
                continue
            
            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
                file_entry = (
                    f"\n{'='*30}\n"
                    f"File: {path.relative_to(root)}\n"
                    f"{'='*30}\n"
                    f"{content}\n"
                )
                context_buffer.append(file_entry)
            except Exception as e:
                print(f"Skipping {path}: {e}")

    return "".join(context_buffer)