#!/usr/bin/env python3
"""
Startup script for QueryFARMER Translation Service
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from translation_service import app
from translation_config import get_config_summary

def main():
    """Start the translation service"""
    print("🚀 Starting QueryFARMER Translation Service...")
    print("=" * 50)
    
    # Show configuration
    config = get_config_summary()
    print("Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print("=" * 50)
    
    # Start the service
    uvicorn.run(
        "translation_service:app",
        host=config["host"],
        port=config["port"],
        reload=config["debug"],
        log_level="info" if config["debug"] else "warning"
    )

if __name__ == "__main__":
    main()

