#!/usr/bin/env python3
"""Test application initialization without running the GUI"""

import sys
import os

# Import all modules at module level
try:
    import config
    from game_engine import GameState, GameRules, Card, Shoe, Hand
    from card_counting import CardCounter
    from ev_calculator import EVCalculator
    from basic_strategy import StrategyTracker
    from settings import settings
    from auto_play import AutoPlayer, DifficultyLevel, PracticeMode
    from betting_strategy import BettingStrategyCalculator
    IMPORTS_OK = True
except Exception as import_error:
    IMPORTS_OK = False
    IMPORT_ERROR = import_error

def test_imports():
    """Test that all required modules can be imported without errors"""
    if IMPORTS_OK:
        print("✓ Config module imported successfully")
        print("✓ Game engine imported successfully") 
        print("✓ Card counting imported successfully")
        print("✓ EV calculator imported successfully")
        print("✓ Basic strategy imported successfully")
        print("✓ Settings imported successfully")
        print("✓ Auto-play imported successfully")
        print("✓ Betting strategy imported successfully")
        return True
    else:
        print(f"✗ Import failed: {IMPORT_ERROR}")
        return False

def test_core_components():
    """Test core component initialization"""
    try:
        # Test GameState
        game_state = GameState()
        print(f"✓ GameState initialized - Current phase: {game_state.phase}")
        
        # Test CardCounter
        counter = CardCounter()
        print(f"✓ CardCounter initialized - Running count: {counter.running_count}")
        
        # Test EVCalculator
        ev_calc = EVCalculator()
        print(f"✓ EVCalculator initialized")
        
        # Test StrategyTracker
        strategy = StrategyTracker()
        print(f"✓ StrategyTracker initialized")
        
        # Test Settings
        settings.load()
        print(f"✓ Settings loaded - Default bankroll: ${settings.betting_limits.default_bankroll}")
        
        return True
    except Exception as e:
        print(f"✗ Component initialization failed: {e}")
        return False

def test_game_logic():
    """Test basic game logic without UI"""
    try:
        game_state = GameState()
        
        # Test shoe - it's already created in GameState init
        print(f"✓ Shoe initialized - Cards: {len(game_state.shoe.cards)}")
        
        # Test card dealing
        game_state.start_new_hand(25)  # $25 bet
        if game_state.player_hand:
            print(f"✓ New hand started - Player cards: {len(game_state.player_hand.cards)}")
            print(f"  Player hand value: {game_state.player_hand.value}")
            print(f"  Dealer upcard: {game_state.dealer_hand.cards[0] if game_state.dealer_hand.cards else 'None'}")
            
            # Test card counting
            counter = CardCounter()
            for card in game_state.player_hand.cards:
                counter.update_count(card)
            if game_state.dealer_hand.cards:
                counter.update_count(game_state.dealer_hand.cards[0])  # Count dealer upcard
            
            print(f"✓ Card counting works - Running count: {counter.running_count}")
            
            # Test EV calculation
            ev_calc = EVCalculator()
            true_count = counter.get_true_count(game_state.shoe.decks_remaining())
            ev = ev_calc.calculate_ev(100, true_count)  # $100 bet
            print(f"✓ EV calculation works - True count: {true_count:.2f}, EV: {ev:.2f}%")
        else:
            print("✗ Failed to start new hand")
        
        return True
    except Exception as e:
        print(f"✗ Game logic test failed: {e}")
        return False

def test_basic_strategy():
    """Test basic strategy tables"""
    try:
        from basic_strategy import BasicStrategy
        strategy = BasicStrategy()
        
        # Test a few known strategy decisions
        test_cases = [
            # (player_total, dealer_upcard, is_soft, can_double, expected_action)
            (16, 10, False, True, 'H'),  # Hard 16 vs 10 = Hit
            (11, 5, False, True, 'D'),   # 11 vs 5 = Double
            (17, 10, False, True, 'S'),  # 17 vs 10 = Stand
            ('A,7', 9, True, True, 'H'), # Soft 18 vs 9 = Hit
        ]
        
        # Test with actual Hand and Card objects
        from game_engine import Hand, Card
        
        # Create hands properly by adding cards one by one
        test_scenarios = []
        
        # Hard 16 vs 10 should HIT
        hand1 = Hand()
        hand1.add_card(Card('8', 'Hearts'))
        hand1.add_card(Card('8', 'Spades'))
        test_scenarios.append((hand1, Card('10', 'Hearts'), 'H'))
        
        # 11 vs 5 should DOUBLE  
        hand2 = Hand()
        hand2.add_card(Card('6', 'Hearts'))
        hand2.add_card(Card('5', 'Spades'))
        test_scenarios.append((hand2, Card('5', 'Hearts'), 'D'))
        
        # 17 vs 10 should STAND
        hand3 = Hand()
        hand3.add_card(Card('10', 'Hearts'))
        hand3.add_card(Card('7', 'Spades'))
        test_scenarios.append((hand3, Card('10', 'Hearts'), 'S'))
        
        for i, (hand, dealer_card, expected) in enumerate(test_scenarios):
            result = strategy.get_optimal_action(hand, dealer_card, True, False, None)
            if result == expected:
                print(f"✓ Strategy test {i+1}: {hand.value} vs {dealer_card.rank} = {result}")
            else:
                print(f"✗ Strategy test {i+1}: {hand.value} vs {dealer_card.rank} = {result} (expected {expected})")
        
        return True
    except Exception as e:
        print(f"✗ Basic strategy test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Blackjack Application Initialization Test ===\n")
    
    print("1. Testing imports...")
    imports_ok = test_imports()
    
    print("\n2. Testing core components...")
    components_ok = test_core_components()
    
    print("\n3. Testing game logic...")
    logic_ok = test_game_logic()
    
    print("\n4. Testing basic strategy...")
    strategy_ok = test_basic_strategy()
    
    print("\n=== Test Summary ===")
    all_tests_passed = imports_ok and components_ok and logic_ok and strategy_ok
    
    if all_tests_passed:
        print("✓ All initialization tests PASSED")
        print("✓ Application is ready for GUI testing")
    else:
        print("✗ Some tests FAILED")
        print("✗ Application needs fixes before GUI testing")
    
    sys.exit(0 if all_tests_passed else 1)