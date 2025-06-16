"""Game configuration and constants"""

# Window settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1050
WINDOW_TITLE = "Blackjack Card Counter Trainer"

# Table settings
TABLE_COLOR = '#0a5c2e'  # Dark green
TABLE_OUTLINE_COLOR = '#d4af37'  # Gold
TABLE_FELT_COLOR = '#1a7c3e'  # Lighter green

# Card settings
CARD_WIDTH = 100
CARD_HEIGHT = 140
CARD_SPACING = 20

# Game settings
DECKS_IN_SHOE = 6
TOTAL_CARDS_IN_SHOE = 52 * DECKS_IN_SHOE  # 312
DEFAULT_PENETRATION = 0.67  # Deal ~4 decks before shuffle
DEALER_STAND_ON = 17
BLACKJACK_PAYOUT = 1.5

# Betting settings
MIN_BET = 5
MAX_BET = 500
DEFAULT_BET = 25
DEFAULT_BANKROLL = 1000

# Card counting settings
HI_LO_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# EV calculation settings
BASE_HOUSE_EDGE = -0.005  # -0.5%
TRUE_COUNT_ADVANTAGE = 0.005  # 0.5% per true count

# UI positions
DEALER_CARD_Y = 80
PLAYER_CARD_Y = 250
DECK_POSITION = (1050, 240)

# Colors
BUTTON_BG = '#2c3e50'
BUTTON_FG = '#ffffff'
BUTTON_ACTIVE_BG = '#34495e'
TEXT_COLOR = '#ffffff'
ERROR_COLOR = '#e74c3c'
SUCCESS_COLOR = '#27ae60'

# Font settings
MAIN_FONT = ('Arial', 12)
BUTTON_FONT = ('Arial', 14, 'bold')
SCORE_FONT = ('Arial', 18, 'bold')
COUNT_FONT = ('Arial', 16)

# Animation settings (for future use)
DEAL_ANIMATION_SPEED = 0.02  # seconds per frame
ANIMATION_STEPS = 20

# File paths
CARDS_DIR = 'cards'
SETTINGS_FILE = 'settings.json'