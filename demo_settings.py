#!/usr/bin/env python3
"""Demo script to showcase the settings system functionality"""

from settings import settings
from game_engine import GameState, Hand, Card

def demo_settings_overview():
    """Show current settings overview"""
    print("=== CURRENT SETTINGS OVERVIEW ===")
    print(f"Game Rules:")
    print(f"  - Dealer stands on soft 17: {settings.game_rules.dealer_stand_soft_17}")
    print(f"  - Blackjack payout: {settings.game_rules.blackjack_payout}:1")
    print(f"  - Double on any two cards: {settings.game_rules.double_on_any_two}")
    print(f"  - Max splits allowed: {settings.game_rules.max_splits}")
    
    print(f"\nBetting Limits:")
    print(f"  - Min bet: ${settings.betting_limits.min_bet}")
    print(f"  - Max bet: ${settings.betting_limits.max_bet}")
    print(f"  - Default bet: ${settings.betting_limits.default_bet}")
    print(f"  - Bet increment: ${settings.betting_limits.bet_increment}")
    
    print(f"\nShoe Configuration:")
    print(f"  - Number of decks: {settings.shoe_config.num_decks}")
    print(f"  - Penetration: {settings.shoe_config.penetration:.1%}")
    print(f"  - Burn card: {settings.shoe_config.burn_card}")
    
    print(f"\nPractice Modes:")
    print(f"  - Auto-deal: {settings.practice_modes.auto_deal}")
    print(f"  - Auto-deal delay: {settings.practice_modes.auto_deal_delay}s")
    print(f"  - Show hints by default: {settings.practice_modes.show_hints_default}")
    print(f"  - Show count by default: {settings.practice_modes.show_count_default}")

def demo_game_rule_changes():
    """Demonstrate how game rule changes affect gameplay"""
    print("\n=== GAME RULE CHANGES DEMO ===")
    
    # Create a soft 17 hand
    hand = Hand(is_dealer=True)
    hand.add_card(Card('A', 'hearts'))
    hand.add_card(Card('6', 'spades'))
    
    print(f"Dealer has: {[str(c) for c in hand.cards]} (value: {hand.value}, soft: {hand.is_soft})")
    
    # Test with dealer stands on soft 17
    settings.game_rules.dealer_stand_soft_17 = True
    must_hit = settings.dealer_must_hit(hand.value, hand.is_soft)
    print(f"With 'dealer stands on soft 17': Dealer must hit = {must_hit}")
    
    # Test with dealer hits on soft 17
    settings.game_rules.dealer_stand_soft_17 = False
    must_hit = settings.dealer_must_hit(hand.value, hand.is_soft)
    print(f"With 'dealer hits on soft 17': Dealer must hit = {must_hit}")
    
    # Reset to default
    settings.game_rules.dealer_stand_soft_17 = True

def demo_betting_limits():
    """Show how betting limits work"""
    print("\n=== BETTING LIMITS DEMO ===")
    
    # Create game state
    gs = GameState()
    print(f"Initial bankroll: ${gs.bankroll}")
    print(f"Initial bet: ${gs.current_bet}")
    
    # Show betting range
    print(f"Betting range: ${settings.betting_limits.min_bet} - ${settings.betting_limits.max_bet}")
    print(f"Bet increment: ${settings.betting_limits.bet_increment}")
    
    # Simulate bet changes
    print("\nSimulating bet changes:")
    bet = settings.betting_limits.default_bet
    print(f"  Start: ${bet}")
    
    # Increase bet
    bet += settings.betting_limits.bet_increment
    print(f"  After increase: ${bet}")
    
    # Decrease bet
    bet -= settings.betting_limits.bet_increment
    print(f"  After decrease: ${bet}")
    
    # Try to go below minimum
    bet = settings.betting_limits.min_bet - settings.betting_limits.bet_increment
    if bet < settings.betting_limits.min_bet:
        bet = settings.betting_limits.min_bet
    print(f"  Minimum enforced: ${bet}")

