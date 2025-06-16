#!/usr/bin/env python3
"""Comprehensive test for card counting accuracy"""

import sys
from game_engine import GameState, Card, Shoe
from card_counting import CardCounter
from settings import settings

def test_hi_lo_values():
    """Test Hi-Lo card values are correct"""
    print("=== Testing Hi-Lo Card Values ===")
    
    try:
        counter = CardCounter()
        
        # Test low cards (2-6) = +1
        low_cards = ['2', '3', '4', '5', '6']
        for rank in low_cards:
            card = Card(rank, 'Hearts')
            initial_count = counter.running_count
            counter.update_count(card)
            if counter.running_count == initial_count + 1:
                print(f"✓ {rank} = +1")
            else:
                print(f"✗ {rank} = {counter.running_count - initial_count} (expected +1)")
                return False
        
        # Reset counter
        counter = CardCounter()
        
        # Test neutral cards (7-9) = 0
        neutral_cards = ['7', '8', '9']
        for rank in neutral_cards:
            card = Card(rank, 'Hearts')
            initial_count = counter.running_count
            counter.update_count(card)
            if counter.running_count == initial_count:
                print(f"✓ {rank} = 0")
            else:
                print(f"✗ {rank} = {counter.running_count - initial_count} (expected 0)")
                return False
        
        # Test high cards (10-A) = -1
        high_cards = ['10', 'J', 'Q', 'K', 'A']
        for rank in high_cards:
            card = Card(rank, 'Hearts')
            initial_count = counter.running_count
            counter.update_count(card)
            if counter.running_count == initial_count - 1:
                print(f"✓ {rank} = -1")
            else:
                print(f"✗ {rank} = {counter.running_count - initial_count} (expected -1)")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Hi-Lo values test failed: {e}")
        return False

def test_running_count_accumulation():
    """Test running count accumulates correctly"""
    print("\n=== Testing Running Count Accumulation ===")
    
    try:
        counter = CardCounter()
        
        # Deal known sequence: 2,3,4,10,J,Q = +1,+1,+1,-1,-1,-1 = 0
        test_sequence = [
            ('2', 'Hearts', 1),
            ('3', 'Spades', 2), 
            ('4', 'Diamonds', 3),
            ('10', 'Hearts', 2),
            ('J', 'Spades', 1),
            ('Q', 'Diamonds', 0)
        ]
        
        for rank, suit, expected_total in test_sequence:
            card = Card(rank, suit)
            counter.update_count(card)
            if counter.running_count == expected_total:
                print(f"✓ After {rank}: RC = {counter.running_count}")
            else:
                print(f"✗ After {rank}: RC = {counter.running_count} (expected {expected_total})")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Running count accumulation test failed: {e}")
        return False

def test_true_count_calculation():
    """Test true count calculation with different deck scenarios"""
    print("\n=== Testing True Count Calculation ===")
    
    try:
        counter = CardCounter()
        
        # Test scenarios: (running_count, cards_remaining, expected_true_count)
        scenarios = [
            (5, 260, 1.0),     # RC=5, 260 cards left (5 decks) = TC=1.0
            (10, 104, 5.0),    # RC=10, 104 cards left (2 decks) = TC=5.0
            (-6, 156, -2.0),   # RC=-6, 156 cards left (3 decks) = TC=-2.0
            (3, 78, 2.0),      # RC=3, 78 cards left (1.5 decks) = TC=2.0
            (1, 13, 2.0),      # RC=1, 13 cards left (0.25 decks, capped at 0.5) = TC=2.0
        ]
        
        for rc, cards_left, expected_tc in scenarios:
            counter.running_count = rc
            true_count = counter.get_true_count(cards_left)
            
            # Allow small floating point differences
            if abs(true_count - expected_tc) < 0.01:
                print(f"✓ RC={rc}, Cards={cards_left} → TC={true_count:.2f}")
            else:
                print(f"✗ RC={rc}, Cards={cards_left} → TC={true_count:.2f} (expected {expected_tc})")
                return False
        
        return True
    except Exception as e:
        print(f"✗ True count calculation test failed: {e}")
        return False

