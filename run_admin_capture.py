
import subprocess
import sys
import os

# Run the admin typing capture script
try:
    result = subprocess.run([sys.executable, "admin_typing_capture.py"], 
                          capture_output=False, text=True)
    print("Admin typing capture completed successfully!")
except Exception as e:
    print(f"Error: {e}")
