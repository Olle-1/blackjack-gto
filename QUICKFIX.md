# Quick Fix Guide

## Display Cut-off Issue - FIXED! ✅

The window height has been increased from 800 to 900 pixels. Just restart the game:
```
python main.py
```

The window is now also resizable, so you can drag the edges if needed!

## Check Your Dependencies

Run this command to check what's installed:
```
python check_dependencies.py
```

Or check manually:

### Check Tkinter:
```
python -c "import tkinter; print('Tkinter OK')"
```

### Check Pillow:
```
python -c "import PIL; print('Pillow OK')"
```

## Install Missing Dependencies

### Install Tkinter (REQUIRED):
- **Windows**: Reinstall Python from python.org and CHECK "tcl/tk and IDLE"
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Mac**: `brew install python-tk`

### Install Pillow (Optional, for better cards):
```
pip install Pillow
```
or
```
python -m pip install Pillow
```

## What You're Seeing

From your screenshot:
- ✅ Tkinter is working (you see the window)
- ✅ Game is running properly 
- ✅ Cards display correctly (4c = 4 of clubs, 9h = 9 of hearts)
- ✅ Running count shows +2 (correct!)
- ❌ Bottom was cut off (now fixed)

## Full Display Should Show:

1. **Count Section**:
   - Running Count: +2
   - True Count: +0.7
   - Eye button (👁) to hide/show

2. **Stats Section**:
   - Session EV: -0.5%
   - Bankroll: $1000

3. **Game Controls**:
   - NEW SHOE button
   - RESET COUNT button
   - SETTINGS button

Now restart the game and you'll see everything!