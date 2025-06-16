# Blackjack Card Counting Trainer - Product Requirements Document

## 1. Project Overview

### 1.1 Purpose
Develop a standalone Windows 11 desktop application for blackjack card counting training that simulates real casino conditions with accurate EV calculations based on both basic strategy adherence and card counting advantage.

### 1.2 Technology Stack Decision
**Selected Technology: Python + Tkinter**

#### Why Tkinter:
- Tkinter comes installed with your Python version. Perhaps the easiest to start with
- Python's syntax is clean and concise, allowing developers to write code quickly and focus on the logic of their applications
- Compared to other GUI libraries, building executables for TkInter applications are simpler because TkInter is included in Python
- Extensive examples of card games already exist in Tkinter
- Perfect balance of simplicity and functionality for this project

### 1.3 Core Value Proposition
- Practice card counting in realistic conditions
- Real-time EV tracking incorporating counting edge
- Performance feedback on basic strategy decisions
- Full hand simulation with proper shoe management

## 2. Technical Architecture with Tkinter

### 2.1 Tkinter Architecture Overview
Tk and most other GUI toolkits do that by simply checking for any new events over and over again, many times every second. This is called an event loop or main loop

The application will use:
- **Main Window**: Root Tk() object
- **Canvas Widget**: For the blackjack table and card display
- **Frame Widgets**: For organizing UI sections
- **Label Widgets**: For displaying scores, counts, and information
- **Button Widgets**: For player actions
- **PIL/Pillow**: For card image handling

### 2.2 Core Components

#### Event Loop Management
The event loop continually processes events, pulled from the system event queue, usually dozens of times a second. It watches for mouse or keyboard events, invoking command callbacks and event bindings as needed

```python
# Main application structure
class BlackjackGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blackjack Card Counter Trainer")
        self.root.geometry("1200x800")
        self.setup_ui()
        
    def run(self):
        self.root.mainloop()
```

#### Image Handling with PIL
To resize an image using the PIL package, we have to follow these steps: Install Pillow Package or PIL in the local machine. Open the Image using Open(image_location) method. Resize the given image using resize((w,h), Image.ANTIALIAS)

```python
from PIL import Image, ImageTk

def load_card_image(card_name):
    image = Image.open(f"cards/{card_name}.png")
    resized = image.resize((100, 140), Image.LANCZOS)
    return ImageTk.PhotoImage(resized)
```

### 2.3 File Structure
```
blackjack_trainer/
├── main.py              # Entry point
├── game_engine.py       # Core game logic
├── ui_components.py     # Tkinter UI elements
├── card_counting.py     # Counting logic
├── ev_calculator.py     # EV calculation engine
├── config.py           # Game settings
├── cards/              # Card PNG images
│   ├── 2_hearts.png
│   ├── 3_hearts.png
│   └── ...
└── requirements.txt    # Dependencies (PIL, etc.)
```

## 3. Detailed Feature Implementation

### 3.1 Canvas-Based Table Display
We'll keep track of who has what cards, and when the deck is empty, the game will end. This is a good foundation for creating just about any card game with Tkinter

```python
class BlackjackTable:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, width=1200, height=600, bg='#0a5c2e')
        self.canvas.pack()
        self.draw_table()
        
    def draw_table(self):
        # Draw semicircle table
        self.canvas.create_arc(200, 100, 1000, 700, 
                              start=0, extent=180, 
                              fill='#1a7c3e', outline='#d4af37', width=3)
```

### 3.2 Card Management System
```python
class Shoe:
    def __init__(self):
        self.cards = self.create_shoe()
        self.dealt_cards = 0
        self.penetration_point = 208  # ~4 decks
        
    def create_shoe(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        deck = [(rank, suit) for _ in range(6) 
                for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck
```

### 3.3 Event-Driven UI Updates
Tkinter allows you to schedule events to occur after a certain amount of time using the after method. This is useful for tasks that need to be executed periodically

```python
def update_display(self):
    # Update card display
    self.canvas.delete("cards")
    self.display_cards()
    
    # Schedule next update if animating
    if self.animating:
        self.root.after(50, self.update_display)
```

### 3.4 Hi-Lo Counting Implementation
```python
class CardCounter:
    def __init__(self):
        self.running_count = 0
        self.true_count = 0
        self.cards_remaining = 312
        
    def update_count(self, card_rank):
        if card_rank in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif card_rank in ['10', 'J', 'Q', 'K', 'A']:
            self.running_count -= 1
        # 7, 8, 9 are neutral (0)
        
        self.calculate_true_count()
```

### 3.5 EV Calculation Engine
```python
class EVCalculator:
    def __init__(self):
        self.base_house_edge = -0.005  # -0.5%
        
    def calculate_ev(self, true_count, bet_size):
        # Each true count adds ~0.5% to player edge
        count_advantage = true_count * 0.005
        total_edge = self.base_house_edge + count_advantage
        return bet_size * total_edge
```

