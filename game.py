"""
Module: game.py
Author: Cael O'Dell
Description: A text-based game that uses gamefunctions.py.
Prompts the user for their name, shows a shop, and spawns an enemy.
Date: 4-05-2026
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

    state = {
        "player": name,
        "player_hp": 30,
        "player_gold": 100,
        "player_inventory": []
    }

    while True:
        action = gamefunctions.get_town_action(state)
        if action == "1":
            gamefunctions.fight_monster(state)
        elif action == "2":
            gamefunctions.sleep(state)
        elif action == "3":
            gamefunctions.show_shop(state)
        elif action == "4":
            gamefunctions.equip_item(state)
        elif action == "5":
            print("Thanks for playing, goodbye!")
            break


if __name__ == "__main__":
    main()