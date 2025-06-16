"""Settings management system for Blackjack Card Counter Trainer"""

import json
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict

@dataclass
class GameRules:
    """Game rule settings"""
    dealer_stand_soft_17: bool = True  # True = stand, False = hit
    dealer_stand_value: int = 17
    blackjack_payout: float = 1.5  # 3:2 payout
    surrender_allowed: bool = False
    late_surrender_only: bool = True
    double_after_split: bool = True
    resplit_aces: bool = False
    max_splits: int = 3
    double_on_any_two: bool = True  # False = only 10,11
    insurance_allowed: bool = True
    split_aces_one_card: bool = True  # Split aces get only one card each
    
@dataclass
class BettingLimits:
    """Betting limit settings"""
    min_bet: int = 5
    max_bet: int = 500
    default_bet: int = 25
    default_bankroll: int = 1000
    bet_increment: int = 5
    
    # Betting strategy settings
    betting_strategy: str = "flat"  # "flat", "spread", "kelly"
    spread_min_multiplier: float = 1.0  # Minimum bet multiplier for spread betting
    spread_max_multiplier: float = 8.0  # Maximum bet multiplier for spread betting
    kelly_fraction: float = 0.25  # Fractional Kelly (25% of full Kelly)
    spread_start_count: float = 1.0  # True count to start spreading bets
    
@dataclass
class ShoeConfiguration:
    """Shoe and deck settings"""
    num_decks: int = 6
    penetration: float = 0.67  # Deal ~67% before shuffle
    burn_card: bool = True  # Burn first card after shuffle
    
@dataclass
class PracticeModes:
    """Practice and training settings"""
    auto_deal: bool = False
    auto_deal_delay: float = 2.0  # seconds between hands
    show_hints_default: bool = False
    show_count_default: bool = True
    show_true_count: bool = True
    show_running_count: bool = True
    show_ev: bool = True
    show_strategy_feedback: bool = True
    warn_on_mistakes: bool = True
    
@dataclass
class DisplayPreferences:
    """UI display preferences"""
    card_style: str = "text"  # "text" or "images"
    table_color: str = "#0a5c2e"
    show_probabilities: bool = False
    show_dealer_hole_card: bool = False  # For practice mode
    animation_speed: float = 0.5  # 0 = instant, 1 = normal
    sound_enabled: bool = False
    
@dataclass
class CountingSystem:
    """Card counting system settings"""
    system: str = "hi-lo"  # Currently only hi-lo supported
    show_deck_estimation: bool = True
    true_count_precision: int = 1  # Decimal places
    
class Settings:
    """Main settings manager class"""
    
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = settings_file
        
        # Initialize all setting groups
        self.game_rules = GameRules()
        self.betting_limits = BettingLimits()
        self.shoe_config = ShoeConfiguration()
        self.practice_modes = PracticeModes()
        self.display_prefs = DisplayPreferences()
        self.counting_system = CountingSystem()
        
        # Load saved settings if they exist
        self.load()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert all settings to a dictionary"""
        return {
            "game_rules": asdict(self.game_rules),
            "betting_limits": asdict(self.betting_limits),
            "shoe_config": asdict(self.shoe_config),
            "practice_modes": asdict(self.practice_modes),
            "display_prefs": asdict(self.display_prefs),
            "counting_system": asdict(self.counting_system)
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """Load settings from a dictionary"""
        if "game_rules" in data:
            self.game_rules = GameRules(**data["game_rules"])
        if "betting_limits" in data:
            self.betting_limits = BettingLimits(**data["betting_limits"])
        if "shoe_config" in data:
            self.shoe_config = ShoeConfiguration(**data["shoe_config"])
        if "practice_modes" in data:
            self.practice_modes = PracticeModes(**data["practice_modes"])
        if "display_prefs" in data:
            self.display_prefs = DisplayPreferences(**data["display_prefs"])
        if "counting_system" in data:
            self.counting_system = CountingSystem(**data["counting_system"])
    
    def save(self) -> bool:
        """Save settings to JSON file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def load(self) -> bool:
        """Load settings from JSON file"""
        if not os.path.exists(self.settings_file):
            return False
            
        try:
            with open(self.settings_file, 'r') as f:
                data = json.load(f)
            self.from_dict(data)
            return True
        except Exception as e:
            print(f"Error loading settings: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.game_rules = GameRules()
        self.betting_limits = BettingLimits()
        self.shoe_config = ShoeConfiguration()
        self.practice_modes = PracticeModes()
        self.display_prefs = DisplayPreferences()
        self.counting_system = CountingSystem()
    
    def get_dealer_stand_value(self) -> int:
        """Get the dealer stand value based on soft 17 rule"""
        return self.game_rules.dealer_stand_value
    
    def dealer_must_hit(self, value: int, is_soft: bool) -> bool:
        """Determine if dealer must hit based on rules"""
        if value < 17:
            return True
        if value == 17 and is_soft and not self.game_rules.dealer_stand_soft_17:
            return True
        return False
    
    def validate(self) -> List[str]:
        """Validate settings and return any errors"""
        errors = []
        
        # Validate betting limits
        if self.betting_limits.min_bet < 1:
            errors.append("Minimum bet must be at least $1")
        if self.betting_limits.max_bet < self.betting_limits.min_bet:
            errors.append("Maximum bet must be greater than minimum bet")
        if self.betting_limits.default_bet < self.betting_limits.min_bet:
            errors.append("Default bet must be at least minimum bet")
        if self.betting_limits.default_bet > self.betting_limits.max_bet:
            errors.append("Default bet cannot exceed maximum bet")
            
        # Validate shoe configuration
        if self.shoe_config.num_decks < 1 or self.shoe_config.num_decks > 8:
            errors.append("Number of decks must be between 1 and 8")
        if self.shoe_config.penetration < 0.5 or self.shoe_config.penetration > 0.9:
            errors.append("Penetration must be between 50% and 90%")
            
        # Validate game rules
        if self.game_rules.blackjack_payout < 1.0:
            errors.append("Blackjack payout must be at least 1:1")
        if self.game_rules.max_splits < 0 or self.game_rules.max_splits > 4:
            errors.append("Max splits must be between 0 and 4")
            
        # Validate practice modes
        if self.practice_modes.auto_deal_delay < 0.5 or self.practice_modes.auto_deal_delay > 10:
            errors.append("Auto-deal delay must be between 0.5 and 10 seconds")
            
        return errors

# Global settings instance
settings = Settings()