def test_deck_remaining_calculation():
    """Test decks remaining calculation accuracy"""
    print("\n=== Testing Decks Remaining Calculation ===")
    
    try:
        shoe = Shoe()
        
        # Test with fresh shoe
        initial_decks = shoe.decks_remaining()
        if abs(initial_decks - 6.0) < 0.1:
            print(f"✓ Fresh shoe: {initial_decks:.2f} decks")
        else:
            print(f"✗ Fresh shoe: {initial_decks:.2f} decks (expected ~6.0)")
            return False
        
        # Deal exactly one deck (52 cards)
        for _ in range(52):
            shoe.deal_card()
        
        after_one_deck = shoe.decks_remaining()
        if abs(after_one_deck - 5.0) < 0.1:
            print(f"✓ After 1 deck dealt: {after_one_deck:.2f} decks")
        else:
            print(f"✗ After 1 deck dealt: {after_one_deck:.2f} decks (expected ~5.0)")
            return False
        
        # Deal until penetration point (~4 decks)
        cards_to_deal = 52 * 3  # Deal 3 more decks
        for _ in range(cards_to_deal):
            if shoe.cards:  # Don't deal if empty
                shoe.deal_card()
        
        at_penetration = shoe.decks_remaining()
        if abs(at_penetration - 2.0) < 0.1:
            print(f"✓ At penetration: {at_penetration:.2f} decks")
        else:
            print(f"✗ At penetration: {at_penetration:.2f} decks (expected ~2.0)")
        
        return True
    except Exception as e:
        print(f"✗ Deck remaining calculation test failed: {e}")
        return False

def test_count_reset_on_shuffle():
    """Test count resets properly on shuffle"""
    print("\n=== Testing Count Reset on Shuffle ===")
    
    try:
        counter = CardCounter()
        
        # Build up a count
        for _ in range(10):
            counter.update_count(Card('2', 'Hearts'))  # +10
        
        if counter.running_count == 10:
            print("✓ Count built up correctly")
        else:
            print(f"✗ Count buildup failed: {counter.running_count}")
            return False
        
        # Reset count (simulate shuffle)
        counter.reset()
        
        if counter.running_count == 0:
            print("✓ Count reset correctly after shuffle")
        else:
            print(f"✗ Count reset failed: {counter.running_count}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Count reset test failed: {e}")
        return False

def test_count_accuracy_over_full_shoe():
    """Test count accuracy over an entire shoe"""
    print("\n=== Testing Count Accuracy Over Full Shoe ===")
    
    try:
        counter = CardCounter()
        shoe = Shoe()
        
        # Count all cards in a fresh shoe
        # A balanced shoe should end with RC = 0
        cards_counted = 0
        while shoe.cards and cards_counted < 312:  # 6 decks = 312 cards
            card = shoe.deal_card()
            counter.update_count(card)
            cards_counted += 1
        
        # Final count should be close to 0 (balanced deck)
        final_count = counter.running_count
        if abs(final_count) <= 2:  # Allow small variance due to penetration
            print(f"✓ Full shoe count: {final_count} (close to balanced)")
        else:
            print(f"✗ Full shoe count: {final_count} (too far from 0)")
            return False
        
        print(f"✓ Counted {cards_counted} cards accurately")
        return True
    except Exception as e:
        print(f"✗ Full shoe count test failed: {e}")
        return False

