# Final Pre-Production Test Plan for 12-Hour Blackjack Session

This document contains a comprehensive, chronologically ordered test plan to verify all critical functionality before a 12-hour play session. Execute these tests in order to ensure system stability and accuracy.

## Pre-Test Setup
- [ ] Verify Python 3.12+ is installed
- [ ] Run `python3 main.py` to ensure no syntax errors
- [ ] Clear any existing settings.json to test defaults
- [ ] Set up a notepad to track any issues found

## Section 1: Initial Launch and Basic Functionality (15 minutes)

### 1.1 Application Launch
- [ ] Launch application - should start without errors
- [ ] Verify window size is 1200x800
- [ ] Check all UI elements are visible and properly aligned
- [ ] Verify green table background renders correctly
- [ ] Confirm no console errors on startup

### 1.2 Initial State Verification  
- [ ] Starting bankroll shows $1000 (default)
- [ ] Bet size shows $10 (default)
- [ ] Count displays show 0 (running and true)
- [ ] EV shows 0.00
- [ ] All action buttons are disabled initially
- [ ] NEW SHOE button is enabled

### 1.3 First Hand Test
- [ ] Click NEW SHOE - verify 6 decks (312 cards) loaded
- [ ] Press SPACE - cards should deal
- [ ] Verify dealer shows one up card, one down
- [ ] Verify player gets two cards
- [ ] Check hand values display correctly
- [ ] Verify appropriate buttons enable (HIT/STAND always, DOUBLE if appropriate)

## Section 2: Core Game Mechanics (30 minutes)

### 2.1 Basic Actions Test
- [ ] **HIT Test**: Hit until 21 or bust - verify:
  - Cards add correctly to hand
  - Value updates properly (including soft aces)
  - Buttons disable on 21 or bust
  - Round completes automatically on bust
  
- [ ] **STAND Test**: Stand on various totals - verify:
  - Dealer reveals hole card
  - Dealer draws according to rules (hit soft 16, stand on 17)
  - Correct winner determination
  - Bankroll updates correctly

- [ ] **DOUBLE Test**: Double on 10 or 11 - verify:
  - Bet doubles (bankroll decreases by original bet)
  - Exactly one card dealt
  - Auto-stands after card
  - Correct payout on win (2x doubled bet)

### 2.2 Blackjack Scenarios
- [ ] **Player Blackjack**: Get A-K or A-Q - verify:
  - Immediate "Blackjack!" message
  - 1.5x payout ($10 bet = $15 win = $25 return)
  - Dealer doesn't draw if player has blackjack
  
- [ ] **Dealer Blackjack**: Dealer shows ace - verify:
  - Insurance offered (if implemented)
  - Dealer blackjack beats player 21
  - Push on player + dealer blackjack
  
- [ ] **Both Blackjack**: Verify push (no money change)

### 2.3 Edge Cases
- [ ] **Soft Hands**: Test A-6 (soft 17) - verify:
  - Shows as 7/17
  - Hit converts to hard hand if busts as soft
  - Strategy hint shows correct play
  
- [ ] **Multiple Aces**: A-A-9 = 21, not 31
- [ ] **Five Card Charlie**: No special rule (normal hand)

## Section 3: Split Functionality (45 minutes)

### 3.1 Basic Split Test
- [ ] Get pair (e.g., 8-8) - verify:
  - SPLIT button enables
  - Split creates two hands with one 8 each
  - Bet doubles (two equal bets)
  - First hand becomes active (highlighted)
  - Message shows "Playing hand 1 of 2"

### 3.2 Multi-Split Test  
- [ ] Split to maximum (3 splits = 4 hands) - verify:
  - Each split hand gets highlighted when active
  - Hands play left to right
  - After standing/busting, auto-advances to next
  - All hands show individual outcomes
  - Bankroll updates sum of all hand results

### 3.3 Split Aces Rules
- [ ] Split aces - verify:
  - Each ace gets exactly ONE card
  - No hit/double options
  - A-10 after split = 21, NOT blackjack
  - Auto-advances after one card

### 3.4 Split Edge Cases
- [ ] **Insufficient Funds**: With $15 bankroll, $10 bet - verify:
  - Can't split (button disabled)
  - Can still hit/stand normally
  
- [ ] **Max Splits**: After 3 splits - verify:
  - Can't split 4th pair
  - SPLIT button disabled
  
- [ ] **Re-split Aces**: Get A-A, split, get another A - verify:
  - Follows settings (allow/disallow resplit aces)

## Section 4: Card Counting Accuracy (30 minutes)

### 4.1 Hi-Lo Count Verification
- [ ] Track 20 cards manually while playing - verify:
  - 2-6: +1 each
  - 7-9: 0 each  
  - 10-J-Q-K-A: -1 each
  - Running count matches your manual count

