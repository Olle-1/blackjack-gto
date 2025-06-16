"""Basic strategy engine for blackjack"""

from typing import Optional, Dict, Tuple, List
from game_engine import Hand, Card

# Basic Strategy Actions
HIT = 'H'
STAND = 'S'
DOUBLE = 'D'  # Double if allowed, else hit
DOUBLE_STAND = 'Ds'  # Double if allowed, else stand
SPLIT = 'P'

class BasicStrategy:
    """Implements basic strategy for blackjack"""
    
    def __init__(self):
        # Hard totals table (player total vs dealer upcard)
        # Rows: Player hard total (5-21)
        # Columns: Dealer upcard (2-10, A)
        self.hard_table = {
            # Player  2    3    4    5    6    7    8    9   10    A
            5:      ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
            6:      ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
            7:      ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
            8:      ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
            9:      ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
            10:     ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
            11:     ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'],
            12:     ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
            13:     ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
            14:     ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
            15:     ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
            16:     ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
            17:     ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            18:     ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            19:     ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            20:     ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            21:     ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
        }
        
        # Soft totals table (player has ace counted as 11)
        # Rows: Player soft total (A,2 through A,9)
        # Columns: Dealer upcard (2-10, A)
        self.soft_table = {
            # Soft    2    3    4    5    6    7    8    9   10    A
            13:     ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A,2
            14:     ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A,3
            15:     ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A,4
            16:     ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A,5
            17:     ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A,6
            18:     ['S', 'Ds','Ds','Ds','Ds','S', 'S', 'H', 'H', 'H'],  # A,7
            19:     ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A,8
            20:     ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A,9
            21:     ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']   # A,10 (BJ)
        }
        
        # Pairs table (when to split)
        # Rows: Pair rank
        # Columns: Dealer upcard (2-10, A)
        self.pair_table = {
            # Pair    2    3    4    5    6    7    8    9   10    A
            '2':    ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],  # 2,2
            '3':    ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],  # 3,3
            '4':    ['H', 'H', 'H', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],  # 4,4
            '5':    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],  # 5,5 (never split)
            '6':    ['P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],  # 6,6
            '7':    ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],  # 7,7
            '8':    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # 8,8
            '9':    ['P', 'P', 'P', 'P', 'P', 'S', 'P', 'P', 'S', 'S'],  # 9,9
            '10':   ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 10,10
            'J':    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # J,J
            'Q':    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # Q,Q
            'K':    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # K,K
            'A':    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']   # A,A
        }
        
        # Convert dealer upcard to table index
        self.dealer_upcard_index = {
            '2': 0, '3': 1, '4': 2, '5': 3, '6': 4,
            '7': 5, '8': 6, '9': 7, '10': 8, 'J': 8, 'Q': 8, 'K': 8, 'A': 9
        }
    
    def get_optimal_action(self, player_hand: Hand, dealer_upcard: Card, 
                          can_double: bool = True, can_split: bool = True) -> str:
        """Get the optimal action based on basic strategy"""
        
        # Get dealer upcard index
        dealer_idx = self.dealer_upcard_index.get(dealer_upcard.rank, 8)
        
        # Check for pairs first (if splitting is allowed)
        if can_split and player_hand.can_split():
            pair_rank = player_hand.cards[0].rank
            action = self.pair_table[pair_rank][dealer_idx]
            
            # Only return the pair action if it's actually 'P' (split)
            # Otherwise, treat as regular hand (e.g., 5,5 or 10,10)
            if action == 'P':
                return action
        
        # Check for soft hands
        if player_hand.is_soft and player_hand.value <= 21:
            # Soft hands are only in the table for totals 13-21
            if player_hand.value >= 13:
                action = self.soft_table[player_hand.value][dealer_idx]
                return self._convert_action(action, can_double)
        
        # Hard hands
        if player_hand.value <= 21:
            # For hard hands less than 5, always hit
            if player_hand.value < 5:
                return HIT
            elif player_hand.value > 21:
                return STAND  # Already bust
            else:
                action = self.hard_table[player_hand.value][dealer_idx]
                return self._convert_action(action, can_double)
        
        return STAND  # Default for bust hands
    
    def _convert_action(self, action: str, can_double: bool) -> str:
        """Convert strategy action based on what's allowed"""
        if action == 'D' and not can_double:
            return HIT
        elif action == 'Ds' and not can_double:
            return STAND
        return action
    
    def action_to_game_action(self, action: str) -> str:
        """Convert strategy action to game action string"""
        action_map = {
            'H': 'hit',
            'S': 'stand',
            'D': 'double',
            'Ds': 'double',
            'P': 'split'
        }
        return action_map.get(action, 'stand')


class StrategyTracker:
    """Tracks player adherence to basic strategy"""
    
    def __init__(self):
        self.decisions_made = 0
        self.correct_decisions = 0
        self.deviations = []
        self.strategy = BasicStrategy()
    
    def record_decision(self, player_hand: Hand, dealer_upcard: Card,
                       player_action: str, can_double: bool, can_split: bool):
        """Record a player decision and check against basic strategy"""
        # Get optimal action
        optimal = self.strategy.get_optimal_action(
            player_hand, dealer_upcard, can_double, can_split
        )
        optimal_game_action = self.strategy.action_to_game_action(optimal)
        
        # Normalize player action
        action_map = {
            'hit': 'hit',
            'stand': 'stand',
            'double': 'double',
            'split': 'split'
        }
        normalized_action = action_map.get(player_action.lower(), player_action.lower())
        
        # Check if correct
        is_correct = normalized_action == optimal_game_action
        
        self.decisions_made += 1
        if is_correct:
            self.correct_decisions += 1
        else:
            # Record deviation
            self.deviations.append({
                'hand_value': player_hand.value,
                'is_soft': player_hand.is_soft,
                'dealer_upcard': str(dealer_upcard),
                'player_action': player_action,
                'optimal_action': optimal_game_action,
                'cards': [str(card) for card in player_hand.cards]
            })
        
        return is_correct, optimal_game_action
    
    def get_adherence_percentage(self) -> float:
        """Get percentage of correct decisions"""
        if self.decisions_made == 0:
            return 100.0
        return (self.correct_decisions / self.decisions_made) * 100
    
    def get_recent_deviations(self, count: int = 5) -> List[Dict]:
        """Get the most recent strategy deviations"""
        return self.deviations[-count:] if self.deviations else []
    
    def reset_tracking(self):
        """Reset tracking statistics"""
        self.decisions_made = 0
        self.correct_decisions = 0
        self.deviations = []
    
    def get_summary(self) -> Dict:
        """Get summary of strategy performance"""
        return {
            'total_decisions': self.decisions_made,
            'correct_decisions': self.correct_decisions,
            'adherence_percentage': self.get_adherence_percentage(),
            'total_deviations': len(self.deviations),
            'recent_deviations': self.get_recent_deviations()
        }