#!/usr/bin/env python3
"""
Alternative entry point for the RFP Analyzer application
"""
import os
from dotenv import load_dotenv
from app import app

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    # Configuration from environment variables
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')
    
    print(f"Starting RFP Analyzer on {host}:{port}")
    print(f"Debug mode: {debug_mode}")
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode
    )
