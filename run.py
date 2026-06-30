# run.py - Launcher for Kids Story Studio

import subprocess
import webbrowser
import time
import os

print("\n" + "="*60)
print("✨ KIDS STORY STUDIO ✨")
print("="*60 + "\n")

# Create required folders
os.makedirs("data", exist_ok=True)
os.makedirs("stories", exist_ok=True)

print("🚀 Starting Kids Story Studio...")
print("📖 Opening browser at: http://localhost:8501\n")

def open_browser():
    time.sleep(2)
    webbrowser.open("http://localhost:8501")

import threading
threading.Thread(target=open_browser, daemon=True).start()

subprocess.run(["streamlit", "run", "app.py"])