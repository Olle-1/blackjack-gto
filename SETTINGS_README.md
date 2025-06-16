# Blackjack Settings System Documentation

## Overview

The settings system provides comprehensive configuration management for the Blackjack Card Counter Trainer. All game rules, betting limits, display preferences, and practice modes are now configurable through a user-friendly interface.

## Files Added

### Core Settings Files
- **`settings.py`** - Main settings management with dataclasses and JSON persistence
- **`settings_dialog.py`** - Tkinter-based settings configuration dialog
- **`test_settings_integration.py`** - Integration test suite

### Modified Files
- **`main.py`** - Integrated settings loading, dialog, and auto-deal functionality
- **`game_engine.py`** - Modified to use settings instead of hardcoded values
- **`basic_strategy.py`** - Added settings import for future strategy variations
- **`ui_components.py`** - Added settings-based display visibility controls

## Settings Categories

### 1. Game Rules (`settings.game_rules`)
- **`dealer_stand_soft_17`** - Whether dealer stands on soft 17 (default: True)
- **`blackjack_payout`** - Blackjack payout ratio (default: 1.5 for 3:2)
- **`surrender_allowed`** - Allow surrender (default: False)
- **`late_surrender_only`** - Only late surrender allowed (default: True)
- **`double_after_split`** - Allow doubling after splits (default: True)
- **`double_on_any_two`** - Allow double on any two cards vs 9,10,11 only (default: True)
- **`resplit_aces`** - Allow re-splitting aces (default: False)
- **`max_splits`** - Maximum number of splits allowed (default: 3)
- **`insurance_allowed`** - Allow insurance bets (default: True)

### 2. Betting Limits (`settings.betting_limits`)
- **`min_bet`** - Minimum bet amount (default: $5)
- **`max_bet`** - Maximum bet amount (default: $500)
- **`default_bet`** - Starting bet amount (default: $25)
- **`default_bankroll`** - Starting bankroll (default: $1000)
- **`bet_increment`** - Amount to increase/decrease bets (default: $5)

### 3. Shoe Configuration (`settings.shoe_config`)
- **`num_decks`** - Number of decks in shoe (default: 6)
- **`penetration`** - Percentage dealt before shuffle (default: 0.67)
- **`burn_card`** - Burn first card after shuffle (default: True)

### 4. Practice Modes (`settings.practice_modes`)
- **`auto_deal`** - Automatically deal new hands (default: False)
- **`auto_deal_delay`** - Delay between auto-dealt hands in seconds (default: 2.0)
- **`show_hints_default`** - Show strategy hints by default (default: False)
- **`show_count_default`** - Show count by default (default: True)
- **`show_running_count`** - Display running count (default: True)
- **`show_true_count`** - Display true count (default: True)
- **`show_ev`** - Display expected value (default: True)
- **`show_strategy_feedback`** - Show strategy feedback (default: True)
- **`warn_on_mistakes`** - Warn when making strategy mistakes (default: True)

### 5. Display Preferences (`settings.display_prefs`)
- **`card_style`** - Card display style: "text" or "images" (default: "text")
- **`table_color`** - Table background color (default: "#0a5c2e")
- **`show_probabilities`** - Display hand probabilities (default: False)
- **`show_dealer_hole_card`** - Show dealer hole card in practice (default: False)
- **`animation_speed`** - Animation speed 0-1 (default: 0.5)
- **`sound_enabled`** - Enable sound effects (default: False)

### 6. Counting System (`settings.counting_system`)
- **`system`** - Counting system to use (default: "hi-lo")
- **`show_deck_estimation`** - Show deck estimation (default: True)
- **`true_count_precision`** - Decimal places for true count (default: 1)

## Usage

### Loading and Saving Settings
```python
from settings import settings

# Settings are automatically loaded on import
# Modify settings
settings.shoe_config.num_decks = 8
settings.game_rules.dealer_stand_soft_17 = False

# Save to file
settings.save()

# Reload from file
settings.load()
```

### Opening Settings Dialog
The settings dialog is accessible through the "SETTINGS" button in the game or programmatically:

```python
from settings_dialog import SettingsDialog

def on_settings_saved():
    print("Settings were saved!")

dialog = SettingsDialog(parent_window, settings, on_settings_saved)
dialog.show()
```

### Settings Validation
Settings are automatically validated when saved:

```python
errors = settings.validate()
if errors:
    for error in errors:
        print(f"Validation error: {error}")
```

## Integration Points

### Game Engine Integration
- **Shoe creation** - Uses `settings.shoe_config.num_decks` and `settings.shoe_config.penetration`
- **Dealer rules** - `settings.dealer_must_hit()` method determines dealer actions
- **Blackjack payout** - Uses `settings.game_rules.blackjack_payout`
- **Default values** - Bet amounts and bankroll from settings

### UI Integration
- **Table colors** - Background color from `settings.display_prefs.table_color`
- **Display visibility** - Count and EV displays controlled by practice mode settings
- **Bet controls** - Min/max/increment values from betting limits
- **Auto-deal** - Automatic hand dealing based on practice mode settings

### Strategy Integration
- **Double rules** - Restricts doubling based on `settings.game_rules.double_on_any_two`
- **Surrender options** - Future implementation will use surrender settings
- **Basic strategy variations** - Ready for dealer soft 17 strategy adjustments

## File Persistence

Settings are automatically saved to `settings.json` in the game directory. The file structure:

```json
{
  "game_rules": {
    "dealer_stand_soft_17": true,
    "blackjack_payout": 1.5,
    ...
  },
  "betting_limits": {
    "min_bet": 5,
    "max_bet": 500,
    ...
  },
  ...
}
```

## Auto-Deal Feature

When enabled in practice modes:
- Automatically deals new hands after the specified delay
- Respects the delay setting (0.5-10 seconds)
- Can be disabled by unchecking "Auto-deal new hands"
- Automatically cancelled when manually dealing or changing settings

## Validation Rules

The system enforces these validation rules:
- Minimum bet ≥ $1
- Maximum bet > minimum bet
- Default bet within min/max range
- Number of decks between 1-8
- Penetration between 50%-90%
- Blackjack payout ≥ 1:1
- Max splits between 0-4
- Auto-deal delay between 0.5-10 seconds

## Future Enhancements

The settings system is designed to support:
- Additional counting systems beyond Hi-Lo
- More game rule variations (European rules, etc.)
- Custom color schemes
- Sound configuration
- Advanced practice modes
- Strategy deviation tracking

## Testing

Run the integration test to verify the settings system:

```bash
python3 test_settings_integration.py
```

This validates:
- All imports work correctly
- Settings save/load functionality
- Game engine integration
- Validation rules
- Default value propagation

## Backward Compatibility

The system maintains backward compatibility:
- If no settings file exists, defaults are used
- Old config.py constants are still available
- Game functions normally without settings file
- Settings file is created on first save