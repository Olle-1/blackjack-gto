# Blackjack Card Counter Trainer

A Windows 11 desktop application for blackjack card counting training with real-time EV calculations.

## Project Structure

```
blackjack/
├── main.py              # Entry point with Tkinter UI
├── game_engine.py       # Core game logic (Card, Shoe, Hand, GameState)
├── card_counting.py     # Hi-Lo counting system implementation
├── ev_calculator.py     # Expected Value calculations
├── ui_components.py     # Tkinter UI components
├── config.py           # Game settings and constants
├── test_game_engine.py # Test script for core functionality
├── cards/              # Directory for card images (to be added)
└── requirements.txt    # Python dependencies
```

## Core Components Implemented

### Phase 1 ✓ Complete
- Project structure created
- All base Python modules implemented
- Configuration system in place
- Core game engine functional

### Game Engine Features
- **Card & Deck Management**: 6-deck shoe with penetration tracking
- **Hand Calculation**: Proper soft/hard ace handling
- **Game Rules**: Dealer stands on 17, blackjack pays 3:2
- **Hi-Lo Counting**: Running count and true count calculation
- **EV Calculation**: Base house edge -0.5%, +0.5% per true count

## Installation

1. Install Python 3.12+ with Tkinter support
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python3 main.py
```

Note: Tkinter must be installed. On Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

## Testing

Run core game logic tests:
```bash
python3 test_game_engine.py
```

## Development Status

Currently implemented:
- Complete game engine without UI dependencies
- Card counting logic
- EV calculation system
- Full Tkinter UI structure (requires Tkinter to run)

Next steps (Phase 2-3):
- Test UI with Tkinter installed
- Add card images
- Implement split functionality
- Add basic strategy validation