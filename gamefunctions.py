"""
Module: gamefunctions.py
Author: Cael O'Dell
Description: This module contains functions for a text-based
geology game. The script generates enemies, handles economy,
and formats the user interface for the shop and welcome screen.
Date: 3-22-2026

"""
import random


def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """
    Calculates max affordable items and remaining balance.

        Parameters:
            itemPrice (float): The cost of the item.
            startingMoney (float): The player's current balance.
            quantityToPurchase (int): The number of items to purchase.

    Returns:
         A tuple of (actual_purchased, leftover_money).
    """
    # figure out the absolute max we can afford
    max_affordable = startingMoney // itemPrice

    # cap the purchase amount so the player's balance doesn't go negative
    actual_purchased = min(quantityToPurchase, max_affordable)

    leftover_money = startingMoney - (actual_purchased * itemPrice)

    return actual_purchased, leftover_money


def random_monster():
    """
    Generates a random geology-themed enemy.
    Parameters:
        None.
    Returns:
        dict: containing monster:
            name
            description
            health
            power
            money
    """
    # initialize the required dictionary keys
    monster = {"name": "", "description": "", "health": 0, "power": 0, "money": 0}

    # pick one of three custom enemies
    enemy_type = random.choice(["Bogged", "Sentient Core Sample", "Malfunctioning CLOD"])

    if enemy_type == "Bogged":
        monster["name"] = "Bogged Skeleton"
        monster[
            "description"] = "A mossy, mushroom-covered skeleton that shoots poison arrows. Watch out for its tipped bow."
        monster["health"] = random.randint(12, 20)
        monster["power"] = random.randint(3, 7)
        monster["money"] = random.randint(2, 6)
    elif enemy_type == "Sentient Core Sample":
        monster["name"] = "Eagle Formation Golem"
        monster[
            "description"] = "A towering mass of sandstone and shale that broke out of the basin analysis lab. It looks heavily cemented."
        monster["health"] = random.randint(60, 110)
        monster["power"] = random.randint(15, 30)
        monster["money"] = random.randint(40, 80)
    elif enemy_type == "Malfunctioning CLOD":
        monster["name"] = "Rogue CLOD"
        monster[
            "description"] = "An automated field assistant that has gone rogue. Its camera is glowing red and the processor is overheating."
        monster["health"] = random.randint(25, 60)
        monster["power"] = random.randint(8, 25)
        monster["money"] = random.randint(15, 30)

    return monster


def print_welcome(name, width):
    """
    Prints a welcome message centered within a specified width.

    Parameters:
        name (str): Name of the player.
        width (int): Total character width of the welcome message.

    Returns:
        None
    """
    welcome_message = f"Hello, {name}!"
    # ^ centers the text based on width parameter
    print(f"{welcome_message:^{width}}")


def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Prints a formatted shop menu with two items and their prices.

    Parameters:
        item1Name (str): The name of the first item.
        item1Price (float): The price of the first item.
        item2Name (str): The name of the second item.
        item2Price (float): The price of the second item.
    Returns: None
    """
    # format the prices to have two decimals and a dollar sign first
    price1_str = f"${item1Price:.2f}"
    price2_str = f"${item2Price:.2f}"

    # using \\ at the end to escape the backslash so it prints one \
    print("/----------------------\\")

    # <12 left aligns to 12 spaces, >8 right aligns
    print(f"| {item1Name:<12} {price1_str:>8}|")
    print(f"| {item2Name:<12} {price2_str:>8}|")
    print("\\----------------------/")


def test_functions():
    """Runs tests for all functions in this module."""
    print('--- Testing purchase_item ---')
    print("Inputs: itemPrice = 123, startingMoney = 1000, quantityToPurchase = 3")
    num_purchased, leftover = purchase_item(123, 1000, 3)
    print(f"Purchased: {num_purchased} | Remaining: {leftover}\n")

    print("Inputs: itemPrice = 123, startingMoney = 201, quantityToPurchase = 3")
    num_purchased, leftover = purchase_item(123, 201, 3)
    print(f"Purchased: {num_purchased} | Remaining: {leftover}\n")

    print("Inputs: itemPrice = 341, startingMoney = 2112, quantityToPurchase = [DEFAULT]")
    num_purchased, leftover = purchase_item(341, 2112)
    print(f"Purchased: {num_purchased} | Remaining: {leftover}\n")

    print('--- Testing random_monster ---')
    enemy1 = random_monster()
    print(enemy1['name'])
    print(enemy1['description'])
    print(f"Stats -> HP: {enemy1['health']} | DMG: {enemy1['power']} | Loot: {enemy1['money']}\n")

    enemy2 = random_monster()
    print(enemy2['name'])
    print(f"Stats -> HP: {enemy2['health']} | DMG: {enemy2['power']} | Loot: {enemy2['money']}\n")

    enemy3 = random_monster()
    print(enemy3['name'])
    print(f"Stats -> HP: {enemy3['health']} | DMG: {enemy3['power']} | Loot: {enemy3['money']}\n")

    print('--- Testing print_welcome ---')
    print_welcome("Surveyor", 20)
    print_welcome("Intern", 20)
    print_welcome("Stratigrapher", 30)
    print("")

    print('--- Testing print_shop_menu ---')
    print_shop_menu("Rock Pick", 31, "Sample Bag", 1.234)
    print_shop_menu("Battery", 0.23, "Rations", 12.34)
    print_shop_menu("Lab Coat", 150.0, "Hard Hat", 75.5)

if __name__ == "__main__":
    test_functions()