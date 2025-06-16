"""UI components and widgets for the blackjack game"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, List, Tuple
from PIL import Image, ImageTk
import os
from config import *

class BlackjackTable:
    """Main game table canvas"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.canvas = tk.Canvas(
            parent, 
            width=WINDOW_WIDTH, 
            height=550, 
            bg=TABLE_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Card image cache
        self.card_images = {}
        self.card_back_image = None
        
        # Card display tracking
        self.dealer_card_ids = []
        self.player_card_ids = []
        
        self._draw_table()
    
    def _draw_table(self):
        """Draw the blackjack table felt"""
        # Main table semicircle
        self.canvas.create_arc(
            200, 100, 1000, 700,
            start=0, extent=180,
            fill=TABLE_FELT_COLOR,
            outline=TABLE_OUTLINE_COLOR,
            width=3,
            tags="table"
        )
        
        # Betting circle
        self.canvas.create_oval(
            575, 400, 625, 450,
            outline=TABLE_OUTLINE_COLOR,
            width=2,
            tags="betting_circle"
        )
        
        # Text labels
        self.canvas.create_text(
            600, 150, 
            text="DEALER", 
            font=SCORE_FONT,
            fill=TABLE_OUTLINE_COLOR,
            tags="label"
        )
        
        self.canvas.create_text(
            600, 500,
            text="PLAYER",
            font=SCORE_FONT,
            fill=TABLE_OUTLINE_COLOR,
            tags="label"
        )
        
        # Deck position indicator
        self.canvas.create_rectangle(
            DECK_POSITION[0], DECK_POSITION[1],
            DECK_POSITION[0] + CARD_WIDTH, DECK_POSITION[1] + CARD_HEIGHT,
            fill='darkgreen',
            outline=TABLE_OUTLINE_COLOR,
            width=2,
            tags="deck"
        )
    
    def load_card_images(self, cards_dir: str = CARDS_DIR):
        """Load all card images into memory"""
        # This will be implemented when we have card images
        # For now, we'll use text representations
        pass
    
    def display_card(self, card_text: str, x: int, y: int, 
                    face_down: bool = False) -> int:
        """Display a card on the table"""
        # Simple text-based card display for now
        if face_down:
            card_id = self.canvas.create_rectangle(
                x, y, x + CARD_WIDTH, y + CARD_HEIGHT,
                fill='darkred',
                outline='white',
                width=2,
                tags="card"
            )
        else:
            # Card background
            card_id = self.canvas.create_rectangle(
                x, y, x + CARD_WIDTH, y + CARD_HEIGHT,
                fill='white',
                outline='black',
                width=2,
                tags="card"
            )
            # Card text
            self.canvas.create_text(
                x + CARD_WIDTH//2, y + CARD_HEIGHT//2,
                text=card_text,
                font=('Arial', 24, 'bold'),
                fill='black' if card_text[1] in 'hd' else 'red',
                tags="card"
            )
        
        return card_id
    
    def clear_cards(self):
        """Remove all cards from the table"""
        self.canvas.delete("card")
        self.dealer_card_ids.clear()
        self.player_card_ids.clear()
    
    def update_dealer_cards(self, cards: List[Tuple[str, bool]]):
        """Update dealer's card display"""
        # Clear existing dealer cards
        for card_id in self.dealer_card_ids:
            self.canvas.delete(card_id)
        self.dealer_card_ids.clear()
        
        # Display new cards
        x_start = 600 - (len(cards) * (CARD_WIDTH + CARD_SPACING)) // 2
        for i, (card_text, face_down) in enumerate(cards):
            x = x_start + i * (CARD_WIDTH + CARD_SPACING)
            card_id = self.display_card(card_text, x, DEALER_CARD_Y, face_down)
            self.dealer_card_ids.append(card_id)
    
    def update_player_cards(self, cards: List[str]):
        """Update player's card display"""
        # Clear existing player cards
        for card_id in self.player_card_ids:
            self.canvas.delete(card_id)
        self.player_card_ids.clear()
        
        # Display new cards
        x_start = 600 - (len(cards) * (CARD_WIDTH + CARD_SPACING)) // 2
        for i, card_text in enumerate(cards):
            x = x_start + i * (CARD_WIDTH + CARD_SPACING)
            card_id = self.display_card(card_text, x, PLAYER_CARD_Y)
            self.player_card_ids.append(card_id)

