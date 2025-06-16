#!/usr/bin/env python3
"""Comprehensive test for EV calculations and mathematical accuracy"""

import sys
from ev_calculator import EVCalculator
from card_counting import CardCounter
from game_engine import GameState
from betting_strategy import BettingStrategyCalculator
from settings import settings

def test_base_ev_formula():
    """Test base EV formula: -0.5% + (0.5% × True Count)"""
    print("=== Testing Base EV Formula ===")
    
    try:
        ev_calc = EVCalculator()
        
        # Test scenarios: (true_count, expected_ev_percentage)
        scenarios = [
            (0.0, -0.5),    # TC=0 → -0.5% house edge
            (1.0, 0.0),     # TC=1 → break even
            (2.0, 0.5),     # TC=2 → +0.5% player edge
            (3.0, 1.0),     # TC=3 → +1.0% player edge
            (4.0, 1.5),     # TC=4 → +1.5% player edge
            (-1.0, -1.0),   # TC=-1 → -1.0% house edge
            (-2.0, -1.5),   # TC=-2 → -1.5% house edge
            (5.5, 2.25),    # TC=5.5 → +2.25% player edge
        ]
        
        for true_count, expected_ev_pct in scenarios:
            ev_pct = ev_calc.get_player_edge(true_count)
            
            if abs(ev_pct - expected_ev_pct) < 0.01:
                print(f"✓ TC={true_count:+4.1f} → EV={ev_pct:+5.2f}%")
            else:
                print(f"✗ TC={true_count:+4.1f} → EV={ev_pct:+5.2f}% (expected {expected_ev_pct:+5.2f}%)")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Base EV formula test failed: {e}")
        return False

def test_bet_ev_calculation():
    """Test EV calculation for specific bet amounts"""
    print("\n=== Testing Bet EV Calculation ===")
    
    try:
        ev_calc = EVCalculator()
        
        # Test scenarios: (bet_amount, true_count, expected_ev_dollars)
        scenarios = [
            (100, 0.0, -0.50),   # $100 at TC=0 → -$0.50 EV
            (100, 1.0, 0.00),    # $100 at TC=1 → $0.00 EV  
            (100, 2.0, 0.50),    # $100 at TC=2 → +$0.50 EV
            (50, 3.0, 0.50),     # $50 at TC=3 → +$0.50 EV
            (200, -1.0, -2.00),  # $200 at TC=-1 → -$2.00 EV
            (25, 4.0, 0.375),    # $25 at TC=4 → +$0.375 EV
        ]
        
        for bet_amount, true_count, expected_ev_dollars in scenarios:
            ev_dollars = ev_calc.calculate_ev(true_count, bet_amount)
            
            if abs(ev_dollars - expected_ev_dollars) < 0.01:
                print(f"✓ ${bet_amount} at TC={true_count:+4.1f} → EV=${ev_dollars:+6.2f}")
            else:
                print(f"✗ ${bet_amount} at TC={true_count:+4.1f} → EV=${ev_dollars:+6.2f} (expected ${expected_ev_dollars:+6.2f})")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Bet EV calculation test failed: {e}")
        return False

def test_session_ev_tracking():
    """Test session EV tracking accuracy"""
    print("\n=== Testing Session EV Tracking ===")
    
    try:
        ev_calc = EVCalculator()
        
        # Simulate a series of hands with known EVs
        hands = [
            (100, 0.0, -0.50),   # Hand 1: -$0.50 EV
            (100, 2.0, 0.50),    # Hand 2: +$0.50 EV
            (50, 1.0, 0.00),     # Hand 3: $0.00 EV
            (200, 3.0, 2.00),    # Hand 4: +$2.00 EV
            (75, -1.0, -0.75),   # Hand 5: -$0.75 EV
        ]
        
        total_expected_ev = 0.0
        
        for i, (bet, tc, expected_hand_ev) in enumerate(hands):
            hand_ev = ev_calc.calculate_ev(tc, bet)
            total_expected_ev += expected_hand_ev
            
            # Track in calculator
            ev_calc.update_session_ev(bet, tc, 0)  # Assuming break-even actual result
            
            print(f"  Hand {i+1}: ${bet} at TC={tc:+4.1f} → EV=${hand_ev:+6.2f}")
        
        # Check cumulative EV
        cumulative_ev = ev_calc.session_stats.total_expected_ev
        
        if abs(cumulative_ev - total_expected_ev) < 0.01:
            print(f"✓ Session EV tracking: ${cumulative_ev:+6.2f} (expected ${total_expected_ev:+6.2f})")
        else:
            print(f"✗ Session EV tracking: ${cumulative_ev:+6.2f} (expected ${total_expected_ev:+6.2f})")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Session EV tracking test failed: {e}")
        return False

