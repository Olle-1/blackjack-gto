#!/usr/bin/env python3
"""Simple test to verify core settings functionality works"""

import sys
import os
import tempfile

# Add the blackjack directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_functionality():
    """Test core settings functionality without UI dependencies"""
    print("🧪 Testing Core Settings Functionality...")
    
    try:
        # Test 1: Basic import
        print("1. Testing settings import...")
        from settings import settings, GameRules, BettingLimits, ShoeConfiguration
        print("   ✅ Import successful")
        
        # Test 2: Default values
        print("2. Testing default values...")
        assert settings.game_rules.dealer_stand_soft_17 == True
        assert settings.betting_limits.min_bet == 5
        assert settings.shoe_config.num_decks == 6
        assert settings.practice_modes.auto_deal == False
        print("   ✅ Default values correct")
        
        # Test 3: Value modification
        print("3. Testing value modification...")
        settings.game_rules.dealer_stand_soft_17 = False
        settings.betting_limits.min_bet = 10
        assert settings.game_rules.dealer_stand_soft_17 == False
        assert settings.betting_limits.min_bet == 10
        print("   ✅ Value modification works")
        
        # Test 4: Validation
        print("4. Testing validation...")
        errors = settings.validate()
        print(f"   ✅ Validation runs (found {len(errors)} errors)")
        
        # Test 5: Serialization
        print("5. Testing serialization...")
        data = settings.to_dict()
        assert isinstance(data, dict)
        assert 'game_rules' in data
        assert 'betting_limits' in data
        print("   ✅ Serialization works")
        
        # Test 6: Deserialization
        print("6. Testing deserialization...")
        from settings import Settings
        new_settings = Settings()
        new_settings.from_dict(data)
        assert new_settings.game_rules.dealer_stand_soft_17 == False
        assert new_settings.betting_limits.min_bet == 10
        print("   ✅ Deserialization works")
        
        # Test 7: Game engine integration
        print("7. Testing game engine integration...")
        from game_engine import GameState
        game_state = GameState()
        # These should not raise exceptions
        assert hasattr(game_state, 'shoe')
        assert hasattr(game_state, 'current_bet')
        print("   ✅ Game engine integration works")
        
        print("\n🎉 All core functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_persistence():
    """Test file persistence functionality"""
    print("\n🧪 Testing Settings Persistence...")
    
    try:
        from settings import Settings
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
            
        try:
            # Create settings instance with temp file
            test_settings = Settings(temp_file)
            
            # Modify some values
            test_settings.game_rules.dealer_stand_soft_17 = False
            test_settings.betting_limits.default_bet = 50
            
            # Save to file
            result = test_settings.save()
            assert result == True
            assert os.path.exists(temp_file)
            print("   ✅ Save to file works")
            
            # Load from file in new instance
            new_settings = Settings(temp_file)
            load_result = new_settings.load()
            assert load_result == True
            assert new_settings.game_rules.dealer_stand_soft_17 == False
            assert new_settings.betting_limits.default_bet == 50
            print("   ✅ Load from file works")
            
            print("\n🎉 Persistence tests passed!")
            return True
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        print(f"\n❌ Persistence test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("BLACKJACK SETTINGS SYSTEM TEST")
    print("=" * 60)
    
    success1 = test_core_functionality()
    success2 = test_persistence()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED - Settings system is working correctly!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Please check the errors above")
        sys.exit(1)