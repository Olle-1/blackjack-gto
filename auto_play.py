"""Auto-play functionality for testing and practice"""

import time
from typing import Optional, Callable
from threading import Thread, Event

try:
    import tkinter as tk
except ImportError:
    # tkinter not available, create a dummy module for constants
    class tk:
        DISABLED = 'disabled'
        NORMAL = 'normal'

from basic_strategy import BasicStrategy
from game_engine import Hand, Card

class AutoPlayer:
    """Automated player that follows basic strategy perfectly"""
    
    def __init__(self, strategy: BasicStrategy):
        self.strategy = strategy
        self.is_active = False
        self.stop_event = Event()
        self.play_thread: Optional[Thread] = None
        self.action_callback: Optional[Callable] = None
        self.speed_ms = 1000  # Default 1 second between actions
        
    def set_action_callback(self, callback: Callable):
        """Set callback function to execute player actions"""
        self.action_callback = callback
        
    def set_speed(self, speed_ms: int):
        """Set auto-play speed in milliseconds"""
        self.speed_ms = max(100, speed_ms)  # Minimum 100ms
        
    def start_auto_play(self):
        """Start auto-play mode"""
        if self.is_active:
            return
            
        self.is_active = True
        self.stop_event.clear()
        self.play_thread = Thread(target=self._auto_play_loop, daemon=True)
        self.play_thread.start()
        
    def stop_auto_play(self):
        """Stop auto-play mode"""
        if not self.is_active:
            return
            
        self.is_active = False
        self.stop_event.set()
        if self.play_thread and self.play_thread.is_alive():
            self.play_thread.join(timeout=1.0)
            
    def get_optimal_action(self, player_hand: Hand, dealer_upcard: Card, 
                          can_double: bool = True, can_split: bool = True,
                          game_state=None) -> str:
        """Get optimal action using basic strategy"""
        return self.strategy.get_optimal_action(
            player_hand, dealer_upcard, can_double, can_split, game_state
        )
        
    def _auto_play_loop(self):
        """Main auto-play loop (runs in separate thread)"""
        while self.is_active and not self.stop_event.is_set():
            try:
                # Wait for the specified delay
                if self.stop_event.wait(self.speed_ms / 1000.0):
                    break  # Stop event was set
                    
                # Execute next action if callback is set
                if self.action_callback and self.is_active:
                    self.action_callback()
                    
            except Exception as e:
                print(f"Auto-play error: {e}")
                break
                
        self.is_active = False

class DifficultyLevel:
    """Manages different difficulty levels for practice"""
    
    DIFFICULTY_LEVELS = {
        'beginner': {
            'name': 'Beginner',
            'show_count': True,
            'show_true_count': True,
            'show_hints': True,
            'show_strategy_feedback': True,
            'show_ev': True,
            'show_bankroll': True,
            'auto_deal_available': True,
            'description': 'All information visible for learning'
        },
        'intermediate': {
            'name': 'Intermediate', 
            'show_count': True,
            'show_true_count': False,
            'show_hints': False,
            'show_strategy_feedback': True,
            'show_ev': True,
            'show_bankroll': True,
            'auto_deal_available': True,
            'description': 'True count hidden, calculate yourself'
        },
        'advanced': {
            'name': 'Advanced',
            'show_count': False,
            'show_true_count': False,
            'show_hints': False,
            'show_strategy_feedback': False,
            'show_ev': False,
            'show_bankroll': True,
            'auto_deal_available': False,
            'description': 'Count and strategy tracking hidden'
        },
        'expert': {
            'name': 'Expert',
            'show_count': False,
            'show_true_count': False,
            'show_hints': False,
            'show_strategy_feedback': False,
            'show_ev': False,
            'show_bankroll': False,
            'auto_deal_available': False,
            'description': 'Casino conditions - minimal information'
        }
    }
    
    def __init__(self, level: str = 'beginner'):
        self.current_level = level
        self.settings = self.DIFFICULTY_LEVELS.get(level, self.DIFFICULTY_LEVELS['beginner'])
        
    def set_level(self, level: str):
        """Change difficulty level"""
        if level in self.DIFFICULTY_LEVELS:
            self.current_level = level
            self.settings = self.DIFFICULTY_LEVELS[level]
            return True
        return False
        
    def get_level_names(self) -> list:
        """Get list of available difficulty levels"""
        return [self.DIFFICULTY_LEVELS[level]['name'] for level in self.DIFFICULTY_LEVELS.keys()]
        
    def get_level_descriptions(self) -> dict:
        """Get descriptions of all difficulty levels"""
        return {level: info['description'] for level, info in self.DIFFICULTY_LEVELS.items()}
        
    def should_show_count(self) -> bool:
        """Whether to show running count"""
        return self.settings['show_count']
        
    def should_show_true_count(self) -> bool:
        """Whether to show true count"""
        return self.settings['show_true_count']
        
    def should_show_hints(self) -> bool:
        """Whether to show strategy hints"""
        return self.settings['show_hints']
        
    def should_show_strategy_feedback(self) -> bool:
        """Whether to show strategy feedback"""
        return self.settings['show_strategy_feedback']
        
    def should_show_ev(self) -> bool:
        """Whether to show EV information"""
        return self.settings['show_ev']
        
    def should_show_bankroll(self) -> bool:
        """Whether to show bankroll"""
        return self.settings['show_bankroll']
        
    def auto_deal_available(self) -> bool:
        """Whether auto-deal is available at this level"""
        return self.settings['auto_deal_available']

