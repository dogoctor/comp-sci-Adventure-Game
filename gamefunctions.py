# gamefunctions.py
# Author: Cael O'Dell
# Description: Function for handling game economy and generating custom enemies
#Computer Science
#2-29-2026

import random


def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    # figure out the absolute max we can afford
    max_affordable = startingMoney // itemPrice

    # cap the purchase amount so the player's balance doesn't go negative
    actual_purchased = min(quantityToPurchase, max_affordable)

    # calculate the remaining balance
    leftover_money = startingMoney - (actual_purchased * itemPrice)

    return actual_purchased, leftover_money


def print_welcome(name, width):
    """Prints a centered welcome message for the player."""
    message = f"Welcome, {name}!"
    print(message.center(width))


def random_monster():
    # initialize the required dictionary keys
    monster = {
        "name": "",
        "description": "",
        "health": 0,
        "power": 0,
        "money": 0
    }

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
        monster["description"] = "An automated field assistant that has gone rogue. Its camera is glowing red and the processor is overheating."
        monster["health"] = random.randint(25, 60)
        monster["power"] = random.randint(8, 25)
        monster["money"] = random.randint(15, 30)

    return monster

def get_town_action(hp, gold):
    """Displays town menu and returns a validated choice ('1', '2', or '3')."""
    print(f"\nYou are in town.")
    print(f"Current HP: {hp} | Current Gold: {gold}")
    print("What would you like to do?")
    print("  1) Leave town (Fight Monster)")
    print("  2) Sleep (Restore HP for 5 Gold)")
    print("  3) Quit")
    while True:
        choice = input("Enter choice: ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")

def display_fight_status(char_hp, monster):
    """Prints current HP for both the player and the monster."""
    print(f"\n  Your HP: {char_hp} | {monster['name']} HP: {monster['health']}")


def get_fight_action():
    """Displays combat options and returns a validated choice ('1' or '2')."""
    print("  1) Attack")
    print("  2) Run Away")
    while True:
        choice = input("  Enter choice: ").strip()
        if choice in ("1", "2"):
            return choice
        print("  Invalid choice. Enter 1 or 2.")


def fight_monster(hp, gold):
    """Runs a full combat encounter. Returns updated (hp, gold)."""
    monster = random_monster()
    char_damage = 10
    print(f"\nA {monster['name']} appears!")
    print(monster['description'])
    while hp > 0 and monster["health"] > 0:
        display_fight_status(hp, monster)
        action = get_fight_action()
        if action == "1":
            monster["health"] -= char_damage
            if monster["health"] > 0:
                hp -= monster["power"]
        elif action == "2":
            print("You ran away!")
            break
    if hp <= 0:
        print("You were knocked out...")
        hp = 1
    elif monster["health"] <= 0:
        print(f"You defeated the {monster['name']}! Gained {monster['money']} gold.")
        gold += monster["money"]
    return hp, gold


def sleep(hp, gold):
    """Restores HP to 30 for 5 gold. Returns updated (hp, gold)."""
    cost = 5
    if gold >= cost:
        gold -= cost
        hp = 30
        print(f"You sleep at the inn. HP restored to 30. Gold remaining: {gold}")
    else:
        print("Not enough gold to sleep at the inn!")
    return hp, gold

if __name__ == "__main__":
    print("--- Testing purchase_item ---")

    # test 1: standard purchase
    print("Inputs: itemPrice = 123, startingMoney = 1000, quantityToPurchase = 3")
    num_purchased, leftover = purchase_item(123, 1000, 3)
    print(f"Purchased: {num_purchased} | Remaining: {leftover}\n")

    # test 2: attempting to buy too much (capped properly)
    print("Inputs: itemPrice = 123, startingMoney = 201, quantityToPurchase = 3")
    num_purchased, leftover = purchase_item(123, 201, 3)
    print(f"Purchased: {num_purchased} | Remaining: {leftover}\n")

    # test 3: testing the default parameter
    print("Inputs: itemPrice = 341, startingMoney = 2112, quantityToPurchase = [DEFAULT]")
    num_purchased, leftover = purchase_item(341, 2112)
    print(f"Purchased: {num_purchased} | Remaining: {leftover}\n")

    print("--- Testing random_monster ---")

    # test 1
    print("Inputs: None (Generating random enemy...)")
    enemy1 = random_monster()
    print(enemy1['name'])
    print(enemy1['description'])
    print(f"Stats -> HP: {enemy1['health']} | DMG: {enemy1['power']} | Loot: {enemy1['money']}\n")

    # test 2
    print("Inputs: None (Generating random enemy...)")
    enemy2 = random_monster()
    print(enemy2['name'])
    print(f"Stats -> HP: {enemy2['health']} | DMG: {enemy2['power']} | Loot: {enemy2['money']}\n")

    # test 3
    print("Inputs: None (Generating random enemy...)")
    enemy3 = random_monster()
    print(enemy3['name'])
    print(f"Stats -> HP: {enemy3['health']} | DMG: {enemy3['power']} | Loot: {enemy3['money']}")