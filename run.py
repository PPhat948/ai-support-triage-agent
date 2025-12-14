import uvicorn
import os
import sys
from pathlib import Path

# Add the project root to sys.path to ensure 'app' and 'scripts' packages are importable
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

if __name__ == "__main__":
    # Run the FastAPI app defined in app/main.py
    # "app.main:app" means: module 'app.main', object 'app'
    print(f"🚀 Starting Server from {ROOT_DIR}...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