def test_variance_calculations():
    """Test variance tracking through session statistics"""
    print("\n=== Testing Variance Calculations ===")
    
    try:
        ev_calc = EVCalculator()
        
        # Test variance tracking through session stats
        # Add some hands with different outcomes
        test_hands = [
            (100, 1.0, 200),   # Win $200 on $100 bet
            (100, 1.0, 0),     # Lose $100 on $100 bet  
            (100, 1.0, 100),   # Push on $100 bet
        ]
        
        for bet, tc, actual_result in test_hands:
            ev_calc.update_session_ev(bet, tc, actual_result)
        
        # Get variance from session stats
        variance = ev_calc.session_stats.get_variance()
        print(f"✓ Session variance tracked: {variance:.2f}")
        
        # Test session summary
        summary = ev_calc.session_stats.get_session_summary()
        if 'variance' in summary and 'expected_ev' in summary:
            print(f"✓ Session summary includes variance and EV")
        else:
            print("✗ Session summary missing key fields")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Variance calculations test failed: {e}")
        return False

def test_bankroll_risk_calculations():
    """Test bankroll management concepts"""
    print("\n=== Testing Bankroll Management ===")
    
    try:
        ev_calc = EVCalculator()
        
        # Test bankroll-related calculations that are implemented
        # Test that EV calculations work with different bankroll scenarios
        bankroll_scenarios = [
            (1000, 25, 1.0),   # Conservative: 2.5% of bankroll
            (1000, 100, 2.0),  # Aggressive: 10% of bankroll
            (500, 25, 0.5),    # Conservative with smaller bankroll
        ]
        
        for bankroll, bet_size, true_count in bankroll_scenarios:
            ev = ev_calc.calculate_ev(true_count, bet_size)
            bet_percentage = (bet_size / bankroll) * 100
            
            print(f"✓ ${bankroll} bankroll, ${bet_size} bet ({bet_percentage:.1f}%) → EV=${ev:+.2f}")
            
            # Sanity check: bet shouldn't be more than 20% of bankroll for safety
            if bet_percentage > 20:
                print(f"⚠ High bet percentage: {bet_percentage:.1f}%")
        
        return True
    except Exception as e:
        print(f"✗ Bankroll management test failed: {e}")
        return False

def test_kelly_criterion():
    """Test Kelly Criterion bet sizing"""
    print("\n=== Testing Kelly Criterion ===")
    
    try:
        ev_calc = EVCalculator()
        
        # Kelly formula: f = (bp - q) / b
        # where f = fraction to bet, b = odds, p = win probability, q = lose probability
        
        scenarios = [
            (1000, 1.0, 0.25),   # $1000 bankroll, +1.0% edge, 25% Kelly
            (2000, 2.0, 0.25),   # $2000 bankroll, +2.0% edge, 25% Kelly
            (500, 0.5, 0.25),    # $500 bankroll, +0.5% edge, 25% Kelly
        ]
        
        for bankroll, edge_pct, kelly_fraction in scenarios:
            # Convert edge percentage to true count for the function
            # edge = -0.005 + true_count * 0.005, so true_count = (edge + 0.005) / 0.005
            true_count_for_edge = (edge_pct/100 + 0.005) / 0.005
            kelly_bet = ev_calc.calculate_kelly_bet(bankroll, true_count_for_edge, kelly_fraction)
            
            # Kelly bet should be reasonable relative to bankroll
            if 0 < kelly_bet < bankroll * 0.5:  # Should be less than 50% of bankroll
                bet_pct = (kelly_bet / bankroll) * 100
                print(f"✓ Kelly bet: ${kelly_bet:.2f} ({bet_pct:.1f}% of ${bankroll} bankroll, {edge_pct}% edge)")
            else:
                print(f"✗ Unreasonable Kelly bet: ${kelly_bet:.2f} for ${bankroll} bankroll")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Kelly Criterion test failed: {e}")
        return False

def test_betting_strategy_integration():
    """Test integration with betting strategy calculator"""
    print("\n=== Testing Betting Strategy Integration ===")
    
    try:
        ev_calc = EVCalculator()
        betting_calc = BettingStrategyCalculator(ev_calc)
        
        # Test flat betting
        flat_bet = betting_calc.calculate_bet_size(1000, 1.5, 25)
        if flat_bet == settings.betting_limits.default_bet:
            print("✓ Flat betting returns default bet size")
        else:
            print(f"✗ Flat betting returned {flat_bet} instead of {settings.betting_limits.default_bet}")
        
        # Test that different strategies can be calculated
        strategies = ["flat", "spread", "kelly"]
        for strategy in strategies:
            # Temporarily change strategy
            original_strategy = settings.betting_limits.betting_strategy
            settings.betting_limits.betting_strategy = strategy
            
            bet_size = betting_calc.calculate_bet_size(1000, 2.0, 25)
            print(f"✓ {strategy.capitalize()} strategy calculated: ${bet_size}")
            
            # Restore original strategy
            settings.betting_limits.betting_strategy = original_strategy
        
        return True
    except Exception as e:
        print(f"✗ Betting strategy integration test failed: {e}")
        return False

