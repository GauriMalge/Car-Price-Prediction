#!/bin/bash
# startup.sh - For Azure App Services (Single Process)

# Install dependencies
pip install -r requirements.txt

# Run the application on PORT (Azure sets this automatically)
export PORT=${PORT:-8000}
python main.py
