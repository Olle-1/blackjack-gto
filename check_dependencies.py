"""Check if required dependencies are installed"""

import sys
import subprocess

def check_tkinter():
    """Check if Tkinter is installed"""
    try:
        import tkinter
        print("✅ Tkinter is installed")
        return True
    except ImportError:
        print("❌ Tkinter is NOT installed")
        return False

def check_pillow():
    """Check if Pillow is installed"""
    try:
        import PIL
        print("✅ Pillow is installed")
        return True
    except ImportError:
        print("❌ Pillow is NOT installed (game will use text-based cards)")
        return False

def install_instructions():
    """Provide installation instructions"""
    print("\n📦 Installation Instructions:")
    print("\nFor Tkinter:")
    print("  Windows: Reinstall Python and check 'tcl/tk and IDLE' option")
    print("  Ubuntu/Debian: sudo apt-get install python3-tk")
    print("  Mac: brew install python-tk")
    
    print("\nFor Pillow (optional, for card images):")
    print("  All platforms: pip install Pillow")
    print("  or: python -m pip install Pillow")
    print("  or: python3 -m pip install Pillow")

def main():
    print("🎰 Blackjack Card Counter - Dependency Check\n")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print()
    
    # Check dependencies
    has_tkinter = check_tkinter()
    has_pillow = check_pillow()
    
    if not has_tkinter:
        print("\n⚠️  Tkinter is REQUIRED to run the game!")
        install_instructions()
    elif not has_pillow:
        print("\n💡 The game will work without Pillow, but cards will be text-based")
        print("   To get nice card images, install Pillow:")
        print("   pip install Pillow")
    else:
        print("\n✨ All dependencies are installed! You're ready to play!")
        print("   Run: python main.py")

if __name__ == "__main__":
    main()