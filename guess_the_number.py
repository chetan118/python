# guess_the_number.py
# My first Python program: a number guessing game.
#
# How to run it:  python3 guess_the_number.py
#
# Python basics used here:
#   - import         : load extra tools that come with Python
#   - variables      : names that store values
#   - print / input  : show text / read what the user types
#   - int()          : turn text like "7" into the number 7
#   - while loop     : repeat code until we say stop
#   - if/elif/else   : choose what to do based on a condition
#   - f-strings      : put variables inside text with {curly braces}

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
    guess = int(input("Your guess: "))

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
