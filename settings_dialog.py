"""Settings dialog for configuring game options"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from settings import Settings

class SettingsDialog:
    """Settings configuration dialog window"""
    
    def __init__(self, parent: tk.Tk, settings: Settings, on_save_callback: Optional[Callable] = None):
        self.parent = parent
        self.settings = settings
        self.on_save_callback = on_save_callback
        self.dialog = None
        
        # Track if settings were changed
        self.settings_changed = False
        
        # Create a copy of settings to work with
        self.temp_settings = Settings()
        self.temp_settings.from_dict(settings.to_dict())
        
    def show(self):
        """Display the settings dialog"""
        if self.dialog is not None:
            self.dialog.lift()
            return
            
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Game Settings")
        self.dialog.geometry("800x700")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(self.dialog)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self._create_game_rules_tab()
        self._create_betting_tab()
        self._create_shoe_tab()
        self._create_practice_tab()
        self._create_display_tab()
        self._create_counting_tab()
        
        # Button frame
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Buttons
        tk.Button(button_frame, text="Save", command=self._save_settings,
                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                 width=10).pack(side="right", padx=5)
        tk.Button(button_frame, text="Cancel", command=self._cancel,
                 bg="#e74c3c", fg="white", font=("Arial", 12),
                 width=10).pack(side="right", padx=5)
        tk.Button(button_frame, text="Reset to Defaults", command=self._reset_defaults,
                 bg="#95a5a6", fg="white", font=("Arial", 12),
                 width=15).pack(side="right", padx=5)
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self._cancel)
        
    def _create_game_rules_tab(self):
        """Create the game rules configuration tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Game Rules")
        
        # Create scrollable frame
        canvas = tk.Canvas(frame, bg="white")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Dealer Rules Section
        dealer_frame = ttk.LabelFrame(scrollable_frame, text="Dealer Rules", padding=10)
        dealer_frame.pack(fill="x", padx=10, pady=5)
        
        self.stand_soft_17_var = tk.BooleanVar(value=self.temp_settings.game_rules.dealer_stand_soft_17)
        ttk.Checkbutton(dealer_frame, text="Dealer stands on soft 17",
                       variable=self.stand_soft_17_var).pack(anchor="w")
        
        # Payout Rules
        payout_frame = ttk.LabelFrame(scrollable_frame, text="Payouts", padding=10)
        payout_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(payout_frame, text="Blackjack payout:").grid(row=0, column=0, sticky="w", padx=5)
        self.blackjack_payout_var = tk.StringVar(value=f"{self.temp_settings.game_rules.blackjack_payout}:1")
        payout_combo = ttk.Combobox(payout_frame, textvariable=self.blackjack_payout_var,
                                   values=["1.5:1", "1.2:1", "1:1"], width=10, state="readonly")
        payout_combo.grid(row=0, column=1, padx=5)
        
        # Surrender Rules
        surrender_frame = ttk.LabelFrame(scrollable_frame, text="Surrender Options", padding=10)
        surrender_frame.pack(fill="x", padx=10, pady=5)
        
        self.surrender_allowed_var = tk.BooleanVar(value=self.temp_settings.game_rules.surrender_allowed)
        ttk.Checkbutton(surrender_frame, text="Surrender allowed",
                       variable=self.surrender_allowed_var,
                       command=self._toggle_surrender_options).pack(anchor="w")
        
        self.late_surrender_var = tk.BooleanVar(value=self.temp_settings.game_rules.late_surrender_only)
        self.late_surrender_check = ttk.Checkbutton(surrender_frame, text="Late surrender only",
                                                   variable=self.late_surrender_var)
        self.late_surrender_check.pack(anchor="w", padx=20)
        if not self.surrender_allowed_var.get():
            self.late_surrender_check.config(state="disabled")
        
        # Splitting Rules
        split_frame = ttk.LabelFrame(scrollable_frame, text="Splitting Rules", padding=10)
        split_frame.pack(fill="x", padx=10, pady=5)
        
        self.double_after_split_var = tk.BooleanVar(value=self.temp_settings.game_rules.double_after_split)
        ttk.Checkbutton(split_frame, text="Double after split allowed",
                       variable=self.double_after_split_var).pack(anchor="w")
        
        self.resplit_aces_var = tk.BooleanVar(value=self.temp_settings.game_rules.resplit_aces)
        ttk.Checkbutton(split_frame, text="Re-split aces allowed",
                       variable=self.resplit_aces_var).pack(anchor="w")
        
        ttk.Label(split_frame, text="Maximum splits:").pack(anchor="w", pady=(10, 0))
        self.max_splits_var = tk.IntVar(value=self.temp_settings.game_rules.max_splits)
        splits_scale = ttk.Scale(split_frame, from_=0, to=4, orient="horizontal",
                                variable=self.max_splits_var, length=200)
        splits_scale.pack(anchor="w", padx=20)
        self.splits_label = ttk.Label(split_frame, text=f"{self.max_splits_var.get()}")
        self.splits_label.pack(anchor="w", padx=20)
        
        # Update label when scale changes
        def update_splits_label(val):
            self.splits_label.config(text=f"{int(float(val))}")
        splits_scale.config(command=update_splits_label)
        
        # Doubling Rules
        double_frame = ttk.LabelFrame(scrollable_frame, text="Doubling Rules", padding=10)
        double_frame.pack(fill="x", padx=10, pady=5)
        
        self.double_any_two_var = tk.BooleanVar(value=self.temp_settings.game_rules.double_on_any_two)
        ttk.Checkbutton(double_frame, text="Double on any two cards",
                       variable=self.double_any_two_var).pack(anchor="w")
        
        # Insurance
        insurance_frame = ttk.LabelFrame(scrollable_frame, text="Insurance", padding=10)
        insurance_frame.pack(fill="x", padx=10, pady=5)
        
        self.insurance_allowed_var = tk.BooleanVar(value=self.temp_settings.game_rules.insurance_allowed)
        ttk.Checkbutton(insurance_frame, text="Insurance allowed",
                       variable=self.insurance_allowed_var).pack(anchor="w")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def _create_betting_tab(self):
        """Create the betting limits configuration tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Betting")
        
        # Betting Limits
        limits_frame = ttk.LabelFrame(frame, text="Betting Limits", padding=10)
        limits_frame.pack(fill="x", padx=10, pady=10)
        
        # Min bet
        ttk.Label(limits_frame, text="Minimum bet: $").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.min_bet_var = tk.IntVar(value=self.temp_settings.betting_limits.min_bet)
        min_bet_spin = ttk.Spinbox(limits_frame, from_=1, to=100, textvariable=self.min_bet_var, width=10)
        min_bet_spin.grid(row=0, column=1, padx=5, pady=5)
        
        # Max bet
        ttk.Label(limits_frame, text="Maximum bet: $").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.max_bet_var = tk.IntVar(value=self.temp_settings.betting_limits.max_bet)
        max_bet_spin = ttk.Spinbox(limits_frame, from_=10, to=10000, textvariable=self.max_bet_var, width=10)
        max_bet_spin.grid(row=1, column=1, padx=5, pady=5)
        
        # Default bet
        ttk.Label(limits_frame, text="Default bet: $").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.default_bet_var = tk.IntVar(value=self.temp_settings.betting_limits.default_bet)
        default_bet_spin = ttk.Spinbox(limits_frame, from_=1, to=1000, textvariable=self.default_bet_var, width=10)
        default_bet_spin.grid(row=2, column=1, padx=5, pady=5)
        
        # Bet increment
        ttk.Label(limits_frame, text="Bet increment: $").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.bet_increment_var = tk.IntVar(value=self.temp_settings.betting_limits.bet_increment)
        increment_spin = ttk.Spinbox(limits_frame, from_=1, to=100, textvariable=self.bet_increment_var, width=10)
        increment_spin.grid(row=3, column=1, padx=5, pady=5)
        
        # Starting Bankroll
        bankroll_frame = ttk.LabelFrame(frame, text="Starting Bankroll", padding=10)
        bankroll_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(bankroll_frame, text="Default bankroll: $").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.default_bankroll_var = tk.IntVar(value=self.temp_settings.betting_limits.default_bankroll)
        bankroll_spin = ttk.Spinbox(bankroll_frame, from_=100, to=100000, 
                                   textvariable=self.default_bankroll_var, width=15)
        bankroll_spin.grid(row=0, column=1, padx=5, pady=5)
        
    def _create_shoe_tab(self):
        """Create the shoe configuration tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Shoe")
        
        # Deck Configuration
        deck_frame = ttk.LabelFrame(frame, text="Deck Configuration", padding=10)
        deck_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(deck_frame, text="Number of decks:").pack(anchor="w")
        self.num_decks_var = tk.IntVar(value=self.temp_settings.shoe_config.num_decks)
        decks_scale = ttk.Scale(deck_frame, from_=1, to=8, orient="horizontal",
                               variable=self.num_decks_var, length=300)
        decks_scale.pack(fill="x", padx=20, pady=5)
        self.decks_label = ttk.Label(deck_frame, text=f"{self.num_decks_var.get()} decks")
        self.decks_label.pack(anchor="w", padx=20)
        
        def update_decks_label(val):
            num = int(float(val))
            self.decks_label.config(text=f"{num} deck{'s' if num > 1 else ''}")
        decks_scale.config(command=update_decks_label)
        
        # Penetration
        penetration_frame = ttk.LabelFrame(frame, text="Penetration", padding=10)
        penetration_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(penetration_frame, text="Deal percentage before shuffle:").pack(anchor="w")
        self.penetration_var = tk.DoubleVar(value=self.temp_settings.shoe_config.penetration)
        pen_scale = ttk.Scale(penetration_frame, from_=0.5, to=0.9, orient="horizontal",
                             variable=self.penetration_var, length=300)
        pen_scale.pack(fill="x", padx=20, pady=5)
        self.pen_label = ttk.Label(penetration_frame, 
                                  text=f"{int(self.penetration_var.get() * 100)}%")
        self.pen_label.pack(anchor="w", padx=20)
        
        def update_pen_label(val):
            self.pen_label.config(text=f"{int(float(val) * 100)}%")
        pen_scale.config(command=update_pen_label)
        
        # Other Options
        other_frame = ttk.LabelFrame(frame, text="Other Options", padding=10)
        other_frame.pack(fill="x", padx=10, pady=10)
        
        self.burn_card_var = tk.BooleanVar(value=self.temp_settings.shoe_config.burn_card)
        ttk.Checkbutton(other_frame, text="Burn first card after shuffle",
                       variable=self.burn_card_var).pack(anchor="w")
        
    def _create_practice_tab(self):
        """Create the practice modes tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Practice")
        
        # Auto-play Options
        auto_frame = ttk.LabelFrame(frame, text="Auto-play Options", padding=10)
        auto_frame.pack(fill="x", padx=10, pady=10)
        
        self.auto_deal_var = tk.BooleanVar(value=self.temp_settings.practice_modes.auto_deal)
        ttk.Checkbutton(auto_frame, text="Auto-deal new hands",
                       variable=self.auto_deal_var,
                       command=self._toggle_auto_deal).pack(anchor="w")
        
        delay_frame = tk.Frame(auto_frame)
        delay_frame.pack(anchor="w", padx=20, pady=5)
        ttk.Label(delay_frame, text="Delay between hands:").pack(side="left")
        self.auto_delay_var = tk.DoubleVar(value=self.temp_settings.practice_modes.auto_deal_delay)
        self.delay_spin = ttk.Spinbox(delay_frame, from_=0.5, to=10, increment=0.5,
                                     textvariable=self.auto_delay_var, width=8)
        self.delay_spin.pack(side="left", padx=5)
        ttk.Label(delay_frame, text="seconds").pack(side="left")
        
        if not self.auto_deal_var.get():
            self.delay_spin.config(state="disabled")
        
        # Training Aids
        aids_frame = ttk.LabelFrame(frame, text="Training Aids", padding=10)
        aids_frame.pack(fill="x", padx=10, pady=10)
        
        self.show_hints_var = tk.BooleanVar(value=self.temp_settings.practice_modes.show_hints_default)
        ttk.Checkbutton(aids_frame, text="Show strategy hints by default",
                       variable=self.show_hints_var).pack(anchor="w")
        
        self.show_count_var = tk.BooleanVar(value=self.temp_settings.practice_modes.show_count_default)
        ttk.Checkbutton(aids_frame, text="Show count by default",
                       variable=self.show_count_var).pack(anchor="w")
        
        self.warn_mistakes_var = tk.BooleanVar(value=self.temp_settings.practice_modes.warn_on_mistakes)
        ttk.Checkbutton(aids_frame, text="Warn on strategy mistakes",
                       variable=self.warn_mistakes_var).pack(anchor="w")
        
        # Information Display
        info_frame = ttk.LabelFrame(frame, text="Information Display", padding=10)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        self.show_running_var = tk.BooleanVar(value=self.temp_settings.practice_modes.show_running_count)
        ttk.Checkbutton(info_frame, text="Show running count",
                       variable=self.show_running_var).pack(anchor="w")
        
        self.show_true_var = tk.BooleanVar(value=self.temp_settings.practice_modes.show_true_count)
        ttk.Checkbutton(info_frame, text="Show true count",
                       variable=self.show_true_var).pack(anchor="w")
        
        self.show_ev_var = tk.BooleanVar(value=self.temp_settings.practice_modes.show_ev)
        ttk.Checkbutton(info_frame, text="Show expected value",
                       variable=self.show_ev_var).pack(anchor="w")
        
        self.show_feedback_var = tk.BooleanVar(value=self.temp_settings.practice_modes.show_strategy_feedback)
        ttk.Checkbutton(info_frame, text="Show strategy feedback",
                       variable=self.show_feedback_var).pack(anchor="w")
        
    def _create_display_tab(self):
        """Create the display preferences tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Display")
        
        # Card Display
        card_frame = ttk.LabelFrame(frame, text="Card Display", padding=10)
        card_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(card_frame, text="Card style:").pack(anchor="w")
        self.card_style_var = tk.StringVar(value=self.temp_settings.display_prefs.card_style)
        ttk.Radiobutton(card_frame, text="Text cards", variable=self.card_style_var,
                       value="text").pack(anchor="w", padx=20)
        ttk.Radiobutton(card_frame, text="Image cards (if available)", 
                       variable=self.card_style_var, value="images").pack(anchor="w", padx=20)
        
        # Advanced Display
        advanced_frame = ttk.LabelFrame(frame, text="Advanced Options", padding=10)
        advanced_frame.pack(fill="x", padx=10, pady=10)
        
        self.show_probs_var = tk.BooleanVar(value=self.temp_settings.display_prefs.show_probabilities)
        ttk.Checkbutton(advanced_frame, text="Show hand probabilities",
                       variable=self.show_probs_var).pack(anchor="w")
        
        self.show_hole_var = tk.BooleanVar(value=self.temp_settings.display_prefs.show_dealer_hole_card)
        ttk.Checkbutton(advanced_frame, text="Show dealer hole card (practice mode)",
                       variable=self.show_hole_var).pack(anchor="w")
        
        # Effects
        effects_frame = ttk.LabelFrame(frame, text="Effects", padding=10)
        effects_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(effects_frame, text="Animation speed:").pack(anchor="w")
        self.animation_var = tk.DoubleVar(value=self.temp_settings.display_prefs.animation_speed)
        anim_scale = ttk.Scale(effects_frame, from_=0, to=1, orient="horizontal",
                              variable=self.animation_var, length=300)
        anim_scale.pack(fill="x", padx=20, pady=5)
        self.anim_label = ttk.Label(effects_frame, text="")
        self.anim_label.pack(anchor="w", padx=20)
        
        def update_anim_label(val):
            speed = float(val)
            if speed == 0:
                text = "Instant (no animation)"
            elif speed < 0.3:
                text = "Very fast"
            elif speed < 0.6:
                text = "Fast"
            elif speed < 0.8:
                text = "Normal"
            else:
                text = "Slow"
            self.anim_label.config(text=text)
        
        update_anim_label(self.animation_var.get())
        anim_scale.config(command=update_anim_label)
        
        self.sound_var = tk.BooleanVar(value=self.temp_settings.display_prefs.sound_enabled)
        ttk.Checkbutton(effects_frame, text="Enable sound effects",
                       variable=self.sound_var).pack(anchor="w", pady=10)
        
    def _create_counting_tab(self):
        """Create the counting system tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Counting")
        
        # Counting System
        system_frame = ttk.LabelFrame(frame, text="Counting System", padding=10)
        system_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(system_frame, text="Card counting system:").pack(anchor="w")
        self.count_system_var = tk.StringVar(value=self.temp_settings.counting_system.system)
        ttk.Radiobutton(system_frame, text="Hi-Lo", variable=self.count_system_var,
                       value="hi-lo").pack(anchor="w", padx=20)
        ttk.Label(system_frame, text="(More systems coming soon)", 
                 font=("Arial", 9, "italic")).pack(anchor="w", padx=40)
        
        # Display Options
        display_frame = ttk.LabelFrame(frame, text="Display Options", padding=10)
        display_frame.pack(fill="x", padx=10, pady=10)
        
        self.show_deck_est_var = tk.BooleanVar(value=self.temp_settings.counting_system.show_deck_estimation)
        ttk.Checkbutton(display_frame, text="Show deck estimation",
                       variable=self.show_deck_est_var).pack(anchor="w")
        
        precision_frame = tk.Frame(display_frame)
        precision_frame.pack(anchor="w", pady=10)
        ttk.Label(precision_frame, text="True count decimal places:").pack(side="left")
        self.tc_precision_var = tk.IntVar(value=self.temp_settings.counting_system.true_count_precision)
        precision_spin = ttk.Spinbox(precision_frame, from_=0, to=2, 
                                    textvariable=self.tc_precision_var, width=5)
        precision_spin.pack(side="left", padx=5)
        
    def _toggle_surrender_options(self):
        """Enable/disable surrender sub-options"""
        if self.surrender_allowed_var.get():
            self.late_surrender_check.config(state="normal")
        else:
            self.late_surrender_check.config(state="disabled")
            
    def _toggle_auto_deal(self):
        """Enable/disable auto-deal delay setting"""
        if self.auto_deal_var.get():
            self.delay_spin.config(state="normal")
        else:
            self.delay_spin.config(state="disabled")
    
    def _save_settings(self):
        """Save settings and close dialog"""
        # Update temp settings from UI
        self._update_temp_settings()
        
        # Validate settings
        errors = self.temp_settings.validate()
        if errors:
            messagebox.showerror("Invalid Settings", "\n".join(errors))
            return
        
        # Copy temp settings to main settings
        self.settings.from_dict(self.temp_settings.to_dict())
        
        # Save to file
        if self.settings.save():
            self.settings_changed = True
            if self.on_save_callback:
                self.on_save_callback()
            self.dialog.destroy()
            self.dialog = None
        else:
            messagebox.showerror("Save Error", "Failed to save settings to file")
    
    def _update_temp_settings(self):
        """Update temp settings from UI values"""
        # Game Rules
        self.temp_settings.game_rules.dealer_stand_soft_17 = self.stand_soft_17_var.get()
        payout_str = self.blackjack_payout_var.get()
        self.temp_settings.game_rules.blackjack_payout = float(payout_str.split(':')[0])
        self.temp_settings.game_rules.surrender_allowed = self.surrender_allowed_var.get()
        self.temp_settings.game_rules.late_surrender_only = self.late_surrender_var.get()
        self.temp_settings.game_rules.double_after_split = self.double_after_split_var.get()
        self.temp_settings.game_rules.resplit_aces = self.resplit_aces_var.get()
        self.temp_settings.game_rules.max_splits = self.max_splits_var.get()
        self.temp_settings.game_rules.double_on_any_two = self.double_any_two_var.get()
        self.temp_settings.game_rules.insurance_allowed = self.insurance_allowed_var.get()
        
        # Betting Limits
        self.temp_settings.betting_limits.min_bet = self.min_bet_var.get()
        self.temp_settings.betting_limits.max_bet = self.max_bet_var.get()
        self.temp_settings.betting_limits.default_bet = self.default_bet_var.get()
        self.temp_settings.betting_limits.bet_increment = self.bet_increment_var.get()
        self.temp_settings.betting_limits.default_bankroll = self.default_bankroll_var.get()
        
        # Shoe Configuration
        self.temp_settings.shoe_config.num_decks = self.num_decks_var.get()
        self.temp_settings.shoe_config.penetration = self.penetration_var.get()
        self.temp_settings.shoe_config.burn_card = self.burn_card_var.get()
        
        # Practice Modes
        self.temp_settings.practice_modes.auto_deal = self.auto_deal_var.get()
        self.temp_settings.practice_modes.auto_deal_delay = self.auto_delay_var.get()
        self.temp_settings.practice_modes.show_hints_default = self.show_hints_var.get()
        self.temp_settings.practice_modes.show_count_default = self.show_count_var.get()
        self.temp_settings.practice_modes.show_running_count = self.show_running_var.get()
        self.temp_settings.practice_modes.show_true_count = self.show_true_var.get()
        self.temp_settings.practice_modes.show_ev = self.show_ev_var.get()
        self.temp_settings.practice_modes.show_strategy_feedback = self.show_feedback_var.get()
        self.temp_settings.practice_modes.warn_on_mistakes = self.warn_mistakes_var.get()
        
        # Display Preferences
        self.temp_settings.display_prefs.card_style = self.card_style_var.get()
        self.temp_settings.display_prefs.show_probabilities = self.show_probs_var.get()
        self.temp_settings.display_prefs.show_dealer_hole_card = self.show_hole_var.get()
        self.temp_settings.display_prefs.animation_speed = self.animation_var.get()
        self.temp_settings.display_prefs.sound_enabled = self.sound_var.get()
        
        # Counting System
        self.temp_settings.counting_system.system = self.count_system_var.get()
        self.temp_settings.counting_system.show_deck_estimation = self.show_deck_est_var.get()
        self.temp_settings.counting_system.true_count_precision = self.tc_precision_var.get()
    
    def _cancel(self):
        """Cancel without saving"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
    
    def _reset_defaults(self):
        """Reset all settings to defaults"""
        response = messagebox.askyesno(
            "Reset Settings",
            "Are you sure you want to reset all settings to their default values?"
        )
        if response:
            self.temp_settings.reset_to_defaults()
            # Refresh the dialog with default values
            self.dialog.destroy()
            self.dialog = None
            self.show()