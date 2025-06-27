#!/usr/bin/env python3
"""
Simple functionality test for CleanNet Shield
Tests core features without requiring GUI interaction
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_core_functionality():
    """Test core functionality without GUI"""
    
    print("🧪 CleanNet Shield - Core Functionality Test")
    print("=" * 50)
    
    try:
        # Test logger
