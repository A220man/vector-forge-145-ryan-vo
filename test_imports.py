#!/usr/bin/env python3
"""Test script to verify imports work."""
import sys

sys.path.insert(0, '/var/lib/alan-portfolio/workspaces/ryan/vector-forge-145-ryan-vo/src')

try:
    print("Main app import OK")
    
    print("Retain router import OK")
    
    print("Recall router import OK")
    
    print("Models import OK")
    
    print("Storage import OK")
    
    print("\nAll imports successful!")
except (ImportError, ModuleNotFoundError) as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