def demo_shoe_configuration():
    """Show how shoe configuration affects the game"""
    print("\n=== SHOE CONFIGURATION DEMO ===")
    
    original_decks = settings.shoe_config.num_decks
    original_penetration = settings.shoe_config.penetration
    
    # Test different deck counts
    for decks in [1, 2, 6, 8]:
        settings.shoe_config.num_decks = decks
        gs = GameState()
        total_cards = gs.shoe.num_decks * 52
        penetration_cards = int(total_cards * settings.shoe_config.penetration)
        remaining_at_shuffle = total_cards - penetration_cards
        
        print(f"  {decks} deck{'s' if decks > 1 else ''}: {total_cards} cards, shuffle at {penetration_cards} cards dealt ({remaining_at_shuffle} remain)")
    
    # Test different penetration levels
    settings.shoe_config.num_decks = 6
    print(f"\nWith 6 decks ({6 * 52} cards):")
    for pen in [0.5, 0.67, 0.75, 0.9]:
        settings.shoe_config.penetration = pen
        cards_dealt = int(6 * 52 * pen)
        cards_remaining = 6 * 52 - cards_dealt
        print(f"  {pen:.0%} penetration: shuffle after {cards_dealt} cards ({cards_remaining} remain)")
    
    # Reset
    settings.shoe_config.num_decks = original_decks
    settings.shoe_config.penetration = original_penetration

def demo_settings_persistence():
    """Demonstrate settings save/load functionality"""
    print("\n=== SETTINGS PERSISTENCE DEMO ===")
    
    # Save current settings
    original_decks = settings.shoe_config.num_decks
    original_bet = settings.betting_limits.default_bet
    
    print(f"Original settings: {original_decks} decks, ${original_bet} default bet")
    
    # Change settings
    settings.shoe_config.num_decks = 8
    settings.betting_limits.default_bet = 50
    print(f"Changed settings: {settings.shoe_config.num_decks} decks, ${settings.betting_limits.default_bet} default bet")
    
    # Save to file
    if settings.save():
        print("Settings saved to file successfully")
    
    # Change settings again
    settings.shoe_config.num_decks = 1
    settings.betting_limits.default_bet = 10
    print(f"Modified in memory: {settings.shoe_config.num_decks} decks, ${settings.betting_limits.default_bet} default bet")
    
    # Load from file
    if settings.load():
        print("Settings loaded from file successfully")
        print(f"Loaded settings: {settings.shoe_config.num_decks} decks, ${settings.betting_limits.default_bet} default bet")
    
    # Restore original settings
    settings.shoe_config.num_decks = original_decks
    settings.betting_limits.default_bet = original_bet
    settings.save()
    print("Original settings restored")

def demo_validation():
    """Show settings validation in action"""
    print("\n=== SETTINGS VALIDATION DEMO ===")
    
    # Create settings with invalid values
    test_settings = settings.__class__()
    test_settings.betting_limits.min_bet = 0  # Invalid
    test_settings.betting_limits.max_bet = -100  # Invalid
    test_settings.shoe_config.num_decks = 15  # Invalid
    test_settings.shoe_config.penetration = 1.5  # Invalid
    test_settings.game_rules.blackjack_payout = 0.5  # Invalid
    
    errors = test_settings.validate()
    print(f"Found {len(errors)} validation errors:")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")
    
    print("\nValidation prevents saving invalid settings!")

def main():
    """Run all demos"""
    print("🎰 BLACKJACK SETTINGS SYSTEM DEMO 🎰\n")
    
    demo_settings_overview()
    demo_game_rule_changes()
    demo_betting_limits()
    demo_shoe_configuration()
    demo_settings_persistence()
    demo_validation()
    
    print("\n=== DEMO COMPLETE ===")
    print("✅ The settings system provides comprehensive configuration")
    print("✅ All game rules and preferences are now customizable")
    print("✅ Settings are automatically saved and loaded")
    print("✅ Validation ensures only valid configurations are used")
    print("\nTo access settings in the game, click the 'SETTINGS' button!")

if __name__ == "__main__":
    main()