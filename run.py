#!/usr/bin/env python3
"""
Gruvbox Login System v2 - Easy startup script
Features: Split CSS architecture + Custom salting
Usage: python run.py
"""

import subprocess
import sys
import os

def main():
    try:
        print("🚀 Starting Gruvbox Login System v2...")
        print("✨ New features: Split CSS + Custom Salting")
        print("📍 Server will be available at: http://localhost:8000")
        print("📖 Login page: http://localhost:8000/")
        print("📝 Signup page: http://localhost:8000/signup")
        print("\n" + "="*60)
        print("🎨 CSS Architecture:")
        print("   - color.css: HSLA color definitions")
        print("   - login.css: All styling and layout")
        print("🔐 Security: Custom # salting + bcrypt hashing")
        print("="*60 + "\n")

        # Run the FastAPI application
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])

    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Make sure you've installed dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
