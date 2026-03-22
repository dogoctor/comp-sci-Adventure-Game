"""
Module: game.py
Author: Cael O'Dell
Description: A simple text-based game that uses gamefunctions.py.
Prompts the user for their name, shows a shop, and spawns an enemy.
Date: 3-22-2026
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
    # greet the player
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name, 30)

    # show the shop and handle a purchase
    print("\nWelcome to the field supply shop!")
    gamefunctions.print_shop_menu("Rock Pick", 31.00, "Sample Bag", 12.50)

    money = 50.00
    quantity = int(input("\nHow many Rock Picks would you like to buy? "))
    purchased, remaining = gamefunctions.purchase_item(31.00, money, quantity)
    print(f"Purchased: {purchased} | Remaining balance: ${remaining:.2f}")

    # spawn a random enemy
    print("\nYou venture into the field...")
    monster = gamefunctions.random_monster()
    print(f"A {monster['name']} appears!")
    print(monster['description'])
    print(f"HP: {monster['health']} | Power: {monster['power']} | Loot: ${monster['money']}")


if __name__ == "__main__":
    main()