class ControlPanel:
    """Panel containing game control buttons"""
    
    def __init__(self, parent: tk.Widget):
        self.frame = tk.Frame(parent, bg=TABLE_COLOR)
        self.frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Action buttons
        self.buttons = {}
        self._create_buttons()
    
    def _create_buttons(self):
        """Create game action buttons"""
        button_configs = [
            ("HIT", 0),
            ("STAND", 1),
            ("DOUBLE", 2),
            ("SPLIT", 3),
        ]
        
        for text, col in button_configs:
            btn = tk.Button(
                self.frame,
                text=text,
                font=BUTTON_FONT,
                bg=BUTTON_BG,
                fg=BUTTON_FG,
                activebackground=BUTTON_ACTIVE_BG,
                width=10,
                height=2,
                state=tk.DISABLED
            )
            btn.grid(row=0, column=col, padx=5)
            self.buttons[text.lower()] = btn
        
        # Bet controls frame
        self.bet_frame = tk.Frame(self.frame, bg=TABLE_COLOR)
        self.bet_frame.grid(row=0, column=4, padx=20)
        
        # Bet decrease button
        self.bet_decrease_btn = tk.Button(
            self.bet_frame,
            text="−",
            font=('Arial', 16, 'bold'),
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG,
            width=2,
            height=1
        )
        self.bet_decrease_btn.grid(row=0, column=0)
        
        # Bet display
        self.bet_label = tk.Label(
            self.bet_frame,
            text=f"Bet: ${DEFAULT_BET}",
            font=BUTTON_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR,
            width=10
        )
        self.bet_label.grid(row=0, column=1, padx=5)
        
        # Bet increase button
        self.bet_increase_btn = tk.Button(
            self.bet_frame,
            text="+",
            font=('Arial', 16, 'bold'),
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG,
            width=2,
            height=1
        )
        self.bet_increase_btn.grid(row=0, column=2)
    
    def set_button_command(self, button_name: str, command: Callable):
        """Set command for a button"""
        if button_name in self.buttons:
            self.buttons[button_name].config(command=command)
    
    def enable_buttons(self, *button_names):
        """Enable specified buttons"""
        for name in button_names:
            if name in self.buttons:
                self.buttons[name].config(state=tk.NORMAL)
    
    def disable_all_buttons(self):
        """Disable all action buttons"""
        for btn in self.buttons.values():
            btn.config(state=tk.DISABLED)
    
    def update_bet_display(self, amount: int):
        """Update bet amount display"""
        self.bet_label.config(text=f"Bet: ${amount}")
    
    def set_bet_commands(self, increase_cmd: Callable, decrease_cmd: Callable):
        """Set commands for bet adjustment buttons"""
        self.bet_increase_btn.config(command=increase_cmd)
        self.bet_decrease_btn.config(command=decrease_cmd)
    
    def enable_bet_controls(self):
        """Enable bet adjustment buttons"""
        self.bet_increase_btn.config(state=tk.NORMAL)
        self.bet_decrease_btn.config(state=tk.NORMAL)
    
    def disable_bet_controls(self):
        """Disable bet adjustment buttons during play"""
        self.bet_increase_btn.config(state=tk.DISABLED)
        self.bet_decrease_btn.config(state=tk.DISABLED)

