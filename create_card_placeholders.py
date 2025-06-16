"""Create simple text-based card placeholder images"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_card_image(rank, suit, output_path):
    """Create a simple card image with text"""
    # Card dimensions
    width, height = 100, 140
    
    # Create white card with black border
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, width-1, height-1], outline='black', width=2)
    
    # Suit colors and symbols
    suit_info = {
        'hearts': ('♥', 'red'),
        'diamonds': ('♦', 'red'),
        'clubs': ('♣', 'black'),
        'spades': ('♠', 'black')
    }
    
    symbol, color = suit_info[suit]
    
    # Try to use a font, fall back to default if not available
    try:
        font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw rank in corners
    draw.text((10, 10), rank, fill=color, font=font_small)
    draw.text((width-25, height-35), rank, fill=color, font=font_small)
    
    # Draw suit symbol in center
    bbox = draw.textbbox((0, 0), symbol, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), symbol, fill=color, font=font_large)
    
    # Save image
    img.save(output_path)

def create_card_back(output_path):
    """Create a card back image"""
    width, height = 100, 140
    
    img = Image.new('RGB', (width, height), 'darkred')
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, width-1, height-1], outline='gold', width=2)
    
    # Draw pattern
    for i in range(10, width-10, 20):
        for j in range(10, height-10, 20):
            draw.ellipse([i, j, i+10, j+10], outline='gold', width=1)
    
    img.save(output_path)

def main():
    """Generate all card images"""
    # Create cards directory if it doesn't exist
    if not os.path.exists('cards'):
        os.makedirs('cards')
    
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    print("Creating card images...")
    
    # Create all cards
    for suit in suits:
        for rank in ranks:
            filename = f"{rank}_{suit}.png"
            filepath = os.path.join('cards', filename)
            create_card_image(rank, suit, filepath)
            print(f"  Created {filename}")
    
    # Create card back
    back_path = os.path.join('cards', 'back.png')
    create_card_back(back_path)
    print("  Created back.png")
    
    print(f"\nCreated {len(suits) * len(ranks) + 1} card images in 'cards/' directory")

if __name__ == "__main__":
    main()