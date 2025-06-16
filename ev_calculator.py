"""Expected Value (EV) calculation engine"""

from typing import Dict, List, Tuple
from config import BASE_HOUSE_EDGE, TRUE_COUNT_ADVANTAGE

class EVCalculator:
    """Calculates expected value based on count and game conditions"""
    
    def __init__(self):
        self.base_house_edge = BASE_HOUSE_EDGE
        self.true_count_advantage = TRUE_COUNT_ADVANTAGE
        self.session_stats = SessionStats()
    
    def calculate_ev(self, true_count: float, bet_size: float) -> float:
        """
        Calculate expected value for a bet
        Each true count point adds approximately 0.5% to player advantage
        """
        # Calculate player edge
        count_advantage = true_count * self.true_count_advantage
        total_edge = self.base_house_edge + count_advantage
        
        # EV = bet_size * edge
        return bet_size * total_edge
    
    def get_player_edge(self, true_count: float) -> float:
        """Get player edge as a percentage"""
        count_advantage = true_count * self.true_count_advantage
        return (self.base_house_edge + count_advantage) * 100
    
    def calculate_kelly_bet(self, bankroll: float, true_count: float, 
                          kelly_fraction: float = 0.25) -> float:
        """
        Calculate optimal bet size using Kelly Criterion
        Using fractional Kelly (default 25%) for variance reduction
        """
        edge = self.base_house_edge + (true_count * self.true_count_advantage)
        
        # Only bet when we have an edge
        if edge <= 0:
            return 0
        
        # Kelly formula: edge / odds
        # For even money bets, odds = 1
        kelly_bet = bankroll * edge * kelly_fraction
        
        return max(0, kelly_bet)
    
    def update_session_ev(self, bet_size: float, true_count: float, 
                         outcome: float):
        """Update session EV tracking"""
        expected = self.calculate_ev(true_count, bet_size)
        self.session_stats.add_hand(bet_size, expected, outcome)

class SessionStats:
    """Track session statistics for EV analysis"""
    
    def __init__(self):
        self.hands_played = 0
        self.total_wagered = 0.0
        self.total_expected_ev = 0.0
        self.total_actual_result = 0.0
        self.results_by_count: Dict[int, List[float]] = {}
    
    def add_hand(self, bet_size: float, expected_ev: float, 
                 actual_result: float):
        """Record a hand's results"""
        self.hands_played += 1
        self.total_wagered += bet_size
        self.total_expected_ev += expected_ev
        self.total_actual_result += actual_result
    
    def get_expected_ev_percentage(self) -> float:
        """Get expected EV as percentage of total wagered"""
        if self.total_wagered == 0:
            return 0.0
        return (self.total_expected_ev / self.total_wagered) * 100
    
    def get_actual_ev_percentage(self) -> float:
        """Get actual results as percentage of total wagered"""
        if self.total_wagered == 0:
            return 0.0
        return (self.total_actual_result / self.total_wagered) * 100
    
    def get_session_summary(self) -> Dict:
        """Get complete session EV summary"""
        return {
            'hands_played': self.hands_played,
            'total_wagered': self.total_wagered,
            'expected_ev': self.total_expected_ev,
            'actual_result': self.total_actual_result,
            'expected_ev_percentage': self.get_expected_ev_percentage(),
            'actual_ev_percentage': self.get_actual_ev_percentage(),
            'variance': self.get_variance()
        }
    
    def get_variance(self) -> float:
        """Calculate variance from expected value"""
        return self.total_actual_result - self.total_expected_ev
    
    def reset(self):
        """Reset session statistics"""
        self.hands_played = 0
        self.total_wagered = 0.0
        self.total_expected_ev = 0.0
        self.total_actual_result = 0.0
        self.results_by_count.clear()

class BettingStrategy:
    """Different betting strategies based on count"""
    
    @staticmethod
    def flat_bet(base_bet: float, true_count: float) -> float:
        """Always bet the same amount regardless of count"""
        return base_bet
    
    @staticmethod
    def spread_betting(min_bet: float, max_bet: float, true_count: float,
                      spread_start: float = 1.0) -> float:
        """
        Vary bet size based on true count
        Start spreading at true_count >= spread_start
        """
        if true_count < spread_start:
            return min_bet
        
        # Linear spread from min to max based on count
        # Max out at true count of 5
        spread_range = min(true_count - spread_start, 4.0) / 4.0
        bet_range = max_bet - min_bet
        
        return min_bet + (bet_range * spread_range)
    
    @staticmethod
    def wonging_bet(min_bet: float, true_count: float, 
                   wong_in_count: float = 1.0) -> float:
        """
        Wong in/out strategy - only bet when count is favorable
        """
        if true_count < wong_in_count:
            return 0  # Sit out
        return min_bet