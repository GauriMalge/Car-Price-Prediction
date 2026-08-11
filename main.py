import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from src.gradio_app import demo

# Configuration from environment variables (for Azure)
PORT = int(os.getenv("PORT", 7860))
HOST = os.getenv("WEBSITE_HOSTNAME", "127.0.0.1") if os.getenv("WEBSITE_HOSTNAME") else "127.0.0.1"


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Car Price Predictor")
    print(f"📍 Server running on http://{HOST}:{PORT}")
    print("=" * 60)
    demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 8000)),
    share=False )
