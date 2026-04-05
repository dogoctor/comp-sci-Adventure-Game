# gamefunctions.py
# Author: Cael O'Dell
# Description: Function for handling game economy and generating custom enemies
#Computer Science
#4-05-2026

import random
import copy

SHOP_ITEMS = [
    {
        "name": "Obsidian Shard",
        "type": "weapon",
        "price": 15,
        "damage_bonus": 8,
        "max_durability": 12,
        "current_durability": 11,
        "equipped": False
    },
    {
        "name": "Eye of the Warden",
        "type": "consumable",
        "price": 20,
        "description": "A pulsating sculk node. All monsters flee from its signal. Single use."
    },
    {
        "name": "Core Breaker",
        "type": "weapon",
        "price": 3,
        "damage_bonus": 2,
        "max_durability": 6,
        "current_durability": 5,
        "equipped": False
    }
]

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

def get_town_action(state):
    """Displays town menu and returns a validated choice ('1'-'5')."""
    print(f"\nYou are in town.")
    print(f"Current HP: {state['player_hp']} | Current Gold: {state['player_gold']}")
    print("What would you like to do?")
    print("  1) Leave town (Fight Monster)")
    print("  2) Sleep (Restore HP for 5 Gold)")
    print("  3) Visit the Outfitter's Cache")
    print("  4) Equip Item")
    print("  5) Quit")
    while True:
        choice = input("Enter choice: ").strip()
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        print("Invalid choice. Please enter 1-5.")

def display_fight_status(char_hp, monster):
    """Prints current HP for both the player and the monster."""
    print(f"\n  Your HP: {char_hp} | {monster['name']} HP: {monster['health']}")

def fight_monster(state):
    """Runs a full combat encounter. Mutates state in place."""
    monster = random_monster()
    base_damage = 10

    equipped_weapon = next(
        (item for item in state["player_inventory"]
         if item["type"] == "weapon" and item.get("equipped") and item["current_durability"] > 0),
        None
    )
    char_damage = base_damage + (equipped_weapon["damage_bonus"] if equipped_weapon else 0)

    print(f"\nA {monster['name']} appears!")
    print(monster['description'])

    while state["player_hp"] > 0 and monster["health"] > 0:
        display_fight_status(state["player_hp"], monster)

        bane = next(
            (item for item in state["player_inventory"]
             if item["type"] == "consumable" and item["name"] == "Eye of the Warden"),
            None
        )

        print("  1) Attack")
        if bane:
            print("  2) Use Eye of the Warden (instantly defeats monster)")
        print("  3) Run Away")

        while True:
            choice = input("  Enter choice: ").strip()
            valid = ["1", "3"] + (["2"] if bane else [])
            if choice in valid:
                break
            print("  Invalid choice.")

        if choice == "1":
            monster["health"] -= char_damage
            if equipped_weapon:
                equipped_weapon["current_durability"] -= 1
                if equipped_weapon["current_durability"] <= 0:
                    print(f"  Your {equipped_weapon['name']} shatters into volcanic glass!")
                    equipped_weapon["equipped"] = False
                    state["player_inventory"].remove(equipped_weapon)
                    equipped_weapon = None
                    char_damage = base_damage
            if monster["health"] > 0:
                state["player_hp"] -= monster["power"]

        elif choice == "2":
            print(f"  The Eye pulses. The {monster['name']} goes still and retreats into the dark.")
            state["player_inventory"].remove(bane)
            monster["health"] = 0

        elif choice == "3":
            print("You fled into the tunnels.")
            return

    if state["player_hp"] <= 0:
        print("You were knocked out and dragged back to town...")
        state["player_hp"] = 1
    elif monster["health"] <= 0:
        print(f"You defeated the {monster['name']}! Gained {monster['money']} gold.")
        state["player_gold"] += monster["money"]


def sleep(state):
    """Restores HP to 30 for 5 gold. Mutates state in place."""
    cost = 5
    if state["player_gold"] >= cost:
        state["player_gold"] -= cost
        state["player_hp"] = 30
        print(f"You rest at the camp. HP restored to 30. Gold remaining: {state['player_gold']}")
    else:
        print("Not enough gold to rest!")

def show_shop(state):
    """Displays shop, handles purchases, adds items to player inventory."""
    print("\n--- Outfitter's Cache ---")
    for i, item in enumerate(SHOP_ITEMS, 1):
        print(f"  {i}) {item['name']} — {item['price']} gold", end="")
        if item["type"] == "weapon":
            print(f" | +{item['damage_bonus']} damage | Durability: {item['max_durability']}", end="")
        elif item["type"] == "consumable":
            print(f" | {item['description']}", end="")
        print()
    print(f"  0) Leave")
    print(f"Current Gold: {state['player_gold']}")

    while True:
        choice = input("Enter choice: ").strip()
        if choice == "0":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(SHOP_ITEMS)):
            print(f"Invalid choice. Enter 0-{len(SHOP_ITEMS)}.")
            continue
        item_template = SHOP_ITEMS[int(choice) - 1]
        if state["player_gold"] < item_template["price"]:
            print("Not enough gold!")
            continue
        state["player_gold"] -= item_template["price"]
        state["player_inventory"].append(copy.deepcopy(item_template))
        print(f"You pocketed the {item_template['name']}. Gold remaining: {state['player_gold']}")


def equip_item(state):
    """Lets the player equip a weapon. Only shows weapon-type items."""
    weapons = [item for item in state["player_inventory"] if item["type"] == "weapon"]

    if not weapons:
        print("\nNo equippable items in inventory.")
        return

    print("\n--- Equipment ---")
    for i, item in enumerate(weapons, 1):
        equipped_str = " [EQUIPPED]" if item.get("equipped") else ""
        print(f"  {i}) {item['name']} | Durability: {item['current_durability']}/{item['max_durability']}{equipped_str}")
    print("  0) None (unequip)")

    while True:
        choice = input("Enter choice: ").strip()
        if choice == "0":
            for item in state["player_inventory"]:
                if item["type"] == "weapon":
                    item["equipped"] = False
            print("Weapon unequipped.")
            return
        if not choice.isdigit() or not (1 <= int(choice) <= len(weapons)):
            print("Invalid choice.")
            continue
        for item in state["player_inventory"]:
            if item["type"] == "weapon":
                item["equipped"] = False
        selected = weapons[int(choice) - 1]
        selected["equipped"] = True
        print(f"{selected['name']} equipped.")
        return

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