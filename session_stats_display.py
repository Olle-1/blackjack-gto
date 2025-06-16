"""Session statistics display component"""

import tkinter as tk
from typing import Dict, Optional
from config import *

class SessionStatsDisplay:
    """Display comprehensive session statistics"""
    
    def __init__(self, parent: tk.Widget):
        self.frame = tk.LabelFrame(
            parent, 
            text="Session Statistics",
            font=('Arial', 12, 'bold'),
            bg=TABLE_COLOR,
            fg=TEXT_COLOR,
            relief=tk.RIDGE,
            borderwidth=2
        )
        self.frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Create two columns for stats
        self.left_frame = tk.Frame(self.frame, bg=TABLE_COLOR)
        self.left_frame.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        
        self.right_frame = tk.Frame(self.frame, bg=TABLE_COLOR)
        self.right_frame.grid(row=0, column=1, padx=20, pady=10, sticky='w')
        
        # Left column stats
        self.hands_label = tk.Label(
            self.left_frame,
            text="Hands Played: 0",
            font=MAIN_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.hands_label.grid(row=0, column=0, sticky='w')
        
        self.win_loss_label = tk.Label(
            self.left_frame,
            text="W/L/P: 0/0/0",
            font=MAIN_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.win_loss_label.grid(row=1, column=0, sticky='w')
        
        self.win_pct_label = tk.Label(
            self.left_frame,
            text="Win %: 0.0%",
            font=MAIN_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.win_pct_label.grid(row=2, column=0, sticky='w')
        
        self.blackjacks_label = tk.Label(
            self.left_frame,
            text="Blackjacks: 0",
            font=MAIN_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.blackjacks_label.grid(row=3, column=0, sticky='w')
        
        # Right column stats
        self.profit_loss_label = tk.Label(
            self.right_frame,
            text="P/L: $0.00",
            font=MAIN_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.profit_loss_label.grid(row=0, column=0, sticky='w')
        
        self.avg_bet_label = tk.Label(
            self.right_frame,
            text="Avg Bet: $0.00",
            font=MAIN_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.avg_bet_label.grid(row=1, column=0, sticky='w')
        
        self.actual_ev_label = tk.Label(
            self.right_frame,
            text="Actual EV: 0.0%",
            font=MAIN_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.actual_ev_label.grid(row=2, column=0, sticky='w')
        
        self.expected_ev_label = tk.Label(
            self.right_frame,
            text="Expected EV: 0.0%",
            font=MAIN_FONT,
            bg=TABLE_COLOR,
            fg=TEXT_COLOR
        )
        self.expected_ev_label.grid(row=3, column=0, sticky='w')
    
    def update_stats(self, game_stats: Dict, ev_stats: Optional[Dict] = None):
        """Update all statistics displays"""
        # Update left column
        self.hands_label.config(text=f"Hands Played: {game_stats['hands_played']}")
        
        self.win_loss_label.config(
            text=f"W/L/P: {game_stats['wins']}/{game_stats['losses']}/{game_stats['pushes']}"
        )
        
        win_pct = game_stats['win_percentage']
        color = SUCCESS_COLOR if win_pct > 50 else ERROR_COLOR if win_pct < 45 else TEXT_COLOR
        self.win_pct_label.config(
            text=f"Win %: {win_pct:.1f}%",
            fg=color
        )
        
        self.blackjacks_label.config(text=f"Blackjacks: {game_stats['blackjacks']}")
        
        # Update right column
        profit = game_stats['profit_loss']
        color = SUCCESS_COLOR if profit > 0 else ERROR_COLOR if profit < 0 else TEXT_COLOR
        self.profit_loss_label.config(
            text=f"P/L: ${profit:+.2f}",
            fg=color
        )
        
        self.avg_bet_label.config(
            text=f"Avg Bet: ${game_stats['average_bet']:.2f}"
        )
        
        # Update EV stats if provided
        if ev_stats:
            actual_ev = ev_stats.get('actual_ev_percentage', 0.0)
            expected_ev = ev_stats.get('expected_ev_percentage', 0.0)
            
            # Actual EV coloring
            color = SUCCESS_COLOR if actual_ev > 0 else ERROR_COLOR if actual_ev < -2 else TEXT_COLOR
            self.actual_ev_label.config(
                text=f"Actual EV: {actual_ev:+.2f}%",
                fg=color
            )
            
            # Expected EV
            self.expected_ev_label.config(
                text=f"Expected EV: {expected_ev:+.2f}%"
            )
    
    def reset_stats(self):
        """Reset all statistics displays"""
        self.hands_label.config(text="Hands Played: 0")
        self.win_loss_label.config(text="W/L/P: 0/0/0")
        self.win_pct_label.config(text="Win %: 0.0%", fg=TEXT_COLOR)
        self.blackjacks_label.config(text="Blackjacks: 0")
        self.profit_loss_label.config(text="P/L: $0.00", fg=TEXT_COLOR)
        self.avg_bet_label.config(text="Avg Bet: $0.00")
        self.actual_ev_label.config(text="Actual EV: 0.0%", fg=TEXT_COLOR)
        self.expected_ev_label.config(text="Expected EV: 0.0%")