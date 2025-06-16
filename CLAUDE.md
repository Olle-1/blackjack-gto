# Blackjack Card Counter Trainer - Codebase Context

## Project Overview
A Windows 11 desktop blackjack game designed to train card counting skills. Built with Python and Tkinter for a standalone executable that requires no installation.

## Architecture
The codebase follows MVC pattern with clear separation:
- **Model**: game_engine.py (game logic)
- **View**: ui_components.py (UI widgets)
- **Controller**: main.py (coordinates everything)

## Key Technical Decisions
1. **No animations** - User specifically requested functional over visual
2. **Text-based cards** - Fallback display that works without images
3. **Modular design** - Each component can be tested independently
4. **Hi-Lo counting** - Standard +1/-1 system implemented

## Core Files
- `main.py` - Entry point, game coordination
- `game_engine.py` - Card, Shoe, Hand, GameState classes
- `card_counting.py` - Hi-Lo counting implementation  
- `ev_calculator.py` - Expected value and betting strategies
- `basic_strategy.py` - Basic strategy tables and tracking
- `ui_components.py` - All Tkinter UI components
- `config.py` - Game settings and constants

## Game Flow
1. New shoe shuffled → 6 decks (312 cards)
2. Player presses SPACE → Deal new hand
3. Count updates in real-time as cards dealt
4. Player actions: Hit/Stand/Double (Split TODO)
5. Dealer plays by house rules (stand on 17)
6. Outcome calculated, bankroll updated
7. At penetration (~4 decks), auto-shuffle

## Counting System
- 2-6: +1
- 7-9: 0 
- 10-A: -1
- True count = Running count / Decks remaining
- EV = -0.5% + (0.5% × True Count)

## Basic Strategy
- Complete lookup tables for hard/soft hands and pairs
- Real-time feedback on player decisions
- Strategy adherence percentage tracking
- Optional hints mode shows optimal play
- Tracks and displays deviations from optimal strategy

## UI Layout
```
[Message Display]
[Blackjack Table Canvas]
  - Dealer cards/score
  - Player cards/score
[Control Buttons: HIT|STAND|DOUBLE|SPLIT] [Bet: $XX [-][+]]
[Count Display] [Actual EV/Bankroll Display]
[Strategy Display: Show Hints checkbox | Strategy: XX% | Feedback]
[Session Statistics: W/L/P | Win% | P/L | Avg Bet | Expected vs Actual EV]
[Game Controls: NEW SHOE|RESET COUNT|SETTINGS]
```

## Keyboard Shortcuts
- H: Hit
- S: Stand  
- D: Double
- Space: New hand
- Esc: Quit

## Testing
- Run `python3 test_game_engine.py` to verify core logic
- Run `python3 test_basic_strategy.py` to verify strategy tables
- Run `python3 verify_shoe.py` to verify shoe/deck mechanics

## Dependencies
- Python 3.12+
- Tkinter (for UI)
- Pillow (for card images, optional)

## Current State
- Core game: ✅ Fully functional
- Card counting: ✅ Complete
- UI: ✅ Working with text cards
- Basic strategy: ✅ Implemented with hints
- Packaging: ❌ Not created yet

## Important Notes
- Requires Tkinter installation to run UI
- Text-based cards work without Pillow
- All game logic tested and working
- Ready for play, just needs dependencies