## 4. User Interface Specification

### 4.1 Layout Structure
```
┌─────────────────────────────────────────────────┐
│  Blackjack Card Counter Trainer      [−][□][×]  │
├─────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────┐  │
│  │          Dealer: 17                       │  │
│  │         [🂡] [🂱]                         │  │
│  │                                           │  │
│  │         BLACKJACK TABLE                   │  │
│  │                                           │  │
│  │         [🂡] [🂱] [🂡]                    │  │
│  │          Player: 21                       │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  [HIT] [STAND] [DOUBLE] [SPLIT]    Bet: $25 [−][+] │
│                                                  │
│  Running Count: +3  │  True Count: +1.5  [👁]   │
│  Session EV: +2.3%  │  Bankroll: $1,025        │
│                                                  │
│  [NEW SHOE] [RESET COUNT] [SETTINGS]           │
└─────────────────────────────────────────────────┘
```

### 4.2 Interactive Elements

#### Buttons
```python
# Action buttons with event handlers
self.hit_button = tk.Button(control_frame, text="HIT", 
                           command=self.hit, width=10, height=2)
self.hit_button.bind('<Return>', lambda e: self.hit())
```

#### Count Display Toggle
```python
def toggle_count_display(self):
    if self.count_visible:
        self.count_label.config(text="Count: ---")
    else:
        self.count_label.config(
            text=f"RC: {self.running_count} TC: {self.true_count:.1f}")
    self.count_visible = not self.count_visible
```

### 4.3 Card Animation
Resize The Image our_card_resize_image = our_card_img.resize((150, 218))

```python
def deal_card_animated(self, target_pos):
    # Start position (deck)
    start_x, start_y = 1100, 300
    end_x, end_y = target_pos
    
    # Create card at deck position
    card_id = self.canvas.create_image(start_x, start_y, 
                                      image=self.card_back, anchor='nw')
    
    # Animate to target
    steps = 20
    for i in range(steps):
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        self.canvas.move(card_id, dx, dy)
        self.canvas.update()
        time.sleep(0.02)
```

## 5. Data Models

### 5.1 Card Model
```python
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self.get_value()
        self.count_value = self.get_count_value()
        
    def get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Soft ace
        else:
            return int(self.rank)
```

### 5.2 Hand Model
```python
class Hand:
    def __init__(self):
        self.cards = []
        self.soft = False
        
    def add_card(self, card):
        self.cards.append(card)
        self.calculate_value()
        
    def calculate_value(self):
        value = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
            
        self.value = value
        self.soft = aces > 0 and value <= 21
```

## 6. Development Guidelines

### 6.1 Tkinter Best Practices
- Button callbacks are also ran in the main loop. So if our button callback takes 5 seconds to run, the main loop can't process other events
- Keep event handlers lightweight
- Use `after()` for periodic updates instead of loops
- All drawing occurs only in the event loop

### 6.2 Performance Optimization
- Pre-load all card images at startup
- Use Canvas tags for efficient updates
- Minimize canvas redraws
- Cache PhotoImage objects

### 6.3 Code Organization
```python
# Separate concerns
class GameEngine:
    """Pure game logic, no UI"""
    pass

class GameUI:
    """UI components and event handling"""
    pass

class CardCountingEngine:
    """Counting logic separated from display"""
    pass
```

## 7. Testing Strategy

### 7.1 Unit Tests
- Card counting accuracy
- EV calculations
- Basic strategy engine
- Shoe penetration

### 7.2 Integration Tests
- Full hand simulation
- Count tracking across hands
- Bankroll management
- UI responsiveness

### 7.3 User Acceptance Tests
- Play 1000 hands, verify EV convergence
- Test all player actions
- Verify count accuracy
- Performance under rapid play

## 8. Deployment

### 8.1 Packaging
```python
# setup.py for py2exe or PyInstaller
setup(
    name="Blackjack Trainer",
    version="1.0",
    windows=[{"script": "main.py"}],
    options={
        "py2exe": {
            "includes": ["tkinter", "PIL"],
            "bundle_files": 1,
            "compressed": True
        }
    }
)
```

### 8.2 Distribution
- Single executable file
- Include card images as resources
- No installation required
- Settings saved locally in JSON

## 9. Future Enhancements
- Additional counting systems (KO, Omega II)
- Tournament mode
- Statistics export
- Custom rule variations
- Speed training mode
- Betting strategy trainer

## 10. Success Metrics
- Loads in < 2 seconds
- Smooth card animations (60 FPS)
- Accurate count tracking (100%)
- EV calculation within 0.01% of theoretical
- Memory usage < 100MB
- Works offline on Windows 11