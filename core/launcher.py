import subprocess
import sys
from core.face_auth import verify_user

def launch_protected_app(command: str):
    """Run face auth before launching the protected app."""
    print(f"🔒 Verifying face to launch: {command}")

    if verify_user():
        print("✅ Face verified. Launching application...")
        try:
            subprocess.Popen(command.split())
        except Exception as e:
            print(f"❌ Failed to launch: {e}")
    else:
        print("❌ Face authentication failed. Access denied.")
        sys.exit(1)
