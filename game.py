"""
Module: game.py
Author: Cael O'Dell
Description: A text-based game that uses gamefunctions.py.
Prompts the user for their name, shows a shop, and spawns an enemy.
Date: 4-26-2026
"""
import gamefunctions
import random
from WanderingMonster import WanderingMonster


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
        else:
            state["monsters"] = [
                WanderingMonster.from_dict(d) for d in state.get("monsters", [])
            ]
            state["map_state"].pop("monster_pos", None)
            print(f"Welcome back, {state['player']}!")

    if load_choice != "y":
        name = input("What is your name?\n")
        gamefunctions.print_welcome(name, 35)
        state = {
            "player": name,
            "player_hp": 30,
            "player_gold": 100,
            "player_inventory": [],
            "monsters": [],
            "map_state": {
                "player_pos": [5, 5],
                "town_pos": [0, 0],
            }
        }
        forbidden = [(0, 0)]  # just town; player pos is distinct
        state["monsters"].append(WanderingMonster.random_spawn([(5, 5)], forbidden, 10, 10))

    while True:
        action = gamefunctions.get_town_action(state)
        if action == "1":
            while True:
                result = gamefunctions.run_map_interface(state)
                if result == "town":
                    break

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