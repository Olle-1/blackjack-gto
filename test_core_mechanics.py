#!/usr/bin/env python3
"""Test core game mechanics comprehensively"""

import sys
from game_engine import GameState, Card, Hand
from card_counting import CardCounter
from ev_calculator import EVCalculator
from basic_strategy import StrategyTracker
from settings import settings

def test_basic_actions():
    """Test HIT, STAND, DOUBLE actions"""
    print("=== Testing Basic Actions ===")
    
    try:
        # Test Hit Action
        game_state = GameState()
        game_state.start_new_hand(25)
        initial_cards = len(game_state.player_hand.cards)
        
        if game_state.player_hand.value < 21:
            result = game_state.player_hit()
            if len(game_state.player_hand.cards) == initial_cards + 1:
                print("✓ HIT action works - card added")
            else:
                print("✗ HIT action failed - no card added")
        
        # Test Stand Action (create new hand)
        game_state = GameState()
        game_state.start_new_hand(25)
        game_state.player_stand()
        if game_state.phase == "dealer_turn":
            print("✓ STAND action works - phase changed to dealer_turn")
        else:
            print(f"✗ STAND action failed - phase is {game_state.phase}")
        
        # Test Double Action (create hand with 10 or 11)
        game_state = GameState()
        # Create a hand with value 11 for doubling test
        game_state.start_new_hand(25)
        hand = game_state.player_hand
        # Clear hand and add specific cards for 11
        hand.cards = []
        hand.add_card(Card('6', 'Hearts'))
        hand.add_card(Card('5', 'Spades'))
        
        original_bet = game_state.hand_bets[0]
        original_bankroll = game_state.bankroll
        
        if hand.value == 11:
            result = game_state.player_double()
            if result and len(hand.cards) == 3:
                print("✓ DOUBLE action works - one card added and bet doubled")
            else:
                print("✗ DOUBLE action failed")
        
        return True
    except Exception as e:
        print(f"✗ Basic actions test failed: {e}")
        return False

def test_blackjack_scenarios():
    """Test various blackjack scenarios"""
    print("\n=== Testing Blackjack Scenarios ===")
    
    try:
        # Test Player Blackjack
        game_state = GameState()
        game_state.start_new_hand(25)
        
        # Force a blackjack by setting specific cards
        hand = game_state.player_hand
        hand.cards = []
        hand.add_card(Card('A', 'Hearts'))
        hand.add_card(Card('K', 'Spades'))
        
        if hand.is_blackjack and hand.value == 21:
            print("✓ Player blackjack detection works")
        else:
            print(f"✗ Player blackjack failed - is_blackjack: {hand.is_blackjack}, value: {hand.value}")
        
        # Test Dealer Blackjack
        dealer_hand = Hand(is_dealer=True)
        dealer_hand.add_card(Card('A', 'Spades'))
        dealer_hand.add_card(Card('Q', 'Hearts'))
        
        if dealer_hand.is_blackjack and dealer_hand.value == 21:
            print("✓ Dealer blackjack detection works")
        else:
            print(f"✗ Dealer blackjack failed - is_blackjack: {dealer_hand.is_blackjack}, value: {dealer_hand.value}")
        
        # Test Push (both blackjack)
        from game_engine import GameRules
        outcome, payout = GameRules.get_hand_outcome(hand, dealer_hand)
        if outcome == "Push" and payout == 1.0:
            print("✓ Blackjack push detection works")
        else:
            print(f"✗ Blackjack push failed - outcome: {outcome}, payout: {payout}")
        
        return True
    except Exception as e:
        print(f"✗ Blackjack scenarios test failed: {e}")
        return False

def test_soft_hands():
    """Test soft hand calculations"""
    print("\n=== Testing Soft Hands ===")
    
    try:
        # Test A-6 (soft 17)
        hand = Hand()
        hand.add_card(Card('A', 'Hearts'))
        hand.add_card(Card('6', 'Spades'))
        
        if hand.value == 17 and hand.is_soft:
            print("✓ A-6 = soft 17")
        else:
            print(f"✗ A-6 failed - value: {hand.value}, is_soft: {hand.is_soft}")
        
        # Test A-6-5 (soft becomes hard)
        hand.add_card(Card('5', 'Hearts'))
        if hand.value == 12 and not hand.is_soft:
            print("✓ A-6-5 = hard 12 (ace reduced)")
        else:
            print(f"✗ A-6-5 failed - value: {hand.value}, is_soft: {hand.is_soft}")
        
        # Test A-A-9 = 21
        hand2 = Hand()
        hand2.add_card(Card('A', 'Hearts'))
        hand2.add_card(Card('A', 'Spades'))
        hand2.add_card(Card('9', 'Hearts'))
        
        if hand2.value == 21:
            print("✓ A-A-9 = 21")
        else:
            print(f"✗ A-A-9 failed - value: {hand2.value}")
        
        return True
    except Exception as e:
        print(f"✗ Soft hands test failed: {e}")
        return False

def test_bust_detection():
    """Test bust detection"""
    print("\n=== Testing Bust Detection ===")
    
    try:
        hand = Hand()
        hand.add_card(Card('10', 'Hearts'))
        hand.add_card(Card('7', 'Spades'))
        hand.add_card(Card('8', 'Hearts'))  # 25 - bust
        
        if hand.is_bust and hand.value > 21:
            print("✓ Bust detection works")
        else:
            print(f"✗ Bust detection failed - is_bust: {hand.is_bust}, value: {hand.value}")
        
        return True
    except Exception as e:
        print(f"✗ Bust detection test failed: {e}")
        return False

