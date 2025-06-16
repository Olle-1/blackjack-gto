"""Core game engine - handles all game logic without UI dependencies"""

import random
from typing import List, Tuple, Optional, Dict
from config import *
from settings import settings

class Card:
    """Represents a single playing card"""
    
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        self._value = self._calculate_value()
        self.count_value = HI_LO_VALUES.get(rank, 0)
    
    def _calculate_value(self) -> int:
        """Calculate blackjack value of the card"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Aces start as 11, Hand class handles soft/hard logic
        else:
            return int(self.rank)
    
    @property
    def value(self) -> int:
        return self._value
    
    def __str__(self) -> str:
        return f"{self.rank}{self.suit[0]}"
    
    def __repr__(self) -> str:
        return f"Card({self.rank}, {self.suit})"

class Shoe:
    """Manages a multi-deck shoe with penetration tracking"""
    
    def __init__(self, num_decks: int = None):
        self.num_decks = num_decks or settings.shoe_config.num_decks
        self.cards: List[Card] = []
        self.dealt_count = 0
        self.penetration_cards = int(self.num_decks * 52 * (1 - settings.shoe_config.penetration))
        self.needs_shuffle = False
        self._create_and_shuffle()
    
    def _create_and_shuffle(self):
        """Create a new shoe and shuffle it"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        self.cards = []
        for _ in range(self.num_decks):
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(rank, suit))
        
        random.shuffle(self.cards)
        self.dealt_count = 0
        self.needs_shuffle = False
        
        # Burn first card if enabled
        if settings.shoe_config.burn_card and self.cards:
            self.cards.pop(0)
    
    def deal_card(self) -> Optional[Card]:
        """Deal a card from the shoe"""
        if not self.cards:
            return None
            
        card = self.cards.pop(0)
        self.dealt_count += 1
        
        # Check if we've reached penetration point
        if self.dealt_count >= self.penetration_cards:
            self.needs_shuffle = True
            
        return card
    
    def cards_remaining(self) -> int:
        """Get number of cards remaining in shoe"""
        return len(self.cards)
    
    def decks_remaining(self) -> float:
        """Calculate approximate decks remaining"""
        return self.cards_remaining() / 52
    
    def shuffle(self):
        """Shuffle the shoe (typically called between hands)"""
        self._create_and_shuffle()

class Hand:
    """Represents a blackjack hand with value calculation"""
    
    def __init__(self, is_dealer: bool = False):
        self.cards: List[Card] = []
        self.is_dealer = is_dealer
        self._value = 0
        self._soft = False
        self.stood = False
        self.doubled = False
        self.is_blackjack = False
    
    def add_card(self, card: Card):
        """Add a card to the hand and recalculate value"""
        self.cards.append(card)
        self._calculate_value()
        
        # Check for blackjack (only on initial 2 cards)
        if len(self.cards) == 2 and self._value == 21:
            self.is_blackjack = True
    
    def _calculate_value(self):
        """Calculate hand value, handling soft/hard aces"""
        total = 0
        aces = 0
        
        # Count all cards and track aces
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
            total += card.value
        
        # Adjust for aces if busted
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        self._value = total
        self._soft = (aces > 0 and total <= 21)
    
    @property
    def value(self) -> int:
        return self._value
    
    @property
    def is_soft(self) -> bool:
        return self._soft
    
    @property
    def is_bust(self) -> bool:
        return self._value > 21
    
    def can_split(self) -> bool:
        """Check if hand can be split (only for initial 2 cards of same rank)"""
        if len(self.cards) != 2:
            return False
        return self.cards[0].rank == self.cards[1].rank
    
    def can_double(self) -> bool:
        """Check if hand can be doubled (only on initial 2 cards)"""
        return len(self.cards) == 2 and not self.doubled