class InfoDisplay:
    """Display panel for counts, EV, and statistics"""
    
    def __init__(self, parent: tk.Widget):
        self.frame = tk.Frame(parent, bg=TABLE_COLOR)
        self.frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Count display
        self.count_frame = tk.Frame(self.frame, bg=TABLE_COLOR)
        self.count_frame.grid(row=0, column=0, padx=10)
        
        self.running_count_label = tk.Label(
            self.count_frame,
            text="Running Count: 0",
            font=COUNT_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.running_count_label.pack()
        
        self.true_count_label = tk.Label(
            self.count_frame,
            text="True Count: 0.0",
            font=COUNT_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.true_count_label.pack()
        
        # Count visibility toggle
        self.count_visible = True
        self.toggle_button = tk.Button(
            self.count_frame,
            text="👁",
            font=('Arial', 16),
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            command=self.toggle_count_visibility
        )
        self.toggle_button.pack(pady=5)
        
        # Statistics display
        self.stats_frame = tk.Frame(self.frame, bg=TABLE_COLOR)
        self.stats_frame.grid(row=0, column=1, padx=10)
        
        self.ev_label = tk.Label(
            self.stats_frame,
            text="Actual EV: 0.0%",
            font=COUNT_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.ev_label.pack()
        
        self.bankroll_label = tk.Label(
            self.stats_frame,
            text=f"Bankroll: ${DEFAULT_BANKROLL}",
            font=COUNT_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.bankroll_label.pack()
    
    def toggle_count_visibility(self):
        """Toggle count display visibility"""
        self.count_visible = not self.count_visible
        if not self.count_visible:
            self.running_count_label.config(text="Running Count: ---")
            self.true_count_label.config(text="True Count: ---")
    
    def update_counts(self, running: int, true: float):
        """Update count displays if visible"""
        if self.count_visible:
            self.running_count_label.config(text=f"Running Count: {running:+d}")
            self.true_count_label.config(text=f"True Count: {true:+.1f}")
    
    def update_ev(self, ev_percentage: float):
        """Update EV display"""
        color = SUCCESS_COLOR if ev_percentage > 0 else ERROR_COLOR if ev_percentage < -2 else TEXT_COLOR
        self.ev_label.config(
            text=f"Actual EV: {ev_percentage:+.2f}%",
            fg=color
        )
    
    def update_bankroll(self, amount: float):
        """Update bankroll display"""
        self.bankroll_label.config(text=f"Bankroll: ${amount:.2f}")

class GameControls:
    """Additional game control buttons"""
    
    def __init__(self, parent: tk.Widget):
        self.frame = tk.Frame(parent, bg=TABLE_COLOR)
        self.frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Control buttons
        self.new_shoe_btn = tk.Button(
            self.frame,
            text="NEW SHOE",
            font=BUTTON_FONT,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG,
            width=12
        )
        self.new_shoe_btn.grid(row=0, column=0, padx=5)
        
        self.reset_count_btn = tk.Button(
            self.frame,
            text="RESET COUNT",
            font=BUTTON_FONT,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG,
            width=12
        )
        self.reset_count_btn.grid(row=0, column=1, padx=5)
        
        self.settings_btn = tk.Button(
            self.frame,
            text="SETTINGS",
            font=BUTTON_FONT,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG,
            width=12
        )
        self.settings_btn.grid(row=0, column=2, padx=5)
        
        # Hand info
        self.hand_info_label = tk.Label(
            self.frame,
            text="",
            font=COUNT_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.hand_info_label.grid(row=0, column=3, padx=20)
    
    def update_hand_info(self, dealer_value: Optional[int], 
                        player_value: Optional[int]):
        """Update hand value display"""
        if dealer_value is None and player_value is None:
            self.hand_info_label.config(text="")
            return
        
        dealer_text = f"Dealer: {dealer_value}" if dealer_value else "Dealer: ?"
        player_text = f"Player: {player_value}" if player_value else "Player: -"
        self.hand_info_label.config(text=f"{dealer_text}  |  {player_text}")

class MessageDisplay:
    """Display game messages and results"""
    
    def __init__(self, parent: tk.Widget):
        self.label = tk.Label(
            parent,
            text="Welcome to Blackjack Card Counter Trainer!",
            font=('Arial', 16, 'bold'),
            bg=TABLE_COLOR,
            fg=TEXT_COLOR,
            height=2
        )
        self.label.pack(fill=tk.X, padx=20, pady=5)
    
    def show_message(self, message: str, color: str = TEXT_COLOR):
        """Display a message"""
        self.label.config(text=message, fg=color)
    
    def clear(self):
        """Clear the message"""
        self.label.config(text="")

class StrategyDisplay:
    """Display basic strategy feedback and statistics"""
    
    def __init__(self, parent: tk.Widget):
        self.frame = tk.Frame(parent, bg=TABLE_COLOR)
        self.frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Hints mode toggle
        self.hints_enabled = False
        self.hints_var = tk.BooleanVar(value=False)
        self.hints_toggle = tk.Checkbutton(
            self.frame,
            text="Show Hints",
            font=MAIN_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR,
            selectcolor=TABLE_COLOR,
            activebackground=TABLE_COLOR,
            variable=self.hints_var,
            command=self.toggle_hints
        )
        self.hints_toggle.grid(row=0, column=0, padx=10)
        
        # Strategy adherence display
        self.adherence_label = tk.Label(
            self.frame,
            text="Strategy: 100.0%",
            font=COUNT_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.adherence_label.grid(row=0, column=1, padx=10)
        
        # Last action feedback
        self.feedback_label = tk.Label(
            self.frame,
            text="",
            font=('Arial', 12),
            bg=TABLE_COLOR,
            fg=TEXT_COLOR,
            width=40
        )
        self.feedback_label.grid(row=0, column=2, padx=10)
        
        # Hint display
        self.hint_label = tk.Label(
            self.frame,
            text="",
            font=('Arial', 14, 'bold'),
            bg=TABLE_COLOR,
            fg=SUCCESS_COLOR,
            width=30
        )
        self.hint_label.grid(row=1, column=0, columnspan=3, pady=5)
    
    def toggle_hints(self):
        """Toggle hints mode"""
        self.hints_enabled = self.hints_var.get()
        if not self.hints_enabled:
            self.hint_label.config(text="")
    
    def show_hint(self, optimal_action: str):
        """Show hint for optimal action"""
        if self.hints_enabled:
            action_text = {
                'hit': 'HIT',
                'stand': 'STAND',
                'double': 'DOUBLE DOWN',
                'split': 'SPLIT'
            }
            self.hint_label.config(
                text=f"Hint: {action_text.get(optimal_action, optimal_action.upper())}",
                fg=SUCCESS_COLOR
            )
    
    def clear_hint(self):
        """Clear hint display"""
        self.hint_label.config(text="")
    
    def update_adherence(self, percentage: float):
        """Update strategy adherence percentage"""
        color = SUCCESS_COLOR if percentage >= 95 else TEXT_COLOR if percentage >= 80 else ERROR_COLOR
        self.adherence_label.config(
            text=f"Strategy: {percentage:.1f}%",
            fg=color
        )
    
    def show_feedback(self, is_correct: bool, player_action: str, optimal_action: str = None):
        """Show feedback on last action"""
        if is_correct:
            self.feedback_label.config(
                text="✓ Correct play!",
                fg=SUCCESS_COLOR
            )
        else:
            if optimal_action:
                action_text = {
                    'hit': 'hit',
                    'stand': 'stand',
                    'double': 'double',
                    'split': 'split'
                }
                self.feedback_label.config(
                    text=f"✗ You: {action_text.get(player_action, player_action)}, "
                         f"Optimal: {action_text.get(optimal_action, optimal_action)}",
                    fg=ERROR_COLOR
                )
            else:
                self.feedback_label.config(text="", fg=TEXT_COLOR)
    
    def clear_feedback(self):
        """Clear feedback display"""
        self.feedback_label.config(text="")