### 4.2 True Count Calculation
- [ ] At ~1 deck used (52 cards) - verify:
  - True count = Running count / 5 (decks remaining)
  - Example: RC=+5 with 5 decks left = TC +1.0
  
- [ ] At ~4 decks used (208 cards) - verify:
  - True count = Running count / 2
  - Updates in real-time as cards dealt

### 4.3 Count Reset Test
- [ ] Play to penetration point (~4 decks) - verify:
  - "Shuffle needed" message appears
  - Count resets to 0 on new shoe
  - Previous count doesn't carry over

### 4.4 Count Display Toggle
- [ ] Toggle count visibility - verify:
  - Can hide/show count during play
  - Count still tracks when hidden
  - Reveals correct count when shown

## Section 5: EV and Mathematics (30 minutes)

### 5.1 EV Formula Verification
- [ ] With TC = 0: EV should show -0.50% (house edge)
- [ ] With TC = +1: EV should show 0.00% (break even)
- [ ] With TC = +2: EV should show +0.50%
- [ ] With TC = +3: EV should show +1.00%
- [ ] With TC = -2: EV should show -1.50%

### 5.2 Session EV Tracking
- [ ] Play 50 hands tracking results - verify:
  - Actual P/L tracks correctly
  - Expected EV = sum of (bet × hand_EV%)
  - Variance is reasonable (actual within 3 SD of expected)

### 5.3 Bankroll Calculations
- [ ] Win hand: Bankroll increases by bet amount
- [ ] Lose hand: Bankroll decreases by bet amount
- [ ] Push: No bankroll change
- [ ] Blackjack: Bankroll increases by 1.5x bet
- [ ] Double win: Bankroll increases by 2x bet
- [ ] Double loss: Bankroll decreases by 2x bet

## Section 6: Basic Strategy Validation (45 minutes)

### 6.1 Strategy Table Spot Checks
Test these specific scenarios match basic strategy:

**Hard Hands:**
- [ ] 16 vs 10: HIT (not STAND)
- [ ] 11 vs any: DOUBLE
- [ ] 12 vs 2-3: HIT
- [ ] 12 vs 4-6: STAND
- [ ] 17-21 vs any: STAND

**Soft Hands:**
- [ ] A,7 vs 2-8: STAND  
- [ ] A,7 vs 9-A: HIT
- [ ] A,6 vs 3-6: DOUBLE
- [ ] A,2-A,5 vs 4-6: DOUBLE

**Pairs:**
- [ ] A,A: Always SPLIT
- [ ] 8,8: Always SPLIT
- [ ] 10,10: Never SPLIT
- [ ] 5,5: Never SPLIT (treat as 10)
- [ ] 9,9 vs 7,10,A: STAND
- [ ] 9,9 vs 2-6,8,9: SPLIT

### 6.2 Strategy Hints Test
- [ ] Enable hints - verify correct advice shown
- [ ] Make wrong play - verify deviation tracked
- [ ] Check adherence % updates correctly
- [ ] Disable hints - verify no advice shown

### 6.3 Split Strategy Verification
- [ ] 4,4 vs 5-6: SPLIT if DAS, HIT if no DAS
- [ ] 2,2 and 3,3 vs 2-7: SPLIT if DAS
- [ ] 6,6 vs 2-6: SPLIT
- [ ] Verify strategy considers current rules

## Section 7: Settings and Configuration (30 minutes)

### 7.1 Settings Dialog Test
- [ ] Open settings - verify all tabs present
- [ ] Change each setting - verify it saves
- [ ] Close and reopen - verify persistence
- [ ] Reset to defaults - verify all reset

### 7.2 Rule Variations Test
- [ ] **Dealer Hits Soft 17**: Verify dealer behavior changes
- [ ] **Double After Split**: Verify DOUBLE enables on split hands
- [ ] **Resplit Aces**: Verify can/can't resplit based on setting
- [ ] **Max Splits**: Change from 3 to 1 - verify enforcement
- [ ] **Blackjack Payout**: Change to 6:5 - verify payout

### 7.3 Betting Limits Test
- [ ] Set min bet $5, max $100 - verify:
  - Can't bet below $5
  - Can't bet above $100
  - Bet increment respects limits
  
- [ ] Set default bet $25 - verify starts at $25

### 7.4 Display Settings
- [ ] Toggle count visibility default
- [ ] Change card back color
- [ ] Adjust auto-deal delay
- [ ] Test each display preference

## Section 8: Auto-Play and Practice Modes (30 minutes)

### 8.1 Auto-Play Test
- [ ] Enable auto-play - verify:
  - Plays perfect basic strategy
  - Respects bet settings
  - Handles splits correctly
  - Stops at bankroll limit
  
- [ ] Test each difficulty level:
  - [ ] Beginner: All info visible
  - [ ] Intermediate: Dealer total hidden
  - [ ] Advanced: Count hidden
  - [ ] Expert: Minimal info

