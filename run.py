#!/usr/bin/env python3
"""
Bot runner script
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.main import main

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBot stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nCritical error: {e}")
        sys.exit(1)
        