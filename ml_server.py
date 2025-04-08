import subprocess
import time
import requests
import os

def start_ml_server():
    """Start the FastAPI ML server if not already running"""
    try:
        # Check if server is already running
        response = requests.get("http://localhost:8000/docs")
        print("[INFO] ML server already running")
    except:
        print("[INFO] Starting ML server...")
        # Get the correct path to the FastAPI main.py file
        # The "flask" directory actually contains the ML model and FastAPI app
        fastapi_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flask")
        
        # Change to the FastAPI directory and start the server
        os.chdir(fastapi_dir)
        # Make sure main.py exists in this directory and contains a FastAPI app
        subprocess.Popen(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])
        
        time.sleep(2)  # Wait for server to start
        print("[INFO] ML server started")

if __name__ == "__main__":
    start_ml_server()