### 8.2 Speed Test
- [ ] Set auto-deal to fastest - verify:
  - No crashes or freezes
  - UI remains responsive
  - Count stays accurate
  - Can still manual override

### 8.3 Betting Strategy Test
- [ ] **Flat Betting**: Constant bet size
- [ ] **Spread Betting**: Verify 1-8x spread based on count
- [ ] **Kelly Criterion**: Verify bet sizing formula
- [ ] Check bet suggestions display correctly

## Section 9: Performance and Stability (60 minutes)

### 9.1 Rapid Play Test
- [ ] Play 500 hands as fast as possible - verify:
  - No slowdown or lag
  - Memory usage stable
  - Count remains accurate
  - No UI glitches

### 9.2 Extended Session Test  
- [ ] Play for 1 hour continuously - monitor:
  - CPU usage remains reasonable
  - Memory doesn't grow unbounded
  - No crashes or freezes
  - Statistics remain accurate

### 9.3 Stress Test Scenarios
- [ ] Spam-click buttons rapidly
- [ ] Resize window during play
- [ ] Alt-tab away and back
- [ ] Play with very high bet sizes
- [ ] Create many split hands rapidly

### 9.4 Edge Case Bombardment
- [ ] Dealer gets 7+ cards to make hand
- [ ] Player gets 10+ cards without busting
- [ ] Split to max hands 10 times in a row
- [ ] Alternate between $1 and $1000 bets
- [ ] Double on every possible hand

## Section 10: Error Recovery (30 minutes)

### 10.1 Interruption Testing
- [ ] Close app mid-hand - verify:
  - Reopens without error
  - Settings preserved
  - Can start fresh game
  
- [ ] Force-quit during shuffle - verify recovery

### 10.2 Invalid State Testing
- [ ] Edit settings.json to invalid values - verify:
  - App handles gracefully
  - Falls back to defaults
  - Shows appropriate warnings

### 10.3 Resource Testing
- [ ] Run without card images - verify text cards work
- [ ] Delete settings file - verify recreates
- [ ] Corrupt JSON - verify error handling

## Section 11: Final Integration Test (45 minutes)

### 11.1 Complete Game Scenario
Play a full "mini-session" using all features:
- [ ] Start with $100 bankroll
- [ ] Use spread betting (1-8 units)
- [ ] Play 100 hands including:
  - At least 5 splits
  - At least 10 doubles
  - Experience one shuffle
  - Track count throughout
  
- [ ] Verify final statistics:
  - Hand count accurate
  - Win/loss/push percentages sum to 100%
  - Actual vs Expected EV reasonable
  - Strategy adherence tracked correctly

### 11.2 Specific Scenario Tests
Run through these exact scenarios:

- [ ] **The Nightmare**: 16 vs 10, hit and bust 5 times - verify tilt protection
- [ ] **The Dream**: Get 3 blackjacks in a row - verify correct payouts
- [ ] **The Grind**: Play 50 hands without splitting - verify no issues
- [ ] **The Variance**: Lose 10 hands in a row - verify bankroll management

### 11.3 Final Checklist
- [ ] All keyboard shortcuts work (H, S, D, P, Space, Esc)
- [ ] No memory leaks after 1000+ hands  
- [ ] Count accuracy verified against manual count
- [ ] EV calculations match formula
- [ ] Strategy hints are correct
- [ ] Split hands resolve properly
- [ ] Settings save and load correctly
- [ ] Auto-play executes perfect strategy
- [ ] UI remains responsive
- [ ] No crashes or freezes

## Section 12: 12-Hour Readiness Verification

### 12.1 Endurance Metrics
After all tests, verify:
- [ ] 500+ hands/hour capability confirmed
- [ ] Memory usage stable over time
- [ ] No performance degradation
- [ ] Count accuracy maintained
- [ ] All calculations verified correct

### 12.2 Critical Features Confirmed
- [ ] Split functionality works flawlessly
- [ ] EV tracking is accurate
- [ ] Basic strategy is correct
- [ ] Bankroll management is bulletproof
- [ ] No crash scenarios found

### 12.3 Backup Plan
- [ ] Settings.json backed up
- [ ] Know how to reset if needed
- [ ] Verified recovery procedures
- [ ] Have manual count backup method

## Post-Test Actions
1. Fix any bugs found during testing
2. Re-run failed sections after fixes
3. Create backup of working settings
4. Clear history for fresh session start
5. Set preferred configuration for 12-hour session

## Success Criteria
- Zero crashes during test period
- All mathematical calculations verified accurate
- Split functionality works in all scenarios  
- Performance maintains 500+ hands/hour
- No memory leaks or degradation
- All UI elements remain responsive
- Count accuracy verified to 100%
- Basic strategy confirmed correct

**Total Testing Time: ~6 hours**

Once all items are checked, the application is verified ready for a 12-hour continuous play session.