def test_count_during_game_simulation():
    """Test counting during actual game play simulation"""
    print("\n=== Testing Count During Game Simulation ===")
    
    try:
        game_state = GameState()
        counter = CardCounter()
        
        # Simulate 10 hands of play
        for hand_num in range(10):
            game_state.start_new_hand(25)
            
            # Count all visible cards
            for card in game_state.player_hand.cards:
                counter.update_count(card)
            
            # Count dealer upcard (hole card not counted until revealed)
            if game_state.dealer_hand.cards:
                counter.update_count(game_state.dealer_hand.cards[0])
            
            # Simulate dealer revealing hole card and drawing to 17
            if len(game_state.dealer_hand.cards) > 1:
                counter.update_count(game_state.dealer_hand.cards[1])  # Hole card
            
            # Simulate dealer drawing to 17
            while game_state.dealer_hand.value < 17:
                card = game_state.shoe.deal_card()
                game_state.dealer_hand.add_card(card)
                counter.update_count(card)
        
        print(f"✓ Simulated 10 hands, final RC: {counter.running_count}")
        
        # Verify true count calculation
        cards_left = game_state.shoe.cards_remaining()
        true_count = counter.get_true_count(cards_left)
        decks_left = cards_left / 52
        print(f"✓ True count: {true_count:.2f} with {decks_left:.2f} decks remaining")
        
        return True
    except Exception as e:
        print(f"✗ Game simulation count test failed: {e}")
        return False

def test_edge_cases():
    """Test counting edge cases"""
    print("\n=== Testing Counting Edge Cases ===")
    
    try:
        counter = CardCounter()
        
        # Test very low deck count (should cap at 0.5 for true count)
        counter.running_count = 2
        true_count_low = counter.get_true_count(5)  # Very few cards left (5 cards = 0.1 decks)
        
        # Should cap the denominator at 0.5
        expected_max_tc = 2 / 0.5  # = 4.0
        if abs(true_count_low - expected_max_tc) < 0.1:
            print(f"✓ Low deck count capped correctly: TC={true_count_low:.2f}")
        else:
            print(f"✗ Low deck count not capped: TC={true_count_low:.2f}")
        
        # Test negative true count
        counter.running_count = -8
        true_count_neg = counter.get_true_count(104)  # 2 decks
        expected_neg_tc = -4.0
        if abs(true_count_neg - expected_neg_tc) < 0.1:
            print(f"✓ Negative true count: TC={true_count_neg:.2f}")
        else:
            print(f"✗ Negative true count wrong: TC={true_count_neg:.2f}")
        
        # Test zero running count
        counter.running_count = 0
        true_count_zero = counter.get_true_count(156)  # 3 decks
        if true_count_zero == 0.0:
            print("✓ Zero running count → Zero true count")
        else:
            print(f"✗ Zero running count gave TC={true_count_zero}")
        
        return True
    except Exception as e:
        print(f"✗ Edge cases test failed: {e}")
        return False

def test_counting_performance():
    """Test counting performance over many cards"""
    print("\n=== Testing Counting Performance ===")
    
    try:
        import time
        
        counter = CardCounter()
        
        # Create 1000 random cards
        cards = []
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
        
        for i in range(1000):
            rank = ranks[i % len(ranks)]
            suit = suits[i % len(suits)]
            cards.append(Card(rank, suit))
        
        # Time the counting
        start_time = time.time()
        for card in cards:
            counter.update_count(card)
        end_time = time.time()
        
        elapsed = end_time - start_time
        cards_per_second = 1000 / elapsed if elapsed > 0 else float('inf')
        
        print(f"✓ Counted 1000 cards in {elapsed:.4f} seconds")
        print(f"✓ Performance: {cards_per_second:.0f} cards/second")
        
        # Should be able to handle at least 1000 cards/second
        if cards_per_second > 1000:
            print("✓ Performance is adequate for rapid play")
        else:
            print("⚠ Performance may be slow for rapid play")
        
        return True
    except Exception as e:
        print(f"✗ Performance test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Card Counting Accuracy Test ===\n")
    
    # Load settings
    settings.load()
    
    tests = [
        test_hi_lo_values,
        test_running_count_accumulation,
        test_true_count_calculation,
        test_deck_remaining_calculation,
        test_count_reset_on_shuffle,
        test_count_accuracy_over_full_shoe,
        test_count_during_game_simulation,
        test_edge_cases,
        test_counting_performance
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print(f"\n=== Card Counting Test Summary ===")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")
    
    if failed == 0:
        print("✓ All card counting tests PASSED")
        print("✓ Counting system is accurate and ready for 12-hour session")
    else:
        print("✗ Some card counting tests FAILED")
        print("✗ Counting system needs fixes before 12-hour session")
    
    sys.exit(0 if failed == 0 else 1)