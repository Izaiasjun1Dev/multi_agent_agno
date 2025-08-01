#!/usr/bin/env python3
"""
Script principal para executar a aplicação Inner API.
"""

import uvicorn

from presentation.app import app

if __name__ == "__main__":
    # Para desenvolvimento com reload
    uvicorn.run(
        "presentation.app:app", 
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        reload_dirs=["src"],
    )
