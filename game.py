"""
Module: game.py
Author: Cael O'Dell
Description: A text-based game that uses gamefunctions.py.
Prompts the user for their name, shows a shop, and spawns an enemy.
Date: 4-12-2026
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
    load_choice = input("Load a saved game? (y/n): ").strip().lower()
    if load_choice == "y":
        filename = input("Enter save filename (or press Enter for 'savegame.json'): ").strip()
        if not filename:
            filename = "savegame.json"
        state = gamefunctions.load_game(filename)
        if state is None:
            print("No save file found. Starting new game.")
            load_choice = "n"

    if load_choice != "y":
        name = input("What is your name?\n")
        gamefunctions.print_welcome(name, 35)
        state = {
            "player": name,
            "player_hp": 30,
            "player_gold": 100,
            "player_inventory": []
        }
    else:
        print(f"Welcome back, {state['player']}!")

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
        elif action == "6":
            filename = input("Enter save filename (or press Enter for 'savegame.json'): ").strip()
            if not filename:
                filename = "savegame.json"
            gamefunctions.save_game(state, filename)
            print("Thanks for playing, goodbye!")
            break


if __name__ == "__main__":
    main()