import random
import time
import sys

# Symbols and multipliers for 3 matching symbols
symbols = {
    "🍒": 2,
    "🍋": 3,
    "🍉": 4,
    "🍇": 5,
    "💎": 10,
    "🔔": 7,
    "🍀": 8
}

# Game variables
balance = 0
total_lost = 0
bet = 1  # minimum bet
game_history = []

# Hidden / random bonus settings
hidden_bonus_trigger = 1000        # loss threshold at which a bonus may activate
hidden_bonus_percentage = 0.10     # 10% of losses
hidden_bonus_chance = 1            # 100% chance to activate (can be changed)

def print_welcome():
    print("=" * 50)
    print("🎰 WELCOME TO ROTATING CASINO 🎰")
    print("=" * 50)
    print("Rules (important info):")
    print(" - Minimum bet: 1 BGN")
    print(" - 3 matching symbols = big win 🎉")
    print(" - 2 matching symbols from the left = double win ✨")
    print("=" * 50)

def deposit_money():
    global balance
    while True:
        try:
            amount = int(input("Enter starting balance (BGN): "))
            if amount <= 0:
                print("❌ Please enter a positive number.")
                continue
            balance = amount
            print(f"✅ Balance set to {balance} BGN.\n")
            break
        except ValueError:
            print("❌ Invalid number, try again.")

def show_menu():
    print("\n--- MAIN MENU ---")
    print("1. Spin the slot machine 🎰")
    print("2. Change bet (min. 1 BGN) 💵")
    print("3. Show balance 💰")
    print("4. Game history 📝")
    print("5. Exit 🚪")

def apply_hidden_bonus():
    """
    Attempts to apply a hidden bonus.
    Returns (triggered: bool, bonus_amount: int)
    If total_lost >= hidden_bonus_trigger and randomness passes,
    returns True and the bonus amount (10% of total_lost as an integer).
    Then resets total_lost.
    """
    global total_lost, balance

    if total_lost > hidden_bonus_trigger:
        # activation chance (e.g. 100%)
        if random.random() < hidden_bonus_chance:
            bonus = int(total_lost * hidden_bonus_percentage)
            if bonus > 0:
                balance += bonus
                total_lost = 0  # reset accumulated losses after bonus
                return True, bonus
    return False, 0

def spin_slot():
    global balance, total_lost, bet

    if balance < bet:
        print("⚠️ You don't have enough money to spin.")
        return

    # Deduct the bet
    balance -= bet
    total_lost += bet

    # Spin animation
    print("\nSpinning...")
    time.sleep(0.8)

    reels = [random.choice(list(symbols.keys())) for _ in range(3)]
    print(" | ".join(reels))

    win_amount = 0

    # Check for 3 matching symbols (jackpot)
    if reels[0] == reels[1] == reels[2]:
        multiplier = symbols[reels[0]]
        win_amount = bet * multiplier
        print(f"🎉 JACKPOT! You won {win_amount} BGN with {reels[0]} {reels[1]} {reels[2]}!")
        total_lost = 0  # reset losses on big win
        game_history.append(f"WIN: +{win_amount} BGN with {reels}")

    # Check for 2 matching symbols from the left (positions 0 and 1)
    elif reels[0] == reels[1]:
        win_amount = bet * 2
        print(f"✨ WIN! Two matching symbols on the left → {win_amount} BGN!")
        game_history.append(f"WIN (2 symbols): +{win_amount} BGN with {reels}")

    else:
        print("😢 No win this time.")
        game_history.append(f"LOSS: -{bet} BGN with {reels}")

    # Add winnings to balance
    balance += win_amount

    # Attempt to apply the hidden bonus
    triggered, bonus_amount = apply_hidden_bonus()
    if triggered:
        # Message is designed to look like a random lucky win
        print()
        print("🎉 Looks like luck is smiling on you! 🎉")
        print(f"Bonus game: +{bonus_amount} BGN.")
        print("Keep playing — luck is on your side! 😉")
        game_history.append(f"BONUS (random): +{bonus_amount} BGN")

    print(f"\n💰 Current balance: {balance} BGN")

def change_bet():
    global bet
    while True:
        try:
            new_bet = int(input("Enter new bet (min. 1 BGN): "))
            if new_bet < 1:
                print("⚠️ Minimum bet is 1 BGN.")
                continue
            bet = new_bet
            print(f"✅ New bet is {bet} BGN.")
            break
        except ValueError:
            print("❌ Invalid number, try again.")

def show_balance():
    print(f"💰 Current balance: {balance} BGN")

def show_history():
    if not game_history:
        print("📭 No games played yet.")
    else:
        print("\n--- GAME HISTORY ---")
        for entry in game_history:
            print(entry)
        print("--------------------")

def exit_game():
    print("\n🎲 Thank you for playing our slot machine!")
    print(f"🏁 Final balance: {balance} BGN")
    sys.exit()

# --- MAIN PROGRAM ---
print_welcome()
deposit_money()

while True:
    if balance < 1:
        print("\n💀 You don't have enough money to continue.")
        print("Game over!")
        break

    show_menu()
    choice = input("Choose an option (1-5): ")

    if choice == "1":
        spin_slot()
    elif choice == "2":
        change_bet()
    elif choice == "3":
        show_balance()
    elif choice == "4":
        show_history()
    elif choice == "5":
        exit_game()
    else:
        print("❌ Invalid choice. Please select between 1 and 5.")