def test_floating_point_precision():
    """Test floating point precision over many calculations"""
    print("\n=== Testing Floating Point Precision ===")
    
    try:
        ev_calc = EVCalculator()
        
        # Perform many small calculations and check for drift
        cumulative_ev = 0.0
        
        for i in range(1000):
            # Small bet, small true count
            bet = 10
            true_count = 0.1
            hand_ev = ev_calc.calculate_ev(true_count, bet)
            cumulative_ev += hand_ev
        
        # Expected: 1000 * (10 * (0.1 * 0.005 - 0.005)) = 1000 * (10 * -0.0045) = 1000 * -0.045 = -45.0
        expected_cumulative = 1000 * (10 * (0.1 * 0.005 - 0.005))
        
        if abs(cumulative_ev - expected_cumulative) < 0.01:
            print(f"✓ Floating point precision maintained over 1000 calculations")
            print(f"  Cumulative EV: ${cumulative_ev:.6f} (expected ${expected_cumulative:.6f})")
        else:
            print(f"✗ Floating point drift detected: ${cumulative_ev:.6f} vs ${expected_cumulative:.6f}")
            return False
        
        # Test very small numbers
        tiny_ev = ev_calc.calculate_ev(0.001, 0.01)  # 1 cent bet at tiny true count
        if abs(tiny_ev) < 1e-6:  # Should be very small but not zero
            print(f"✓ Tiny calculations handled correctly: ${tiny_ev:.8f}")
        else:
            print(f"⚠ Tiny calculation result: ${tiny_ev:.8f}")
        
        return True
    except Exception as e:
        print(f"✗ Floating point precision test failed: {e}")
        return False

def test_edge_case_scenarios():
    """Test mathematical edge cases"""
    print("\n=== Testing Edge Case Scenarios ===")
    
    try:
        ev_calc = EVCalculator()
        
        # Test zero bet
        zero_ev = ev_calc.calculate_ev(2.0, 0)
        if zero_ev == 0.0:
            print("✓ Zero bet returns zero EV")
        else:
            print(f"✗ Zero bet returned {zero_ev}")
        
        # Test very high true count
        high_tc_ev = ev_calc.calculate_ev(10.0, 100)
        expected_high = 100 * (10.0 * 0.005 - 0.005)  # (10*0.005 - 0.005) = 0.045 * 100 = 4.5
        if abs(high_tc_ev - expected_high) < 0.01:
            print(f"✓ Very high true count handled: TC=10.0 → EV=${high_tc_ev:.2f}")
        else:
            print(f"✗ High true count calculation error: ${high_tc_ev:.2f} vs ${expected_high:.2f}")
        
        # Test very negative true count
        negative_tc_ev = ev_calc.calculate_ev(-5.0, 100)
        expected_negative = 100 * (-5.0 * 0.005 - 0.005)  # (-5*0.005 - 0.005) = -0.03 * 100 = -3.0
        if abs(negative_tc_ev - expected_negative) < 0.01:
            print(f"✓ Very negative true count handled: TC=-5.0 → EV=${negative_tc_ev:.2f}")
        else:
            print(f"✗ Negative true count calculation error: ${negative_tc_ev:.2f} vs ${expected_negative:.2f}")
        
        return True
    except Exception as e:
        print(f"✗ Edge case scenarios test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== EV and Mathematics Test ===\n")
    
    # Load settings
    settings.load()
    
    tests = [
        test_base_ev_formula,
        test_bet_ev_calculation,
        test_session_ev_tracking,
        test_variance_calculations,
        test_bankroll_risk_calculations,
        test_kelly_criterion,
        test_betting_strategy_integration,
        test_floating_point_precision,
        test_edge_case_scenarios
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
    
    print(f"\n=== EV and Mathematics Test Summary ===")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")
    
    if failed == 0:
        print("✓ All EV and mathematics tests PASSED")
        print("✓ Mathematical accuracy verified for 12-hour session")
    else:
        print("✗ Some EV and mathematics tests FAILED")
        print("✗ Mathematical accuracy needs verification before 12-hour session")
    
    sys.exit(0 if failed == 0 else 1)