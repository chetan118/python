# 01_guess_the_number.py
# My first Python program: a number guessing game.
#
# How to run it:  python3 01_guess_the_number.py
#
# Python basics used here:
#   - import         : load extra tools that come with Python
#   - variables      : names that store values
#   - print / input  : show text / read what the user types
#   - int()          : turn text like "7" into the number 7
#   - while loop     : repeat code until we say stop
#   - if/elif/else   : choose what to do based on a condition
#   - f-strings      : put variables inside text with {curly braces}
#   - try/except     : catch an error instead of crashing (added in S2)
#   - continue       : skip to the next loop round

# "random" is a built-in module for picking random numbers.
import random

# randint(1, 10) picks a whole number from 1 to 10 (both included).
secret = random.randint(1, 10)

# Count how many guesses the player has made. Starts at 0.
attempts = 0

print("I'm thinking of a number between 1 and 10.")

# "while True" loops forever... until we hit "break" below.
while True:
    # input() always gives back text, so int() converts it to a number.
    # But int("abc") crashes with a ValueError. To handle that, we wrap it:
    #
    #   Python:  try: ... except ValueError: ...
    #   PHP:     try { ... } catch (ValueError $e) { ... }
    #   Ruby:    begin ... rescue ArgumentError ... end
    #   JS:      try { ... } catch (e) { ... }
    #
    # Note for JS: parseInt("abc") doesn't throw, it quietly returns NaN.
    # Python is stricter and raises an error you have to handle.
    # Also, JS catch grabs every error; Python's "except ValueError" only
    # catches that one type (like PHP/Ruby).
    #
    # Only the risky line goes inside "try". If it fails, Python jumps
    # straight to the matching "except" block.
    try:
        guess = int(input("Your guess: "))
    except ValueError:
        print("That's not a number. Try again.")
        # "continue" skips the rest of this loop and starts the next round
        # (same as PHP/JS continue, Ruby's next). So a bad input isn't counted.
        continue

    # Same as: attempts = attempts + 1
    attempts += 1

    # Compare the guess with the secret number.
    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")
    else:
        # The f before the quotes lets us drop {attempts} into the text.
        print(f"Correct! You got it in {attempts} tries.")
        break  # exit the loop, which ends the program
