# How to Play Blackjack Card Counter Trainer on Your Flight

## Quick Start Guide for Beginners

### Before Your Flight (5 minutes)

1. **Install Python** (if not already installed)
   - Go to https://www.python.org/downloads/
   - Download Python 3.12 or newer
   - During installation, CHECK "Add Python to PATH"
   - Also CHECK "tcl/tk and IDLE" (includes Tkinter)

2. **Download the Game**
   - Copy the entire `blackjack` folder to your laptop
   - No internet needed once downloaded!

3. **Install Pillow** (optional, for better cards)
   - Open Command Prompt/Terminal
   - Type: `pip install Pillow`
   - If this fails, the game still works with text cards

### Launching the Game

1. **Open Command Prompt/Terminal**
   - Windows: Press Win+R, type `cmd`, press Enter
   - Mac: Press Cmd+Space, type `terminal`, press Enter

2. **Navigate to Game Folder**
   ```
   cd path/to/blackjack
   ```
   Example: `cd C:\Users\YourName\Downloads\blackjack`

3. **Start the Game**
   ```
   python main.py
   ```
   Or if that doesn't work:
   ```
   python3 main.py
   ```

### How to Play

#### Basic Controls
- **SPACE** or click table: Deal new hand
- **H** or HIT button: Take another card
- **S** or STAND button: Keep your hand
- **D** or DOUBLE button: Double bet, take one card

#### Understanding the Display

```
Dealer: 17          [Shows dealer's cards]
[K♠] [7♦]          

BLACKJACK TABLE

[A♥] [5♣] [4♦]     [Your cards]
Player: 20
```

**Bottom Info Panel:**
- **Running Count**: The raw count (+1 for 2-6, -1 for 10-A)
- **True Count**: Running count ÷ decks remaining
- **Session EV**: Your expected value percentage
- **Bankroll**: Your current money

#### Card Counting Basics

The game uses Hi-Lo counting:
- Cards 2-6: Count +1 (good for player)
- Cards 7-9: Count 0 (neutral)
- Cards 10-A: Count -1 (good for house)

**When count is positive**: You have an advantage, consider betting more
**When count is negative**: House has advantage, bet minimum

#### Playing Strategy

1. **Always stand on 17+**
2. **Always hit on 11 or less**
3. **For 12-16**: Depends on dealer's card
   - Hit if dealer shows 7-A
   - Stand if dealer shows 2-6

4. **Double down on**:
   - 11 (always)
   - 10 (unless dealer has A)
   - 9 (if dealer shows 3-6)

#### Practice Mode

Click the **eye button** (👁) to hide/show the count. Practice counting in your head, then check if you're right!

### Troubleshooting

**"No module named tkinter"**
- Windows: Reinstall Python with Tkinter option checked
- Mac/Linux: `sudo apt-get install python3-tk`

**Cards show as text (Ah, Ks, etc)**
- This is normal without Pillow installed
- A = Ace, K = King, Q = Queen, J = Jack
- h = hearts, d = diamonds, c = clubs, s = spades

**Game won't start**
- Make sure you're in the blackjack folder
- Try `python3` instead of `python`
- Check Python is installed: `python --version`

### Flight Tips

1. **Offline Ready**: Once downloaded, no internet needed
2. **Battery Saver**: Close other apps, dim screen
3. **Practice Goals**:
   - Keep accurate running count for 100 hands
   - Achieve positive Session EV
   - Learn basic strategy decisions

4. **Challenge Progression**:
   - Start with count visible
   - Hide count and check every 10 hands
   - Try to maintain count through shuffle

### What the Numbers Mean

- **Positive True Count**: You have mathematical edge
- **+1 True Count** ≈ 0% house edge (even game)
- **+2 True Count** ≈ 0.5% player advantage
- **+4 True Count** ≈ 1.5% player advantage

### Have Fun!

Remember: This is practice for skill development. Real casino play involves real money risk. The goal is to learn card counting as a mental exercise and understand the mathematics of blackjack.

Safe travels and enjoy mastering the count at 30,000 feet! ✈️