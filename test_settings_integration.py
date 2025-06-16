#!/usr/bin/env python3
"""Simple test to verify settings integration works correctly"""

import sys
import os
import tempfile
import json

# Add the blackjack directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_settings_import():
    """Test that settings can be imported without errors"""
    try:
        from settings import settings, GameRules, BettingLimits, ShoeConfiguration
        print("✅ Settings import successful")
        return True
    except Exception as e:
        print(f"❌ Settings import failed: {e}")
        return False

def test_settings_basic_functionality():
    """Test basic settings functionality"""
    try:
        from settings import settings
        
        # Test default values
        assert settings.game_rules.dealer_stand_soft_17 == True
        assert settings.betting_limits.min_bet == 5
        assert settings.shoe_config.num_decks == 6
        
        # Test modification
        settings.game_rules.dealer_stand_soft_17 = False
        assert settings.game_rules.dealer_stand_soft_17 == False
        
        print("✅ Basic settings functionality works")
        return True
    except Exception as e:
        print(f"❌ Basic settings test failed: {e}")
        return False

def test_settings_persistence():
    """Test settings save/load functionality"""
    try:
        from settings import settings
        
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        # Backup original file path
        original_file = settings.settings_file
        settings.settings_file = temp_file
        
        try:
            # Modify settings
            settings.game_rules.dealer_stand_soft_17 = False
            settings.betting_limits.min_bet = 10
            
            # Save settings
            settings.save()
            
            # Verify file was created
            assert os.path.exists(temp_file)
            
            # Load settings in a new instance
            from settings import Settings
            new_settings = Settings(temp_file)
            new_settings.load()
            
            # Verify settings were loaded correctly
            assert new_settings.game_rules.dealer_stand_soft_17 == False
            assert new_settings.betting_limits.min_bet == 10
            
            print("✅ Settings persistence works")
            return True
            
        finally:
            # Restore original file path
            settings.settings_file = original_file
            # Clean up temp file
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        print(f"❌ Settings persistence test failed: {e}")
        return False

def test_game_engine_integration():
    """Test that game engine can use settings"""
    try:
        from settings import settings
        from game_engine import GameState, Shoe
        
        # Test shoe creation with settings
        game_state = GameState()
        assert game_state.shoe.num_decks == settings.shoe_config.num_decks
        
        # Test default bet from settings
        assert game_state.current_bet == settings.betting_limits.default_bet
        
        print("✅ Game engine integration works")
        return True
    except Exception as e:
        print(f"❌ Game engine integration test failed: {e}")
        return False

def test_settings_dialog_import():
    """Test that settings dialog can be imported"""
    try:
        from settings_dialog import SettingsDialog
        print("✅ Settings dialog import successful")
        return True
    except Exception as e:
        print(f"❌ Settings dialog import failed: {e}")
        return False

def test_main_game_import():
    """Test that main game can be imported with settings"""
    try:
        # This will test the full integration
        from main import BlackjackGame
        print("✅ Main game import with settings successful")
        return True
    except Exception as e:
        print(f"❌ Main game import failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("🧪 Testing Settings Integration...")
    print("=" * 50)
    
    tests = [
        ("Settings Import", test_settings_import),
        ("Settings Basic Functionality", test_settings_basic_functionality),
        ("Settings Persistence", test_settings_persistence),
        ("Game Engine Integration", test_game_engine_integration),
        ("Settings Dialog Import", test_settings_dialog_import),
        ("Main Game Import", test_main_game_import),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Settings integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)