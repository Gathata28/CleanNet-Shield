#!/usr/bin/env python3
"""
Debug script to test CleanNet Shield imports and functionality
"""

import sys
import os

def test_imports():
    """Test all module imports"""
    print("🧪 Testing CleanNet Shield imports...")
    
    try:
        # Test standard library imports
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        print("✅ Email modules imported")
        
        import json