class GameRules:
    """Enforces blackjack game rules and determines outcomes"""
    
    @staticmethod
    def dealer_must_hit(hand: Hand) -> bool:
        """Determine if dealer must hit based on game rules"""
        return settings.dealer_must_hit(hand.value, hand.is_soft)
    
    @staticmethod
    def get_hand_outcome(player_hand: Hand, dealer_hand: Hand) -> Tuple[str, float]:
        """
        Determine outcome of a hand
        Returns: (outcome_string, payout_multiplier)
        """
        # Check for blackjacks first
        player_bj = player_hand.is_blackjack
        dealer_bj = dealer_hand.is_blackjack
        
        if player_bj and dealer_bj:
            return ("Push", 1.0)  # Return original bet
        elif dealer_bj:
            return ("Dealer Blackjack", 0.0)  # Lose bet
        elif player_bj:
            return ("Blackjack!", 1.0 + settings.game_rules.blackjack_payout)  # Configurable payout
        
        # Check for busts
        if player_hand.is_bust:
            return ("Bust", 0.0)
        elif dealer_hand.is_bust:
            return ("Dealer Bust", 2.0)  # Win pays 1:1
        
        # Compare values
        if player_hand.value > dealer_hand.value:
            return ("Win", 2.0)
        elif player_hand.value < dealer_hand.value:
            return ("Lose", 0.0)
        else:
            return ("Push", 1.0)

