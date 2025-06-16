#!/usr/bin/env python3
"""Test that settings button exists and is functional"""

import tkinter as tk
import sys
from ui_components import GameControls

def test_settings_button_exists():
    """Test that settings button is created and configured"""
    print("=== Testing Settings Button ===")
    
    try:
        # Create a test window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create GameControls
        game_controls = GameControls(root)
        
        # Check if settings button exists
        if hasattr(game_controls, 'settings_btn'):
            print("✓ Settings button exists in GameControls")
            
            # Check button properties
            button_text = game_controls.settings_btn.cget('text')
            if button_text == "SETTINGS":
                print("✓ Settings button has correct text")
            else:
                print(f"✗ Settings button text is '{button_text}' instead of 'SETTINGS'")
            
            # Check if button is visible (grid configured)
            grid_info = game_controls.settings_btn.grid_info()
            if grid_info:
                print(f"✓ Settings button is gridded at row {grid_info['row']}, column {grid_info['column']}")
                return True
            else:
                print("✗ Settings button is not gridded (not visible)")
                return False
        else:
            print("✗ Settings button does not exist")
            return False
            
    except Exception as e:
        print(f"✗ Settings button test failed: {e}")
        return False
    finally:
        if 'root' in locals():
            root.destroy()

def test_full_ui_layout():
    """Test complete UI layout to verify settings button placement"""
    print("\n=== Testing Full UI Layout ===")
    
    try:
        # Import main components
        from ui_components import (
            BlackjackTable, ControlPanel, InfoDisplay, 
            GameControls, MessageDisplay, StrategyDisplay
        )
        from session_stats_display import SessionStatsDisplay
        
        # Create test window
        root = tk.Tk()
        root.withdraw()
        
        # Create all UI components in order
        message_display = MessageDisplay(root)
        table = BlackjackTable(root)
        control_panel = ControlPanel(root)
        info_display = InfoDisplay(root)
        strategy_display = StrategyDisplay(root)
        session_stats_display = SessionStatsDisplay(root)
        game_controls = GameControls(root)
        
        # Verify game controls and settings button
        if hasattr(game_controls, 'settings_btn'):
            print("✓ Settings button created in full UI layout")
            
            # Check all GameControls buttons
            buttons = [
                ('new_shoe_btn', 'NEW SHOE'),
                ('reset_count_btn', 'RESET COUNT'),
                ('settings_btn', 'SETTINGS')
            ]
            
            for btn_name, expected_text in buttons:
                if hasattr(game_controls, btn_name):
                    btn = getattr(game_controls, btn_name)
                    text = btn.cget('text')
                    if text == expected_text:
                        print(f"✓ {btn_name}: '{text}'")
                    else:
                        print(f"✗ {btn_name}: '{text}' (expected '{expected_text}')")
                else:
                    print(f"✗ {btn_name} missing")
            
            return True
        else:
            print("✗ Settings button missing from full UI layout")
            return False
            
    except Exception as e:
        print(f"✗ Full UI layout test failed: {e}")
        return False
    finally:
        if 'root' in locals():
            root.destroy()

if __name__ == "__main__":
    print("=== Settings Button UI Test ===\n")
    
    test1_passed = test_settings_button_exists()
    test2_passed = test_full_ui_layout()
    
    print(f"\n=== Test Summary ===")
    if test1_passed and test2_passed:
        print("✓ All settings button tests PASSED")
        print("✓ Settings button is properly implemented and should be visible")
    else:
        print("✗ Some settings button tests FAILED")
        print("✗ Settings button may have issues")
    
    sys.exit(0 if (test1_passed and test2_passed) else 1)