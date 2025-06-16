"""Test basic strategy implementation"""

from basic_strategy import BasicStrategy
from game_engine import Card, Hand

def test_basic_strategy():
    """Test various basic strategy scenarios"""
    strategy = BasicStrategy()
    
    print("=== BASIC STRATEGY TEST ===\n")
    
    # Test hard hands
    print("HARD HANDS:")
    test_cases = [
        # (player_cards, dealer_upcard, expected_action, description)
        ([('10', 'hearts'), ('6', 'diamonds')], ('9', 'clubs'), 'H', "Hard 16 vs 9 should HIT"),
        ([('10', 'hearts'), ('7', 'diamonds')], ('6', 'clubs'), 'S', "Hard 17 vs 6 should STAND"),
        ([('5', 'hearts'), ('6', 'diamonds')], ('9', 'clubs'), 'D', "11 vs 9 should DOUBLE"),
        ([('10', 'hearts'), ('10', 'diamonds')], ('A', 'clubs'), 'S', "20 vs A should STAND"),
        ([('5', 'hearts'), ('3', 'diamonds')], ('6', 'clubs'), 'H', "Hard 8 vs 6 should HIT"),
        ([('9', 'hearts'), ('3', 'diamonds')], ('2', 'clubs'), 'H', "Hard 12 vs 2 should HIT"),
        ([('9', 'hearts'), ('4', 'diamonds')], ('6', 'clubs'), 'S', "Hard 13 vs 6 should STAND"),
    ]
    
    for player_cards, dealer_card, expected, desc in test_cases:
        hand = Hand()
        for rank, suit in player_cards:
            hand.add_card(Card(rank, suit))
        dealer = Card(dealer_card[0], dealer_card[1])
        
        action = strategy.get_optimal_action(hand, dealer, can_double=True, can_split=False)
        result = "✓" if action == expected else "✗"
        print(f"{result} {desc}: Got {action}, Expected {expected}")
    
    # Test soft hands
    print("\nSOFT HANDS:")
    soft_cases = [
        ([('A', 'hearts'), ('6', 'diamonds')], ('2', 'clubs'), 'H', "Soft 17 (A,6) vs 2 should HIT"),
        ([('A', 'hearts'), ('7', 'diamonds')], ('2', 'clubs'), 'S', "Soft 18 (A,7) vs 2 should STAND"),
        ([('A', 'hearts'), ('7', 'diamonds')], ('6', 'clubs'), 'Ds', "Soft 18 (A,7) vs 6 should DOUBLE/STAND"),
        ([('A', 'hearts'), ('2', 'diamonds')], ('5', 'clubs'), 'D', "Soft 13 (A,2) vs 5 should DOUBLE"),
        ([('A', 'hearts'), ('8', 'diamonds')], ('6', 'clubs'), 'S', "Soft 19 (A,8) vs 6 should STAND"),
    ]
    
    for player_cards, dealer_card, expected, desc in soft_cases:
        hand = Hand()
        for rank, suit in player_cards:
            hand.add_card(Card(rank, suit))
        dealer = Card(dealer_card[0], dealer_card[1])
        
        action = strategy.get_optimal_action(hand, dealer, can_double=True, can_split=False)
        result = "✓" if action == expected else "✗"
        print(f"{result} {desc}: Got {action}, Expected {expected}")
    
    # Test pairs
    print("\nPAIRS:")
    pair_cases = [
        ([('8', 'hearts'), ('8', 'diamonds')], ('10', 'clubs'), 'P', "8,8 vs 10 should SPLIT"),
        ([('A', 'hearts'), ('A', 'diamonds')], ('10', 'clubs'), 'P', "A,A vs 10 should SPLIT"),
        ([('10', 'hearts'), ('10', 'diamonds')], ('6', 'clubs'), 'S', "10,10 vs 6 should STAND"),
        ([('5', 'hearts'), ('5', 'diamonds')], ('10', 'clubs'), 'H', "5,5 vs 10 should HIT (hard 10 vs 10)"),
        ([('9', 'hearts'), ('9', 'diamonds')], ('7', 'clubs'), 'S', "9,9 vs 7 should STAND"),
        ([('2', 'hearts'), ('2', 'diamonds')], ('2', 'clubs'), 'P', "2,2 vs 2 should SPLIT"),
    ]
    
    for player_cards, dealer_card, expected, desc in pair_cases:
        hand = Hand()
        for rank, suit in player_cards:
            hand.add_card(Card(rank, suit))
        dealer = Card(dealer_card[0], dealer_card[1])
        
        action = strategy.get_optimal_action(hand, dealer, can_double=True, can_split=True)
        result = "✓" if action == expected else "✗"
        print(f"{result} {desc}: Got {action}, Expected {expected}")
    
    # Test action conversion
    print("\nACTION CONVERSION:")
    print("When double not allowed:")
    hand = Hand()
    hand.add_card(Card('5', 'hearts'))
    hand.add_card(Card('6', 'diamonds'))
    dealer = Card('9', 'clubs')
    
    with_double = strategy.get_optimal_action(hand, dealer, can_double=True, can_split=False)
    without_double = strategy.get_optimal_action(hand, dealer, can_double=False, can_split=False)
    print(f"11 vs 9 with double: {with_double}")
    print(f"11 vs 9 without double: {without_double}")

if __name__ == "__main__":
    test_basic_strategy()