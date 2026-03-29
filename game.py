"""
Module: game.py
Author: Cael O'Dell
Description: A simple text-based game that uses gamefunctions.py.
Prompts the user for their name, shows a shop, and spawns an enemy.
Date: 3-29-2026
"""
import gamefunctions


def main():
    """
    Runs the main game loop.

    Parameters:
        None.

    Returns:
        None.
    """
    """greet the player"""
    name = input("What is your name?\n")
    gamefunctions.print_welcome(name, 35)

    hp, gold = 30, 10

    while True:
        action = gamefunctions.get_town_action(hp, gold)
        if action == "1":
            hp, gold = gamefunctions.fight_monster(hp, gold)
        elif action == "2":
            hp, gold = gamefunctions.sleep(hp, gold)
        elif action == "3":
            print("Thanks for playing! Goodbye!")
            break



if __name__ == "__main__":
    main()