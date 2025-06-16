"""Card counting logic and calculations"""

from typing import List
from game_engine import Card, Shoe
from config import HI_LO_VALUES

class CardCounter:
    """Implements Hi-Lo card counting system"""
    
    def __init__(self):
        self.running_count = 0
        self.cards_seen = 0
        self.starting_decks = 6
        
    def reset(self):
        """Reset count for new shoe"""
        self.running_count = 0
        self.cards_seen = 0
    
    def update_count(self, card: Card):
        """Update running count based on card seen"""
        self.running_count += card.count_value
        self.cards_seen += 1
    
    def update_count_multiple(self, cards: List[Card]):
        """Update count for multiple cards at once"""
        for card in cards:
            self.update_count(card)
    
    def get_true_count(self, cards_remaining: int) -> float:
        """Calculate true count based on decks remaining"""
        if cards_remaining <= 0:
            return 0.0
            
        decks_remaining = cards_remaining / 52
        if decks_remaining < 0.5:  # Avoid division by very small numbers
            decks_remaining = 0.5
            
        return self.running_count / decks_remaining
    
    def get_running_count(self) -> int:
        """Get current running count"""
        return self.running_count

class CountingSystem:
    """Base class for different counting systems (for future expansion)"""
    
    def __init__(self, name: str):
        self.name = name
        self.card_values = {}
    
    def get_count_value(self, card: Card) -> int:
        """Get count value for a card"""
        return self.card_values.get(card.rank, 0)

class HiLoSystem(CountingSystem):
    """Standard Hi-Lo counting system"""
    
    def __init__(self):
        super().__init__("Hi-Lo")
        self.card_values = HI_LO_VALUES

class CountingStats:
    """Track counting accuracy and performance"""
    
    def __init__(self):
        self.correct_counts = 0
        self.total_counts = 0
        self.count_history = []
    
    def record_count(self, actual_count: int, player_count: int):
        """Record a count for accuracy tracking"""
        is_correct = actual_count == player_count
        self.total_counts += 1
        if is_correct:
            self.correct_counts += 1
        
        self.count_history.append({
            'actual': actual_count,
            'player': player_count,
            'correct': is_correct
        })
    
    def get_accuracy(self) -> float:
        """Calculate counting accuracy percentage"""
        if self.total_counts == 0:
            return 0.0
        return (self.correct_counts / self.total_counts) * 100
    
    def reset_stats(self):
        """Reset counting statistics"""
        self.correct_counts = 0
        self.total_counts = 0
        self.count_history = []