class GameState:
    """Manages the complete state of a blackjack game"""
    
    def __init__(self):
        self.shoe = Shoe()
        self.player_hands: List[Hand] = []  # List of player hands (for splits)
        self.dealer_hand: Optional[Hand] = None
        self.hand_bets: List[int] = []  # Bet amount for each hand
        self.active_hand_index: int = 0  # Which hand is currently being played
        self.current_bet = settings.betting_limits.default_bet
        self.bankroll = settings.betting_limits.default_bankroll
        self.hands_played = 0
        self.phase = "betting"  # betting, playing, dealer_turn, complete
        
        # Session statistics
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.total_wagered = 0.0
    
    @property
    def player_hand(self) -> Optional[Hand]:
        """Backwards compatibility - returns current active hand"""
        if self.player_hands:
            if self.active_hand_index < len(self.player_hands):
                return self.player_hands[self.active_hand_index]
            return self.player_hands[0]  # Fallback to first hand
        return None
    
    @player_hand.setter
    def player_hand(self, hand: Hand):
        """Backwards compatibility - sets as first hand"""
        self.player_hands = [hand] if hand else []
        self.hand_bets = [self.current_bet] if hand else []
        self.active_hand_index = 0
    
    def start_new_hand(self, bet_amount: int):
        """Start a new hand with the specified bet"""
        if self.shoe.needs_shuffle:
            self.shoe.shuffle()
        
        self.current_bet = bet_amount
        
        # Initialize with single hand
        initial_hand = Hand()
        self.player_hands = [initial_hand]
        self.hand_bets = [bet_amount]
        self.active_hand_index = 0
        self.dealer_hand = Hand(is_dealer=True)
        
        # Deal initial cards (player, dealer, player, dealer)
        self.player_hands[0].add_card(self.shoe.deal_card())
        self.dealer_hand.add_card(self.shoe.deal_card())
        self.player_hands[0].add_card(self.shoe.deal_card())
        self.dealer_hand.add_card(self.shoe.deal_card())
        
        self.phase = "playing"
        self.hands_played += 1
        
        # Check for blackjacks
        if self.player_hands[0].is_blackjack or self.dealer_hand.is_blackjack:
            self.phase = "complete"
    
    def player_hit(self) -> bool:
        """Player takes a card. Returns False if bust."""
        return self.player_hit_hand(self.active_hand_index)
    
    def player_hit_hand(self, hand_index: int) -> bool:
        """Player takes a card on specific hand. Returns False if bust."""
        if self.phase != "playing" or hand_index >= len(self.player_hands):
            return False
            
        hand = self.player_hands[hand_index]
        hand.add_card(self.shoe.deal_card())
        
        # Check if this hand is done (bust or 21)
        if hand.is_bust or hand.value == 21:
            return self._advance_to_next_hand()
        
        return True
    
    def player_stand(self):
        """Player stands current hand"""
        if self.phase != "playing":
            return
            
        # Mark current hand as stood
        if self.active_hand_index < len(self.player_hands):
            self.player_hands[self.active_hand_index].stood = True
        
        # Move to next hand or finish
        self._advance_to_next_hand()
    
    def player_double(self) -> bool:
        """Player doubles down. Returns False if not allowed."""
        if self.phase != "playing":
            return False
        
        hand = self.player_hands[self.active_hand_index]
        current_hand_bet = self.hand_bets[self.active_hand_index]
        
        if not hand.can_double():
            return False
        
        # Double the bet (ensure bankroll can cover it)
        if self.bankroll < current_hand_bet:
            return False
            
        self.hand_bets[self.active_hand_index] *= 2
        hand.doubled = True
        
        # Take exactly one card and stand
        hand.add_card(self.shoe.deal_card())
        
        # This hand is now complete, move to next hand
        self._advance_to_next_hand()
        
        return True
    
    def player_split(self) -> bool:
        """Player splits current hand. Returns False if not allowed."""
        if self.phase != "playing":
            return False
        
        hand = self.player_hands[self.active_hand_index]
        current_hand_bet = self.hand_bets[self.active_hand_index]
        
        # Check if split is allowed
        if not hand.can_split():
            return False
        
        # Check max splits limit
        if len(self.player_hands) >= settings.game_rules.max_splits + 1:
            return False
        
        # Check bankroll for additional bet
        if self.bankroll < current_hand_bet:
            return False
        
        # Perform the split
        card1, card2 = hand.cards[0], hand.cards[1]
        
        # Create new hand with second card
        new_hand = Hand()
        new_hand.add_card(card2)
        
        # Original hand keeps first card
        hand.cards = [card1]
        hand._calculate_value()
        hand.is_blackjack = False  # Split hands can't be blackjack
        
        # Insert new hand after current one
        self.player_hands.insert(self.active_hand_index + 1, new_hand)
        self.hand_bets.insert(self.active_hand_index + 1, current_hand_bet)
        
        # Deal one card to each hand
        hand.add_card(self.shoe.deal_card())
        new_hand.add_card(self.shoe.deal_card())
        
        # Special rule for split aces - only get one card each
        if card1.rank == 'A' and settings.game_rules.split_aces_one_card:
            # Both hands are complete, move to next non-ace hand or dealer
            self._advance_to_next_hand()
        
        return True
    
    def _advance_to_next_hand(self) -> bool:
        """Advance to next hand or finish all hands. Returns True if continuing play."""
        self.active_hand_index += 1
        
        # Check if there are more hands to play
        if self.active_hand_index < len(self.player_hands):
            return True
        
        # All hands complete, dealer plays
        self.phase = "dealer_turn"
        self.play_dealer_hand()
        return False
    
    def can_split_current_hand(self) -> bool:
        """Check if current active hand can be split"""
        if self.phase != "playing" or self.active_hand_index >= len(self.player_hands):
            return False
        
        hand = self.player_hands[self.active_hand_index]
        
        # Basic split requirements
        if not hand.can_split():
            return False
        
        # Max splits limit
        if len(self.player_hands) >= settings.game_rules.max_splits + 1:
            return False
        
        # Bankroll check
        current_hand_bet = self.hand_bets[self.active_hand_index]
        if self.bankroll < current_hand_bet:
            return False
        
        return True
    
    def play_dealer_hand(self):
        """Play out the dealer's hand according to house rules"""
        while GameRules.dealer_must_hit(self.dealer_hand):
            self.dealer_hand.add_card(self.shoe.deal_card())
        
        self.phase = "complete"
    
    def complete_hand(self) -> Tuple[str, float]:
        """Complete all hands and update bankroll - returns summary of first hand for backwards compatibility"""
        if not self.player_hands:
            return "No hands", 0.0
        
        # For backwards compatibility, if only one hand, use old logic
        if len(self.player_hands) == 1:
            return self._complete_single_hand(0)
        
        # Multiple hands - process all and return summary
        return self._complete_all_hands()
    
    def _complete_single_hand(self, hand_index: int) -> Tuple[str, float]:
        """Complete a single hand (backwards compatibility)"""
        hand = self.player_hands[hand_index]
        bet = self.hand_bets[hand_index]
        
        outcome, payout_mult = GameRules.get_hand_outcome(hand, self.dealer_hand)
        
        # Update bankroll
        winnings = bet * payout_mult
        self.bankroll = self.bankroll - bet + winnings
        profit = winnings - bet
        
        # Update statistics
        self.total_wagered += bet
        if outcome == "Push":
            self.pushes += 1
        elif outcome == "Blackjack!":
            self.wins += 1
            self.blackjacks += 1
        elif payout_mult > 1.0:  # Win
            self.wins += 1
        else:  # Loss
            self.losses += 1
        
        return outcome, profit
    
    def _complete_all_hands(self) -> Tuple[str, float]:
        """Complete all hands and return summary"""
        total_profit = 0.0
        wins = 0
        losses = 0
        pushes = 0
        hand_results = []
        
        for i, (hand, bet) in enumerate(zip(self.player_hands, self.hand_bets)):
            outcome, payout_mult = GameRules.get_hand_outcome(hand, self.dealer_hand)
            
            # Calculate winnings for this hand
            winnings = bet * payout_mult
            profit = winnings - bet
            total_profit += profit
            
            # Track results
            hand_results.append((i+1, outcome, profit))
            
            # Update statistics
            self.total_wagered += bet
            if outcome == "Push":
                self.pushes += 1
                pushes += 1
            elif outcome == "Blackjack!":
                self.wins += 1
                self.blackjacks += 1
                wins += 1
            elif payout_mult > 1.0:  # Win
                self.wins += 1
                wins += 1
            else:  # Loss
                self.losses += 1
                losses += 1
        
        # Update bankroll with total
        self.bankroll += total_profit
        
        # Create summary message
        if wins == len(self.player_hands):
            summary = f"All {len(self.player_hands)} hands won!"
        elif losses == len(self.player_hands):
            summary = f"All {len(self.player_hands)} hands lost"
        elif pushes == len(self.player_hands):
            summary = f"All {len(self.player_hands)} hands pushed"
        else:
            summary = f"{wins}W/{losses}L/{pushes}P"
        
        return summary, total_profit
    
    def get_hand_results(self) -> List[Tuple[str, float]]:
        """Get detailed results for each hand"""
        results = []
        for i, (hand, bet) in enumerate(zip(self.player_hands, self.hand_bets)):
            outcome, payout_mult = GameRules.get_hand_outcome(hand, self.dealer_hand)
            winnings = bet * payout_mult
            profit = winnings - bet
            results.append((outcome, profit))
        return results
    
    def get_win_percentage(self) -> float:
        """Get win percentage (excluding pushes)"""
        total_decisions = self.wins + self.losses
        if total_decisions == 0:
            return 0.0
        return (self.wins / total_decisions) * 100
    
    def get_session_stats(self) -> Dict:
        """Get complete session statistics"""
        return {
            'hands_played': self.hands_played,
            'wins': self.wins,
            'losses': self.losses,
            'pushes': self.pushes,
            'blackjacks': self.blackjacks,
            'win_percentage': self.get_win_percentage(),
            'total_wagered': self.total_wagered,
            'profit_loss': self.bankroll - DEFAULT_BANKROLL,
            'average_bet': self.total_wagered / self.hands_played if self.hands_played > 0 else 0
        }