class PracticeMode:
    """Manages practice mode functionality"""
    
    def __init__(self):
        self.auto_player = None
        self.difficulty = DifficultyLevel()
        self.session_stats = {
            'hands_played': 0,
            'correct_decisions': 0,
            'total_decisions': 0,
            'start_time': None,
            'end_time': None
        }
        
    def set_auto_player(self, auto_player: AutoPlayer):
        """Set the auto player instance"""
        self.auto_player = auto_player
        
    def start_practice_session(self):
        """Start a new practice session"""
        self.session_stats = {
            'hands_played': 0,
            'correct_decisions': 0,
            'total_decisions': 0,
            'start_time': time.time(),
            'end_time': None
        }
        
    def end_practice_session(self):
        """End current practice session"""
        self.session_stats['end_time'] = time.time()
        
    def record_decision(self, is_correct: bool):
        """Record a player decision"""
        self.session_stats['total_decisions'] += 1
        if is_correct:
            self.session_stats['correct_decisions'] += 1
            
    def record_hand_played(self):
        """Record a completed hand"""
        self.session_stats['hands_played'] += 1
        
    def get_session_summary(self) -> dict:
        """Get summary of current practice session"""
        total_decisions = self.session_stats['total_decisions']
        correct_decisions = self.session_stats['correct_decisions']
        
        accuracy = (correct_decisions / total_decisions * 100) if total_decisions > 0 else 0
        
        duration = 0
        if self.session_stats['start_time']:
            end_time = self.session_stats['end_time'] or time.time()
            duration = end_time - self.session_stats['start_time']
            
        return {
            'hands_played': self.session_stats['hands_played'],
            'total_decisions': total_decisions,
            'correct_decisions': correct_decisions,
            'accuracy_percentage': accuracy,
            'session_duration': duration,
            'hands_per_minute': (self.session_stats['hands_played'] / (duration / 60)) if duration > 0 else 0
        }
        
    def get_difficulty_level(self) -> str:
        """Get current difficulty level"""
        return self.difficulty.current_level
        
    def set_difficulty_level(self, level: str) -> bool:
        """Set difficulty level"""
        return self.difficulty.set_level(level)
        
    def apply_difficulty_settings(self, ui_components: dict):
        """Apply difficulty settings to UI components"""
        # This will be called to hide/show UI elements based on difficulty
        difficulty = self.difficulty
        
        # Count display
        if 'info_display' in ui_components:
            info_display = ui_components['info_display']
            if not difficulty.should_show_count():
                info_display.running_count_label.config(text="Running Count: ---")
                info_display.true_count_label.config(text="True Count: ---")
                info_display.count_visible = False
                
        # Strategy display
        if 'strategy_display' in ui_components:
            strategy_display = ui_components['strategy_display']
            if not difficulty.should_show_hints():
                strategy_display.hints_enabled = False
                strategy_display.hints_var.set(False)
                strategy_display.hints_toggle.config(state=tk.DISABLED)
            if not difficulty.should_show_strategy_feedback():
                strategy_display.feedback_label.config(text="")
                
        # EV and bankroll display
        if 'info_display' in ui_components:
            info_display = ui_components['info_display']
            if not difficulty.should_show_ev():
                info_display.ev_label.config(text="EV: ---")
            if not difficulty.should_show_bankroll():
                info_display.bankroll_label.config(text="Bankroll: ---")