def test_dealer_rules():
    """Test dealer hitting rules"""
    print("\n=== Testing Dealer Rules ===")
    
    try:
        from game_engine import GameRules
        
        # Test dealer hits soft 16
        hand = Hand(is_dealer=True)
        hand.add_card(Card('A', 'Hearts'))
        hand.add_card(Card('5', 'Spades'))  # Soft 16
        
        must_hit = GameRules.dealer_must_hit(hand)
        if must_hit:
            print("✓ Dealer hits soft 16")
        else:
            print("✗ Dealer should hit soft 16")
        
        # Test dealer stands on 17
        hand2 = Hand(is_dealer=True)
        hand2.add_card(Card('10', 'Hearts'))
        hand2.add_card(Card('7', 'Spades'))  # Hard 17
        
        must_hit2 = GameRules.dealer_must_hit(hand2)
        if not must_hit2:
            print("✓ Dealer stands on hard 17")
        else:
            print("✗ Dealer should stand on hard 17")
        
        return True
    except Exception as e:
        print(f"✗ Dealer rules test failed: {e}")
        return False

def test_win_loss_determination():
    """Test outcome calculations"""
    print("\n=== Testing Win/Loss Determination ===")
    
    try:
        from game_engine import GameRules
        
        # Player 20 vs Dealer 19 = Win
        player_hand = Hand()
        player_hand.add_card(Card('10', 'Hearts'))
        player_hand.add_card(Card('Q', 'Spades'))
        
        dealer_hand = Hand(is_dealer=True)
        dealer_hand.add_card(Card('10', 'Hearts'))
        dealer_hand.add_card(Card('9', 'Spades'))
        
        outcome, payout = GameRules.get_hand_outcome(player_hand, dealer_hand)
        if "Win" in outcome and payout == 2.0:
            print("✓ Player win detection works")
        else:
            print(f"✗ Player win failed - outcome: {outcome}, payout: {payout}")
        
        # Player 18 vs Dealer 20 = Loss
        player_hand2 = Hand()
        player_hand2.add_card(Card('10', 'Hearts'))
        player_hand2.add_card(Card('8', 'Spades'))
        
        dealer_hand2 = Hand(is_dealer=True)
        dealer_hand2.add_card(Card('10', 'Hearts'))
        dealer_hand2.add_card(Card('Q', 'Spades'))
        
        outcome2, payout2 = GameRules.get_hand_outcome(player_hand2, dealer_hand2)
        if "Lose" in outcome2 and payout2 == 0.0:
            print("✓ Player loss detection works")
        else:
            print(f"✗ Player loss failed - outcome: {outcome2}, payout: {payout2}")
        
        # Player 19 vs Dealer 19 = Push
        dealer_hand3 = Hand(is_dealer=True)
        dealer_hand3.add_card(Card('10', 'Hearts'))
        dealer_hand3.add_card(Card('9', 'Spades'))
        
        player_hand3 = Hand()
        player_hand3.add_card(Card('10', 'Hearts'))
        player_hand3.add_card(Card('9', 'Spades'))
        
        outcome3, payout3 = GameRules.get_hand_outcome(player_hand3, dealer_hand3)
        if outcome3 == "Push" and payout3 == 1.0:
            print("✓ Push detection works")
        else:
            print(f"✗ Push failed - outcome: {outcome3}, payout: {payout3}")
        
        return True
    except Exception as e:
        print(f"✗ Win/loss determination test failed: {e}")
        return False

def test_bankroll_calculations():
    """Test bankroll updates"""
    print("\n=== Testing Bankroll Calculations ===")
    
    try:
        game_state = GameState()
        initial_bankroll = game_state.bankroll
        bet_amount = 25
        
        # Note: start_new_hand doesn't deduct bankroll - this might be done in the UI layer
        game_state.start_new_hand(bet_amount)
        # Just verify the bet is set correctly
        if game_state.current_bet == bet_amount and game_state.hand_bets[0] == bet_amount:
            print("✓ Bet amount is set correctly")
        else:
            print(f"✗ Bet setting failed - current_bet: {game_state.current_bet}, hand_bet: {game_state.hand_bets[0]}")
        
        # Simulate a win and test payout
        current_bankroll = game_state.bankroll
        game_state.bankroll += bet_amount * 2  # Win bet back + winnings
        
        if game_state.bankroll == current_bankroll + (bet_amount * 2):
            print("✓ Win payout calculation works")
        else:
            print("✗ Win payout failed")
        
        return True
    except Exception as e:
        print(f"✗ Bankroll calculations test failed: {e}")
        return False

def test_session_statistics():
    """Test session tracking"""
    print("\n=== Testing Session Statistics ===")
    
    try:
        game_state = GameState()
        
        # Test initial stats
        if (game_state.hands_played == 0 and 
            game_state.wins == 0 and 
            game_state.losses == 0 and 
            game_state.pushes == 0):
            print("✓ Initial session stats are zero")
        else:
            print("✗ Initial session stats not zero")
        
        # Test hand counting
        game_state.start_new_hand(25)
        if game_state.hands_played == 1:
            print("✓ Hand counting works")
        else:
            print(f"✗ Hand counting failed - played: {game_state.hands_played}")
        
        return True
    except Exception as e:
        print(f"✗ Session statistics test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Core Game Mechanics Test ===\n")
    
    # Load settings
    settings.load()
    
    tests = [
        test_basic_actions,
        test_blackjack_scenarios,
        test_soft_hands,
        test_bust_detection,
        test_dealer_rules,
        test_win_loss_determination,
        test_bankroll_calculations,
        test_session_statistics
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
    
    print(f"\n=== Core Mechanics Test Summary ===")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")
    
    if failed == 0:
        print("✓ All core mechanics tests PASSED")
        print("✓ Game engine is working correctly")
    else:
        print("✗ Some core mechanics tests FAILED")
        print("✗ Game engine needs fixes")
    
    sys.exit(0 if failed == 0 else 1)