"""Main entry point for Blackjack Card Counter Trainer"""

import tkinter as tk
from tkinter import messagebox
import sys
from typing import Optional

from config import *
from game_engine import GameState, GameRules
from card_counting import CardCounter
from ev_calculator import EVCalculator
from basic_strategy import StrategyTracker
from ui_components import (
    BlackjackTable, ControlPanel, InfoDisplay, 
    GameControls, MessageDisplay, StrategyDisplay
)
from session_stats_display import SessionStatsDisplay

class BlackjackGame:
    """Main application class that coordinates game logic and UI"""
    
    def __init__(self):
        # Initialize Tkinter root
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.root.resizable(True, True)  # Allow resizing if needed
        self.root.configure(bg=TABLE_COLOR)
        
        # Initialize game components
        self.game_state = GameState()
        self.counter = CardCounter()
        self.ev_calculator = EVCalculator()
        self.strategy_tracker = StrategyTracker()
        
        # Setup UI
        self._setup_ui()
        self._setup_bindings()
        
        # Start with a fresh shoe
        self.new_shoe()
    
    def _setup_ui(self):
        """Initialize all UI components"""
        # Message display at top
        self.message_display = MessageDisplay(self.root)
        
        # Main game table
        self.table = BlackjackTable(self.root)
        
        # Control panels
        self.control_panel = ControlPanel(self.root)
        self.info_display = InfoDisplay(self.root)
        self.strategy_display = StrategyDisplay(self.root)
        self.session_stats_display = SessionStatsDisplay(self.root)
        self.game_controls = GameControls(self.root)
        
        # Wire up button commands
        self.control_panel.set_button_command('hit', self.player_hit)
        self.control_panel.set_button_command('stand', self.player_stand)
        self.control_panel.set_button_command('double', self.player_double)
        self.control_panel.set_button_command('split', self.player_split)
        
        # Wire up bet controls
        self.control_panel.set_bet_commands(self.increase_bet, self.decrease_bet)
        
        self.game_controls.new_shoe_btn.config(command=self.new_shoe)
        self.game_controls.reset_count_btn.config(command=self.reset_count)
        self.game_controls.settings_btn.config(command=self.show_settings)
    
    def _setup_bindings(self):
        """Setup keyboard bindings"""
        self.root.bind('h', lambda e: self.player_hit())
        self.root.bind('s', lambda e: self.player_stand())
        self.root.bind('d', lambda e: self.player_double())
        self.root.bind('n', lambda e: self.new_hand())
        self.root.bind('<space>', lambda e: self.new_hand())
        self.root.bind('<Escape>', lambda e: self.root.quit())
    
    def new_shoe(self):
        """Start a new shoe"""
        self.game_state.shoe.shuffle()
        self.counter.reset()
        self.table.clear_cards()
        self.control_panel.disable_all_buttons()
        self.control_panel.enable_bet_controls()  # Allow bet adjustment between hands
        self.message_display.show_message("New shoe shuffled! Press SPACE to deal.")
        self.update_displays()
    
    def reset_count(self):
        """Reset the running count"""
        response = messagebox.askyesno(
            "Reset Count", 
            "Are you sure you want to reset the count and strategy tracking?"
        )
        if response:
            self.counter.reset()
            self.strategy_tracker.reset_tracking()
            self.update_displays()
            self.strategy_display.update_adherence(100.0)
            self.strategy_display.clear_feedback()
            self.message_display.show_message("Count and strategy tracking reset")
    
    def show_settings(self):
        """Show settings dialog (placeholder for now)"""
        messagebox.showinfo("Settings", "Settings dialog coming soon!")
    
    def increase_bet(self):
        """Increase bet size"""
        if self.game_state.phase != "betting":
            return
        
        # Increase by minimum bet increments
        new_bet = self.game_state.current_bet + MIN_BET
        
        # Check maximum bet and bankroll limits
        if new_bet > MAX_BET:
            new_bet = MAX_BET
        if new_bet > self.game_state.bankroll:
            new_bet = int(self.game_state.bankroll)
        
        self.game_state.current_bet = new_bet
        self.control_panel.update_bet_display(new_bet)
    
    def decrease_bet(self):
        """Decrease bet size"""
        if self.game_state.phase != "betting":
            return
        
        # Decrease by minimum bet increments
        new_bet = self.game_state.current_bet - MIN_BET
        
        # Check minimum bet
        if new_bet < MIN_BET:
            new_bet = MIN_BET
        
        self.game_state.current_bet = new_bet
        self.control_panel.update_bet_display(new_bet)
    
    def new_hand(self):
        """Deal a new hand"""
        if self.game_state.phase != "betting" and self.game_state.phase != "complete":
            return
        
        # Check for shuffle needed
        if self.game_state.shoe.needs_shuffle:
            self.message_display.show_message("Penetration reached. Shuffling...", ERROR_COLOR)
            self.new_shoe()
            return
        
        # Start new hand
        self.game_state.start_new_hand(self.game_state.current_bet)
        
        # Disable bet controls during play
        self.control_panel.disable_bet_controls()
        
        # Update counter with dealt cards
        for card in self.game_state.player_hand.cards:
            self.counter.update_count(card)
        # Only count dealer's up card
        self.counter.update_count(self.game_state.dealer_hand.cards[0])
        
        # Update displays
        self.update_displays()
        self.display_hands()
        
        # Check for blackjacks
        if self.game_state.phase == "complete":
            self.complete_hand()
        else:
            # Enable appropriate buttons
            self.control_panel.enable_buttons('hit', 'stand')
            can_double = self.game_state.player_hand.can_double()
            can_split = self.game_state.player_hand.can_split()
            
            if can_double:
                self.control_panel.enable_buttons('double')
            if can_split:
                self.control_panel.enable_buttons('split')
            
            # Show hint if enabled
            if self.strategy_display.hints_enabled:
                optimal_action = self.strategy_tracker.strategy.get_optimal_action(
                    self.game_state.player_hand,
                    self.game_state.dealer_hand.cards[0],
                    can_double,
                    can_split
                )
                game_action = self.strategy_tracker.strategy.action_to_game_action(optimal_action)
                self.strategy_display.show_hint(game_action)
            
            self.message_display.clear()
            self.strategy_display.clear_feedback()
    
    def player_hit(self):
        """Handle player hit action"""
        if self.game_state.phase != "playing":
            return
        
        # Track decision before hitting
        is_correct, optimal = self.strategy_tracker.record_decision(
            self.game_state.player_hand,
            self.game_state.dealer_hand.cards[0],
            'hit',
            self.game_state.player_hand.can_double(),
            self.game_state.player_hand.can_split()
        )
        
        # Show feedback
        self.strategy_display.show_feedback(is_correct, 'hit', optimal)
        self.strategy_display.update_adherence(
            self.strategy_tracker.get_adherence_percentage()
        )
        
        self.game_state.player_hit()
        
        # Update count with new card
        new_card = self.game_state.player_hand.cards[-1]
        self.counter.update_count(new_card)
        
        # Update displays
        self.update_displays()
        self.display_hands()
        
        if self.game_state.player_hand.is_bust:
            self.strategy_display.clear_hint()
            self.complete_hand()
        else:
            # Disable double/split after first hit
            self.control_panel.buttons['double'].config(state=tk.DISABLED)
            self.control_panel.buttons['split'].config(state=tk.DISABLED)
            
            # Show new hint if enabled
            if self.strategy_display.hints_enabled:
                optimal_action = self.strategy_tracker.strategy.get_optimal_action(
                    self.game_state.player_hand,
                    self.game_state.dealer_hand.cards[0],
                    False,  # Can't double after hit
                    False   # Can't split after hit
                )
                game_action = self.strategy_tracker.strategy.action_to_game_action(optimal_action)
                self.strategy_display.show_hint(game_action)
    
    def player_stand(self):
        """Handle player stand action"""
        if self.game_state.phase != "playing":
            return
        
        # Track decision before standing
        is_correct, optimal = self.strategy_tracker.record_decision(
            self.game_state.player_hand,
            self.game_state.dealer_hand.cards[0],
            'stand',
            self.game_state.player_hand.can_double(),
            self.game_state.player_hand.can_split()
        )
        
        # Show feedback
        self.strategy_display.show_feedback(is_correct, 'stand', optimal)
        self.strategy_display.update_adherence(
            self.strategy_tracker.get_adherence_percentage()
        )
        self.strategy_display.clear_hint()
        
        self.control_panel.disable_all_buttons()
        self.game_state.player_stand()
        
        # Count dealer's hole card
        self.counter.update_count(self.game_state.dealer_hand.cards[1])
        
        # Count any additional dealer cards
        for i in range(2, len(self.game_state.dealer_hand.cards)):
            self.counter.update_count(self.game_state.dealer_hand.cards[i])
        
        # Update displays and complete hand
        self.update_displays()
        self.display_hands(show_hole_card=True)
        self.complete_hand()
    
    def player_double(self):
        """Handle player double down"""
        if self.game_state.phase != "playing":
            return
        
        # Track decision before doubling
        is_correct, optimal = self.strategy_tracker.record_decision(
            self.game_state.player_hand,
            self.game_state.dealer_hand.cards[0],
            'double',
            True,  # We know we can double or we wouldn't be here
            self.game_state.player_hand.can_split()
        )
        
        # Show feedback
        self.strategy_display.show_feedback(is_correct, 'double', optimal)
        self.strategy_display.update_adherence(
            self.strategy_tracker.get_adherence_percentage()
        )
        self.strategy_display.clear_hint()
        
        if not self.game_state.player_double():
            self.message_display.show_message("Cannot double!", ERROR_COLOR)
            return
        
        # Update count with new card
        new_card = self.game_state.player_hand.cards[-1]
        self.counter.update_count(new_card)
        
        # If not bust, dealer plays
        if not self.game_state.player_hand.is_bust:
            # Count dealer's hole card
            self.counter.update_count(self.game_state.dealer_hand.cards[1])
            
            # Count any additional dealer cards
            for i in range(2, len(self.game_state.dealer_hand.cards)):
                self.counter.update_count(self.game_state.dealer_hand.cards[i])
        
        # Update displays
        self.control_panel.disable_all_buttons()
        self.update_displays()
        self.display_hands(show_hole_card=True)
        self.complete_hand()
    
    def player_split(self):
        """Handle player split (placeholder for now)"""
        self.message_display.show_message("Split functionality coming soon!", ERROR_COLOR)
    
    def complete_hand(self):
        """Complete the hand and show results"""
        outcome, profit = self.game_state.complete_hand()
        
        # Update EV tracking
        true_count = self.counter.get_true_count(self.game_state.shoe.cards_remaining())
        self.ev_calculator.update_session_ev(
            self.game_state.current_bet, true_count, profit
        )
        
        # Display outcome
        color = SUCCESS_COLOR if profit > 0 else ERROR_COLOR if profit < 0 else TEXT_COLOR
        profit_text = f" (${profit:+.2f})" if profit != 0 else ""
        self.message_display.show_message(f"{outcome}{profit_text}", color)
        
        # Update displays
        self.control_panel.disable_all_buttons()
        self.update_displays()
        
        # Reset for next hand
        self.game_state.phase = "betting"
        
        # Re-enable bet controls
        self.control_panel.enable_bet_controls()
    
    def display_hands(self, show_hole_card: bool = False):
        """Update card display on table"""
        # Player cards
        player_cards = [f"{card.rank}{card.suit[0]}" 
                       for card in self.game_state.player_hand.cards]
        self.table.update_player_cards(player_cards)
        
        # Dealer cards
        dealer_cards = []
        for i, card in enumerate(self.game_state.dealer_hand.cards):
            if i == 1 and not show_hole_card:
                dealer_cards.append(("??", True))  # Face down
            else:
                dealer_cards.append((f"{card.rank}{card.suit[0]}", False))
        self.table.update_dealer_cards(dealer_cards)
        
        # Update hand values
        dealer_value = (self.game_state.dealer_hand.value 
                       if show_hole_card 
                       else self.game_state.dealer_hand.cards[0].value)
        player_value = self.game_state.player_hand.value
        
        self.game_controls.update_hand_info(dealer_value, player_value)
    
    def update_displays(self):
        """Update all information displays"""
        # Count displays
        running = self.counter.get_running_count()
        true = self.counter.get_true_count(self.game_state.shoe.cards_remaining())
        self.info_display.update_counts(running, true)
        
        # EV display - now shows ACTUAL EV not theoretical
        actual_ev = self.ev_calculator.session_stats.get_actual_ev_percentage()
        self.info_display.update_ev(actual_ev)
        
        # Bankroll display
        self.info_display.update_bankroll(self.game_state.bankroll)
        
        # Bet display
        self.control_panel.update_bet_display(self.game_state.current_bet)
        
        # Update session statistics
        game_stats = self.game_state.get_session_stats()
        ev_stats = self.ev_calculator.session_stats.get_session_summary()
        self.session_stats_display.update_stats(game_stats, ev_stats)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        game = BlackjackGame()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()