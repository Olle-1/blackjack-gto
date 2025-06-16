"""Test script to verify game engine functionality"""

from game_engine import Card, Shoe, Hand, GameRules, GameState
from card_counting import CardCounter
from ev_calculator import EVCalculator

def test_card_creation():
    """Test card creation and values"""
    print("Testing Card Creation:")
    cards = [
        Card('A', 'hearts'),
        Card('K', 'spades'),
        Card('5', 'diamonds'),
        Card('10', 'clubs')
    ]
    
    for card in cards:
        print(f"  {card} - Value: {card.value}, Count: {card.count_value}")
    print()

def test_hand_calculation():
    """Test hand value calculation"""
    print("Testing Hand Calculation:")
    
    # Test soft hand
    hand1 = Hand()
    hand1.add_card(Card('A', 'hearts'))
    hand1.add_card(Card('6', 'diamonds'))
    print(f"  A-6: Value={hand1.value}, Soft={hand1.is_soft}")
    
    # Test hard hand
    hand2 = Hand()
    hand2.add_card(Card('10', 'hearts'))
    hand2.add_card(Card('7', 'diamonds'))
    print(f"  10-7: Value={hand2.value}, Soft={hand2.is_soft}")
    
    # Test multiple aces
    hand3 = Hand()
    hand3.add_card(Card('A', 'hearts'))
    hand3.add_card(Card('A', 'diamonds'))
    hand3.add_card(Card('9', 'clubs'))
    print(f"  A-A-9: Value={hand3.value}, Soft={hand3.is_soft}")
    
    # Test bust
    hand4 = Hand()
    hand4.add_card(Card('10', 'hearts'))
    hand4.add_card(Card('9', 'diamonds'))
    hand4.add_card(Card('5', 'clubs'))
    print(f"  10-9-5: Value={hand4.value}, Bust={hand4.is_bust}")
    print()

def test_shoe():
    """Test shoe functionality"""
    print("Testing Shoe:")
    shoe = Shoe(num_decks=6)
    print(f"  Cards in shoe: {shoe.cards_remaining()}")
    print(f"  Decks remaining: {shoe.decks_remaining():.2f}")
    
    # Deal some cards
    for _ in range(10):
        card = shoe.deal_card()
        print(f"  Dealt: {card}")
    
    print(f"  Cards remaining: {shoe.cards_remaining()}")
    print(f"  Needs shuffle: {shoe.needs_shuffle}")
    print()

def test_counting():
    """Test card counting"""
    print("Testing Card Counting:")
    counter = CardCounter()
    
    test_cards = [
        Card('2', 'hearts'),    # +1
        Card('10', 'spades'),   # -1
        Card('A', 'diamonds'),  # -1
        Card('5', 'clubs'),     # +1
        Card('7', 'hearts'),    # 0
    ]
    
    for card in test_cards:
        counter.update_count(card)
        print(f"  {card}: Running count = {counter.get_running_count()}")
    
    # Test true count
    cards_remaining = 250
    true_count = counter.get_true_count(cards_remaining)
    print(f"  True count with {cards_remaining} cards: {true_count:.2f}")
    print()

def test_ev_calculation():
    """Test EV calculations"""
    print("Testing EV Calculation:")
    ev_calc = EVCalculator()
    
    test_scenarios = [
        (0, 25),    # True count 0, $25 bet
        (2, 25),    # True count +2, $25 bet
        (-1, 25),   # True count -1, $25 bet
        (4, 100),   # True count +4, $100 bet
    ]
    
    for true_count, bet in test_scenarios:
        ev = ev_calc.calculate_ev(true_count, bet)
        edge = ev_calc.get_player_edge(true_count)
        print(f"  TC={true_count:+d}, Bet=${bet}: EV=${ev:+.2f}, Edge={edge:+.2f}%")
    print()

def test_game_flow():
    """Test basic game flow"""
    print("Testing Game Flow:")
    game = GameState()
    
    # Start a hand
    game.start_new_hand(25)
    print(f"  Player: {[str(c) for c in game.player_hand.cards]}")
    print(f"  Dealer: {[str(c) for c in game.dealer_hand.cards]}")
    
    # Player hits
    if not game.player_hand.is_blackjack:
        game.player_hit()
        print(f"  After hit: {[str(c) for c in game.player_hand.cards]} = {game.player_hand.value}")
        
        if not game.player_hand.is_bust:
            # Player stands
            game.player_stand()
            print(f"  Dealer final: {[str(c) for c in game.dealer_hand.cards]} = {game.dealer_hand.value}")
            
            # Get outcome
            outcome, profit = game.complete_hand()
            print(f"  Outcome: {outcome}, Profit: ${profit:+.2f}")
    print()

if __name__ == "__main__":
    print("=== Blackjack Game Engine Test ===\n")
    
    test_card_creation()
    test_hand_calculation()
    test_shoe()
    test_counting()
    test_ev_calculation()
    test_game_flow()
    
    print("All tests completed!")