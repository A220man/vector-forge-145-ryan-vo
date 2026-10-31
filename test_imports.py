#!/usr/bin/env python3
"""Test script to verify imports work."""
import sys
sys.path.insert(0, '/var/lib/alan-portfolio/workspaces/ryan/vector-forge-145-ryan-vo/src')

try:
    from vector_forge.main import app
    print("Main app import OK")
    
    from vector_forge.api.retain import router as retain_router
    print("Retain router import OK")
    
    from vector_forge.api.recall import router as recall_router
    print("Recall router import OK")
    
    from vector_forge.models.memory import (
        MemoryItem,
        RetainRequest,
        RetainResponse,
        RecallRequest,
        RecallResponse,
        RecallResult,
    )
    print("Models import OK")
    
    from vector_forge.storage.memory import memory_storage
    print("Storage import OK")
    
    print("\nAll imports successful!")
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
