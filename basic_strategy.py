"""Basic strategy engine for blackjack"""

from typing import Optional, Dict, Tuple, List
from game_engine import Hand, Card
from settings import settings

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
            12:     ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # A,A (when can't split)
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
                          can_double: bool = True, can_split: bool = True,
                          game_state=None) -> str:
        """Get the optimal action based on basic strategy"""
        
        # Get dealer upcard index
        dealer_idx = self.dealer_upcard_index.get(dealer_upcard.rank, 8)
        
        # Check for pairs first (if splitting is allowed)
        if can_split and player_hand.can_split():
            pair_rank = player_hand.cards[0].rank
            split_action = self._get_split_action(pair_rank, dealer_idx, game_state)
            
            # Return the split action (could be 'P' for split or alternative action)
            if split_action:
                return split_action
        
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
    
    def _get_split_action(self, pair_rank: str, dealer_idx: int, game_state=None) -> str:
        """Get split action considering game rules and current state"""
        # Get base strategy action
        base_action = self.pair_table[pair_rank][dealer_idx]
        
        # Strategy recommends split - check if game allows it
        if base_action == 'P':
            if game_state:
                # Check split limits
                if hasattr(game_state, 'player_hands') and hasattr(game_state, 'can_split_current_hand'):
                    if not game_state.can_split_current_hand():
                        # Can't split due to limits/bankroll, treat as regular hand
                        return self._get_non_split_action(pair_rank, dealer_idx)
                
                # Check rule variations that affect strategy
                if hasattr(game_state, 'settings') or 'settings' in globals():
                    from settings import settings
                    
                    # Double after split (DAS) rule affects some pairs
                    if not settings.game_rules.double_after_split:
                        # Without DAS, some pairs become less favorable to split
                        if pair_rank == '4' and dealer_idx in [3, 4]:  # 4-4 vs 5-6
                            return 'H'  # Hit instead of split without DAS
                        if pair_rank == '6' and dealer_idx in [1]:     # 6-6 vs 3  
                            return 'H'  # Hit instead of split without DAS
            
            # Default: return the recommended split
            return 'P'
        
        # Strategy doesn't recommend split, return the base action
        return base_action
    
    def _get_non_split_action(self, pair_rank: str, dealer_idx: int) -> str:
        """Get action for pair when splitting is not allowed/recommended"""
        # Convert pair to hand value and get regular strategy
        pair_value = self._get_pair_value(pair_rank)
        
        if pair_rank == 'A':
            # A-A treated as soft 12 when can't split
            if 12 in self.soft_table:
                action = self.soft_table[12][dealer_idx]
                return self._convert_action(action, True)  # Assume can double
            else:
                return 'H'
        elif pair_value <= 21 and pair_value in self.hard_table:
            # Most pairs are hard hands when can't split
            action = self.hard_table[pair_value][dealer_idx]
            return self._convert_action(action, True)  # Assume can double
        else:
            return 'S'  # Default for high values or missing entries
    
    def _get_pair_value(self, pair_rank: str) -> int:
        """Get the total value of a pair"""
        if pair_rank == 'A':
            return 12  # A-A = 2 or 12, treat as soft 12
        elif pair_rank in ['J', 'Q', 'K']:
            return 20  # 10-value pairs
        else:
            return int(pair_rank) * 2


class StrategyTracker:
    """Tracks player adherence to basic strategy"""
    
    def __init__(self):
        self.decisions_made = 0
        self.correct_decisions = 0
        self.deviations = []
        self.strategy = BasicStrategy()
    
    def record_decision(self, player_hand: Hand, dealer_upcard: Card,
                       player_action: str, can_double: bool, can_split: bool,
                       game_state=None, hand_index: int = 0):
        """Record a player decision and check against basic strategy"""
        # Get optimal action with game state context
        optimal = self.strategy.get_optimal_action(
            player_hand, dealer_upcard, can_double, can_split, game_state
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
            # Record deviation with enhanced context
            deviation = {
                'hand_value': player_hand.value,
                'is_soft': player_hand.is_soft,
                'dealer_upcard': str(dealer_upcard),
                'player_action': player_action,
                'optimal_action': optimal_game_action,
                'cards': [str(card) for card in player_hand.cards],
                'hand_index': hand_index
            }
            
            # Add split context if relevant
            if game_state and hasattr(game_state, 'player_hands'):
                deviation['is_split_hand'] = len(game_state.player_hands) > 1
                deviation['total_hands'] = len(game_state.player_hands)
                deviation['is_pair'] = player_hand.can_split()
            
            self.deviations.append(deviation)
        
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