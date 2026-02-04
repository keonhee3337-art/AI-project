import sys
import subprocess
import os

print(f"--- DIAGNOSTIC ---")
print(f"Python Location: {sys.executable}")
print(f"Trying to install 'openpyxl' to this specific location...")

try:
    # We use the full path to python.exe to ensure we install to the RIGHT place
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
    print("\n✅ SUCCESS: 'openpyxl' is installed!")
except Exception as e:
    print(f"\n❌ AUTOMATIC INSTALL FAILED: {e}")
    print("You must run this command manually in your terminal:")
    print(f'"{sys.executable}" -m pip install openpyxl')