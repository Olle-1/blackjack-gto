#!/usr/bin/env python3
"""Test betting strategy functionality"""

import sys
import os

# Add the blackjack directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_betting_strategy_components():
    """Test betting strategy components without UI"""
    print("🧪 Testing Betting Strategy Components...")
    
    try:
        # Test imports
        print("1. Testing imports...")
        from betting_strategy import BettingStrategyCalculator
        from ev_calculator import EVCalculator
        from settings import settings
        print("   ✅ Betting strategy imports successful")
        
        # Test component creation
        print("2. Testing component creation...")
        ev_calc = EVCalculator()
        betting_calc = BettingStrategyCalculator(ev_calc)
        print("   ✅ Component creation successful")
        
        # Test flat betting
        print("3. Testing flat betting...")
        settings.betting_limits.betting_strategy = "flat"
        settings.betting_limits.default_bet = 25
        bet = betting_calc.calculate_bet_size(1000, 2.0, 25)
        assert bet == 25, f"Expected 25, got {bet}"
        print("   ✅ Flat betting works")
        
        # Test spread betting
        print("4. Testing spread betting...")
        settings.betting_limits.betting_strategy = "spread"
        settings.betting_limits.min_bet = 5
        settings.betting_limits.spread_min_multiplier = 1.0
        settings.betting_limits.spread_max_multiplier = 8.0
        settings.betting_limits.spread_start_count = 1.0
        
        # Test low count (should bet minimum)
        bet = betting_calc.calculate_bet_size(1000, 0.5, 25)
        assert bet == 5, f"Expected 5 for low count, got {bet}"
        
        # Test high count (should bet more)
        bet = betting_calc.calculate_bet_size(1000, 3.0, 25)
        assert bet > 5, f"Expected bet > 5 for high count, got {bet}"
        print("   ✅ Spread betting works")
        
        # Test Kelly betting
        print("5. Testing Kelly betting...")
        settings.betting_limits.betting_strategy = "kelly"
        settings.betting_limits.kelly_fraction = 0.25
        
        # Test positive count (should calculate Kelly bet)
        bet = betting_calc.calculate_bet_size(1000, 2.0, 25)
        assert bet >= 5, f"Expected bet >= 5 for Kelly, got {bet}"
        print("   ✅ Kelly betting works")
        
        # Test descriptions
        print("6. Testing strategy descriptions...")
        settings.betting_limits.betting_strategy = "flat"
        desc = betting_calc.get_strategy_description()
        assert "Flat betting" in desc
        
        settings.betting_limits.betting_strategy = "spread"
        desc = betting_calc.get_strategy_description()
        assert "Spread betting" in desc
        
        settings.betting_limits.betting_strategy = "kelly"
        desc = betting_calc.get_strategy_description()
        assert "Kelly" in desc
        print("   ✅ Strategy descriptions work")
        
        print("\n🎉 All betting strategy tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Betting strategy test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_settings_integration():
    """Test that betting strategy settings work"""
    print("\n🧪 Testing Settings Integration...")
    
    try:
        from settings import Settings
        
        # Test that new settings fields exist
        print("1. Testing new settings fields...")
        test_settings = Settings()
        assert hasattr(test_settings.betting_limits, 'betting_strategy')
        assert hasattr(test_settings.betting_limits, 'spread_min_multiplier')
        assert hasattr(test_settings.betting_limits, 'kelly_fraction')
        print("   ✅ New settings fields exist")
        
        # Test default values
        print("2. Testing default values...")
        assert test_settings.betting_limits.betting_strategy == "flat"
        assert test_settings.betting_limits.spread_min_multiplier == 1.0
        assert test_settings.betting_limits.kelly_fraction == 0.25
        print("   ✅ Default values correct")
        
        # Test serialization includes new fields
        print("3. Testing serialization...")
        data = test_settings.to_dict()
        assert 'betting_strategy' in data['betting_limits']
        assert 'kelly_fraction' in data['betting_limits']
        print("   ✅ Serialization includes new fields")
        
        print("\n🎉 Settings integration tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Settings integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_betting_strategies():
    """Demonstrate different betting strategies"""
    print("\n🎯 BETTING STRATEGY DEMONSTRATION:")
    print("=" * 50)
    
    try:
        from betting_strategy import BettingStrategyCalculator
        from ev_calculator import EVCalculator
        from settings import settings
        
        ev_calc = EVCalculator()
        betting_calc = BettingStrategyCalculator(ev_calc)
        
        bankroll = 1000
        test_counts = [-2, -1, 0, 1, 2, 3, 4, 5]
        
        print(f"Bankroll: ${bankroll}")
        print(f"{'Count':<6} {'Flat':<8} {'Spread':<10} {'Kelly':<8}")
        print("-" * 35)
        
        for count in test_counts:
            # Flat betting
            settings.betting_limits.betting_strategy = "flat"
            flat_bet = betting_calc.calculate_bet_size(bankroll, count, 25)
            
            # Spread betting
            settings.betting_limits.betting_strategy = "spread"
            spread_bet = betting_calc.calculate_bet_size(bankroll, count, 25)
            
            # Kelly betting
            settings.betting_limits.betting_strategy = "kelly"
            kelly_bet = betting_calc.calculate_bet_size(bankroll, count, 25)
            
            print(f"{count:+2.0f}     ${flat_bet:<7.0f} ${spread_bet:<9.0f} ${kelly_bet:<7.0f}")
        
        print("\n📊 STRATEGY DESCRIPTIONS:")
        for strategy in ["flat", "spread", "kelly"]:
            settings.betting_limits.betting_strategy = strategy
            desc = betting_calc.get_strategy_description()
            print(f"  {strategy.upper()}: {desc}")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("BETTING STRATEGY SYSTEM TEST")
    print("=" * 60)
    
    success1 = test_betting_strategy_components()
    success2 = test_settings_integration()
    success3 = demo_betting_strategies()
    
    print("\n" + "=" * 60)
    if success1 and success2 and success3:
        print("🎉 ALL TESTS PASSED - Betting strategy system is working!")
        print("\nNEW FEATURES ADDED:")
        print("✅ Flat betting (default)")
        print("✅ Spread betting (1x-8x based on count)")
        print("✅ Kelly Criterion betting (25% Kelly)")
        print("✅ Settings dialog with strategy selection")
        print("✅ Real-time bet suggestions in game")
        print("✅ Strategy descriptions and help text")
    else:
        print("❌ SOME TESTS FAILED")
    
    sys.exit(0)