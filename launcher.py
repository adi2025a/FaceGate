#!/usr/bin/env python3

import sys
import subprocess
from core.face_auth import verify_user

def launch_protected_app(command: list[str]):
    """Runs face verification before launching the protected app."""
    print(f"\n🔒 Verifying face to launch: {' '.join(command)}")

    if verify_user():
        print("✅ Face verified. Launching application...\n")
        try:
            subprocess.Popen(command)
        except Exception as e:
            print(f"❌ Failed to launch application: {e}")
            sys.exit(1)
    else:
        print("❌ Face authentication failed. Access denied.")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("⚠️  No command provided to launcher.")
        print("Usage: python3 launcher.py <app> [args...]")
        sys.exit(1)

    # Get full command from arguments (excluding script name)
    command = sys.argv[1:]
    launch_protected_app(command)

if __name__ == "__main__":
    main()
