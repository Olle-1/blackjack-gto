"""Verify shoe creation and card dealing logic"""

from game_engine import Shoe, Card
from collections import Counter
from config import DECKS_IN_SHOE, HI_LO_VALUES

def verify_shoe_creation():
    """Verify that shoe is created correctly with all cards"""
    shoe = Shoe(num_decks=DECKS_IN_SHOE)
    
    print(f"Created shoe with {DECKS_IN_SHOE} decks")
    print(f"Total cards in shoe: {len(shoe.cards)}")
    print(f"Expected: {52 * DECKS_IN_SHOE} cards")
    print(f"Match: {len(shoe.cards) == 52 * DECKS_IN_SHOE}")
    print()
    
    # Count each rank
    rank_counter = Counter()
    suit_counter = Counter()
    
    for card in shoe.cards:
        rank_counter[card.rank] += 1
        suit_counter[card.suit] += 1
    
    print("Rank distribution:")
    for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
        count = rank_counter[rank]
        expected = 4 * DECKS_IN_SHOE  # 4 suits * number of decks
        print(f"  {rank}: {count} cards (expected: {expected}) - {'✓' if count == expected else '✗'}")
    
    print("\nSuit distribution:")
    for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
        count = suit_counter[suit]
        expected = 13 * DECKS_IN_SHOE  # 13 ranks * number of decks
        print(f"  {suit}: {count} cards (expected: {expected}) - {'✓' if count == expected else '✗'}")
    
    # Verify Hi-Lo count values
    print("\nHi-Lo count verification:")
    total_count = 0
    for card in shoe.cards:
        total_count += card.count_value
    print(f"Total Hi-Lo count of full shoe: {total_count} (should be 0 for balanced system)")
    
    # Test dealing and penetration
    print(f"\nPenetration test:")
    print(f"Penetration set to: {shoe.penetration_cards} cards")
    print(f"Will shuffle after dealing ~{shoe.penetration_cards / 52:.1f} decks")
    
    cards_dealt = 0
    while not shoe.needs_shuffle and shoe.cards:
        card = shoe.deal_card()
        cards_dealt += 1
    
    print(f"Dealt {cards_dealt} cards before shuffle needed")
    print(f"Cards remaining: {shoe.cards_remaining()}")
    print(f"Approximate decks dealt: {cards_dealt / 52:.1f}")
    print(f"Approximate decks remaining: {shoe.cards_remaining() / 52:.1f}")

def verify_card_dealing():
    """Verify cards are dealt properly and count is tracked"""
    shoe = Shoe(num_decks=DECKS_IN_SHOE)
    initial_count = len(shoe.cards)
    
    print("\nDealing test:")
    # Deal 10 cards
    dealt_cards = []
    for i in range(10):
        card = shoe.deal_card()
        dealt_cards.append(card)
        print(f"  Card {i+1}: {card} (count value: {card.count_value:+d})")
    
    print(f"\nCards remaining: {shoe.cards_remaining()} (started with {initial_count})")
    print(f"Cards dealt: {len(dealt_cards)}")
    print(f"Match: {initial_count - len(dealt_cards) == shoe.cards_remaining()}")
    
    # Calculate running count
    running_count = sum(card.count_value for card in dealt_cards)
    print(f"\nRunning count after 10 cards: {running_count:+d}")

if __name__ == "__main__":
    print("=== BLACKJACK SHOE VERIFICATION ===\n")
    verify_shoe_creation()
    verify_card_dealing()