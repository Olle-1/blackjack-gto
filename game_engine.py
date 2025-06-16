"""Core game engine - handles all game logic without UI dependencies"""

import random
from typing import List, Tuple, Optional, Dict
from config import *

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
    
    def __init__(self, num_decks: int = DECKS_IN_SHOE):
        self.num_decks = num_decks
        self.cards: List[Card] = []
        self.dealt_count = 0
        self.penetration_cards = int(num_decks * 52 * (1 - DEFAULT_PENETRATION))
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
        """Determine if dealer must hit based on standard rules"""
        if hand.value < DEALER_STAND_ON:
            return True
        # Some variations have dealer hit on soft 17
        # For now, we'll use standard rules (stand on all 17s)
        return False
    
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
            return ("Blackjack!", 1.0 + BLACKJACK_PAYOUT)  # 3:2 payout
        
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
        self.player_hand: Optional[Hand] = None
        self.dealer_hand: Optional[Hand] = None
        self.current_bet = DEFAULT_BET
        self.bankroll = DEFAULT_BANKROLL
        self.hands_played = 0
        self.phase = "betting"  # betting, playing, dealer_turn, complete
        
        # Session statistics
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.total_wagered = 0.0
    
    def start_new_hand(self, bet_amount: int):
        """Start a new hand with the specified bet"""
        if self.shoe.needs_shuffle:
            self.shoe.shuffle()
        
        self.current_bet = bet_amount
        self.player_hand = Hand()
        self.dealer_hand = Hand(is_dealer=True)
        
        # Deal initial cards (player, dealer, player, dealer)
        self.player_hand.add_card(self.shoe.deal_card())
        self.dealer_hand.add_card(self.shoe.deal_card())
        self.player_hand.add_card(self.shoe.deal_card())
        self.dealer_hand.add_card(self.shoe.deal_card())
        
        self.phase = "playing"
        self.hands_played += 1
        
        # Check for blackjacks
        if self.player_hand.is_blackjack or self.dealer_hand.is_blackjack:
            self.phase = "complete"
    
    def player_hit(self) -> bool:
        """Player takes a card. Returns False if bust."""
        if self.phase != "playing":
            return False
            
        self.player_hand.add_card(self.shoe.deal_card())
        
        if self.player_hand.is_bust:
            self.phase = "complete"
            return False
        return True
    
    def player_stand(self):
        """Player stands, dealer's turn"""
        if self.phase != "playing":
            return
            
        self.player_hand.stood = True
        self.phase = "dealer_turn"
        self.play_dealer_hand()
    
    def player_double(self) -> bool:
        """Player doubles down. Returns False if not allowed."""
        if self.phase != "playing" or not self.player_hand.can_double():
            return False
        
        # Double the bet (ensure bankroll can cover it)
        if self.bankroll < self.current_bet:
            return False
            
        self.current_bet *= 2
        self.player_hand.doubled = True
        
        # Take exactly one card and stand
        self.player_hand.add_card(self.shoe.deal_card())
        
        if not self.player_hand.is_bust:
            self.phase = "dealer_turn"
            self.play_dealer_hand()
        else:
            self.phase = "complete"
        
        return True
    
    def play_dealer_hand(self):
        """Play out the dealer's hand according to house rules"""
        while GameRules.dealer_must_hit(self.dealer_hand):
            self.dealer_hand.add_card(self.shoe.deal_card())
        
        self.phase = "complete"
    
    def complete_hand(self) -> Tuple[str, float]:
        """Complete the hand and update bankroll"""
        outcome, payout_mult = GameRules.get_hand_outcome(
            self.player_hand, self.dealer_hand
        )
        
        # Update bankroll
        winnings = self.current_bet * payout_mult
        self.bankroll = self.bankroll - self.current_bet + winnings
        profit = winnings - self.current_bet
        
        # Update statistics
        self.total_wagered += self.current_bet
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