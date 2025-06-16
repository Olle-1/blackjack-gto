#!/usr/bin/env python3
"""Test auto-play and practice mode functionality"""

import sys
import os

# Add the blackjack directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_auto_play_components():
    """Test that auto-play components can be imported and instantiated"""
    print("🧪 Testing Auto-Play Components...")
    
    try:
        # Test imports
        print("1. Testing imports...")
        from auto_play import AutoPlayer, DifficultyLevel, PracticeMode
        from basic_strategy import BasicStrategy
        print("   ✅ Auto-play imports successful")
        
        # Test component creation
        print("2. Testing component creation...")
        strategy = BasicStrategy()
        auto_player = AutoPlayer(strategy)
        difficulty = DifficultyLevel()
        practice_mode = PracticeMode()
        print("   ✅ Component creation successful")
        
        # Test auto player configuration
        print("3. Testing auto player configuration...")
        auto_player.set_speed(500)  # 500ms
        practice_mode.set_auto_player(auto_player)
        print("   ✅ Auto player configuration successful")
        
        # Test difficulty levels
        print("4. Testing difficulty levels...")
        levels = difficulty.get_level_names()
        assert len(levels) == 4  # beginner, intermediate, advanced, expert
        assert 'Beginner' in levels
        assert 'Expert' in levels
        
        # Test difficulty settings
        assert difficulty.should_show_count() == True  # Default is beginner
        difficulty.set_level('expert')
        assert difficulty.should_show_count() == False  # Expert hides count
        print("   ✅ Difficulty levels working")
        
        # Test practice mode session tracking
        print("5. Testing practice mode session tracking...")
        practice_mode.start_practice_session()
        practice_mode.record_decision(True)   # Correct decision
        practice_mode.record_decision(False)  # Incorrect decision
        practice_mode.record_hand_played()
        
        summary = practice_mode.get_session_summary()
        assert summary['total_decisions'] == 2
        assert summary['correct_decisions'] == 1
        assert summary['hands_played'] == 1
        assert summary['accuracy_percentage'] == 50.0
        print("   ✅ Session tracking working")
        
        print("\n🎉 All auto-play component tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Auto-play test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_integration():
    """Test that main game can import auto-play without errors"""
    print("\n🧪 Testing Main Game Integration...")
    
    try:
        # This tests that main.py can import auto_play without errors
        print("1. Testing main game import with auto-play...")
        
        # We can't actually run the GUI, but we can test the imports
        import main
        print("   ✅ Main game import successful")
        
        print("\n🎉 Main game integration test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Main integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("AUTO-PLAY AND PRACTICE MODE TEST")
    print("=" * 60)
    
    success1 = test_auto_play_components()
    success2 = test_main_integration()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED - Auto-play system is working correctly!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Please check the errors above")
        sys.exit(1)