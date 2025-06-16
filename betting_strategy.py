"""Betting strategy implementations for different approaches"""

from typing import Dict, Optional
from settings import settings
from ev_calculator import EVCalculator

class BettingStrategyCalculator:
    """Calculate optimal bet sizes based on different strategies"""
    
    def __init__(self, ev_calculator: EVCalculator):
        self.ev_calculator = ev_calculator
        
    def calculate_bet_size(self, bankroll: float, true_count: float, 
                          current_bet: float) -> float:
        """Calculate recommended bet size based on current strategy"""
        strategy = settings.betting_limits.betting_strategy
        
        if strategy == "flat":
            return self._flat_betting(current_bet)
        elif strategy == "spread":
            return self._spread_betting(bankroll, true_count, current_bet)
        elif strategy == "kelly":
            return self._kelly_betting(bankroll, true_count)
        else:
            return current_bet
    
    def _flat_betting(self, current_bet: float) -> float:
        """Flat betting - always bet the same amount"""
        return settings.betting_limits.default_bet
    
    def _spread_betting(self, bankroll: float, true_count: float, 
                       current_bet: float) -> float:
        """Spread betting based on true count"""
        min_bet = settings.betting_limits.min_bet
        max_bet = settings.betting_limits.max_bet
        start_count = settings.betting_limits.spread_start_count
        min_multiplier = settings.betting_limits.spread_min_multiplier
        max_multiplier = settings.betting_limits.spread_max_multiplier
        
        # If count is below start threshold, bet minimum
        if true_count < start_count:
            return min_bet
        
        # Calculate multiplier based on count
        # Linear scaling from min to max multiplier
        count_range = 5.0 - start_count  # Max count range (5 - start)
        effective_count = min(true_count - start_count, count_range)
        
        # Calculate multiplier
        multiplier_range = max_multiplier - min_multiplier
        multiplier = min_multiplier + (effective_count / count_range) * multiplier_range
        
        # Calculate bet size
        suggested_bet = min_bet * multiplier
        
        # Ensure bet is within limits and bankroll
        suggested_bet = max(min_bet, min(max_bet, suggested_bet))
        suggested_bet = min(suggested_bet, bankroll * 0.1)  # Max 10% of bankroll
        
        return int(suggested_bet)
    
    def _kelly_betting(self, bankroll: float, true_count: float) -> float:
        """Kelly Criterion betting"""
        min_bet = settings.betting_limits.min_bet
        max_bet = settings.betting_limits.max_bet
        kelly_fraction = settings.betting_limits.kelly_fraction
        
        # Calculate player edge
        edge = self.ev_calculator.get_player_edge(true_count) / 100.0
        
        # Only bet when we have an edge
        if edge <= 0:
            return min_bet
        
        # Kelly formula: edge / odds (for even money bets, odds = 1)
        kelly_bet = bankroll * edge * kelly_fraction
        
        # Ensure bet is within limits
        kelly_bet = max(min_bet, min(max_bet, kelly_bet))
        kelly_bet = min(kelly_bet, bankroll * 0.2)  # Max 20% of bankroll for safety
        
        return int(kelly_bet)
    
    def get_strategy_description(self) -> str:
        """Get description of current betting strategy"""
        strategy = settings.betting_limits.betting_strategy
        
        if strategy == "flat":
            return f"Flat betting ${settings.betting_limits.default_bet} every hand"
        elif strategy == "spread":
            min_mult = settings.betting_limits.spread_min_multiplier
            max_mult = settings.betting_limits.spread_max_multiplier
            start = settings.betting_limits.spread_start_count
            return f"Spread betting {min_mult}x-{max_mult}x starting at count +{start}"
        elif strategy == "kelly":
            fraction = settings.betting_limits.kelly_fraction
            return f"Kelly Criterion betting ({fraction*100:.0f}% Kelly)"
        else:
            return "Unknown betting strategy"
    
    def should_show_bet_suggestion(self, current_bet: float, suggested_bet: float) -> bool:
        """Determine if bet suggestion should be shown"""
        # Show suggestion if it differs significantly from current bet
        return abs(current_bet - suggested_bet) >= settings.betting_limits.bet_increment
    
    def get_bet_suggestion_text(self, current_bet: float, suggested_bet: float, 
                               true_count: float) -> str:
        """Get formatted bet suggestion text"""
        if not self.should_show_bet_suggestion(current_bet, suggested_bet):
            return ""
        
        strategy = settings.betting_limits.betting_strategy
        
        if strategy == "flat":
            return f"Flat betting: ${suggested_bet:.0f}"
        elif strategy == "spread":
            return f"Count +{true_count:.1f}: Suggest ${suggested_bet:.0f}"
        elif strategy == "kelly":
            return f"Kelly suggests: ${suggested_bet:.0f}"
        else:
            return f"Suggested bet: ${suggested_bet:.0f}"

class BettingDisplay:
    """Display betting strategy information in the UI"""
    
    def __init__(self, parent, betting_calculator: BettingStrategyCalculator):
        self.parent = parent
        self.betting_calculator = betting_calculator
        self.suggestion_label = None
        self._create_display()
    
    def _create_display(self):
        """Create betting strategy display elements"""
        # This would be integrated into the main UI
        pass
    
    def update_suggestion(self, current_bet: float, bankroll: float, 
                         true_count: float):
        """Update betting suggestion display"""
        suggested_bet = self.betting_calculator.calculate_bet_size(
            bankroll, true_count, current_bet
        )
        
        suggestion_text = self.betting_calculator.get_bet_suggestion_text(
            current_bet, suggested_bet, true_count
        )
        
        # This would update the UI label
        if self.suggestion_label and suggestion_text:
            self.suggestion_label.config(text=suggestion_text)
        
        return suggested_bet