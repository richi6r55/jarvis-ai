# Comprehensive testing and validation

import subprocess
import sys

def run_tests():
    """Run all tests"""
    print("🧪 Running tests...")
    
    # Run pytest if available
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Could not run pytest: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
