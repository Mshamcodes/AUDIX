"""
@file logger.py
@brief Simple Logging Utility for AUDIX System

This module provides basic logging functions for the application,
including timestamped standard logs and error messages.
"""

from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")   

def error(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] ERROR: {message}")

# TEST 
if __name__ == "__main__":
    log("This is a log message.")
    error("This is an error message.")
