# 02_shopping_list.py
# Session 2: build a shopping list, then show the items and the total cost.
#
# How to run it:  python3 02_shopping_list.py
#
# Python basics used here:
#   - def            : define your own function
#   - return         : send a value back from a function
#   - lists          : an ordered collection, like [1, 2, 3]
#   - .append()      : add an item to the end of a list
#   - for loop       : do something once for each item in a list
#   - len() / sum()  : count the items / add up the numbers in a list
#   - float()        : turn text like "2.50" into the number 2.5
#
# No imports needed in this file. Three kinds of names:
#   - len(items)        : a built-in function, always available
#                         (like PHP's count() needing no require)
#   - items.append(x)   : a method that every list has
#                         (like Ruby's items << x, JS's items.push(x))
#   - random.randint()  : comes from a module, so it needs "import random"
#                         (import is roughly PHP/Ruby/Node "require")
# To see every built-in:  python3 -c "print(dir(__builtins__))"


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
# In Python, a function must be defined BEFORE the line that calls it runs.
# PHP and JS let you call a function that's written further down the file
# (they "hoist" it). Python doesn't, so functions usually go at the top.
#
#   Python:  def ask_price(name):        (body is the indented block)
#   PHP:     function askPrice($name) { ... }
#   Ruby:    def ask_price(name) ... end
#   JS:      function askPrice(name) { ... }
#
# Python names functions and variables in snake_case, like Ruby.


def ask_price(name):
    # Keep asking until the user types a valid number.
    # This is the same try/except pattern from the guessing game warm-up.
    while True:
        try:
            # float() is like int(), but allows decimals: "2.50" -> 2.5
            # "return" exits the function right away, so it also ends the loop.
            return float(input(f"Price of {name}: "))
        except ValueError:
            print("Please enter a number, like 2.50")

    # About return: Ruby returns the last line automatically.
    # Python does NOT. Without "return", a function gives back None
    # (like PHP/JS returning null/undefined).


def show_list(items):
    print("\nYour shopping list:")  # \n prints a blank line first

    # A "for" loop runs once for each item in the list.
    #
    #   Python:  for item in items:
    #   PHP:     foreach ($items as $item) { ... }
    #   Ruby:    items.each do |item| ... end
    #   JS:      for (const item of items) { ... }
    for item in items:
        print(f"  - {item}")


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

# An empty list. Python lists work like PHP arrays (the [] kind),
# Ruby Arrays, and JS Arrays.
items = []
prices = []

print("Add items to your list. Press Enter on an empty line to finish.")

while True:
    name = input("Item: ")

    # An empty input gives "" (an empty string), so we stop there.
    if name == "":
        break

    # .append() adds to the end of the list.
    #   PHP: $items[] = $name;   Ruby: items << name   JS: items.push(name)
    items.append(name)
    prices.append(ask_price(name))

# "if not items" means "if the list is empty".
# Python treats an empty list as False, like PHP does.
# Careful: in Ruby and JS an empty array counts as TRUE.
if not items:
    print("Your list is empty.")
else:
    show_list(items)

    # len() counts items:  PHP count($items), Ruby/JS items.length
    # sum() adds numbers:  PHP array_sum(), Ruby .sum, JS .reduce(...)
    count = len(items)
    total = sum(prices)

    # {total:.2f} shows the number with exactly 2 decimal places.
    # This also hides float rounding: 0.1 + 0.2 is really
    # 0.30000000000000004 in Python, PHP, Ruby and JS alike.
    print(f"\n{count} items, total: {total:.2f}")
