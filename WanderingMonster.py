# wandering_montster.py
# Author: Cael O'Dell
# Description: Functions for moving monster around in the map
#Computer Science
#4-26-2026

import random

class WanderingMonster:
    def __init__(self, x, y, monster_type, color, hp):
        self.x = x
        self.y = y
        self.monster_type = monster_type
        self.color = color
        self.hp = hp

    @classmethod
    def random_spawn(cls, occupied, forbidden, grid_w, grid_h):
        blocked = set(map(tuple, occupied)) | set(map(tuple, forbidden))
        while True:
            x = random.randint(0, grid_w - 1)
            y = random.randint(0, grid_h - 1)
            if (x, y) not in blocked:
                types = [
                    ("Bogged Skeleton",        [0, 128, 0],   random.randint(12, 20)),
                    ("Eagle Formation Golem",   [139, 90, 43], random.randint(60, 110)),
                    ("Rogue CLOD",             [255, 0, 0],   random.randint(25, 60)),
                ]
                monster_type, color, hp = random.choice(types)
                return cls(x, y, monster_type, color, hp)

    @classmethod
    def from_dict(cls, data):
        return cls(
            x=data["x"],
            y=data["y"],
            monster_type=data["monster_type"],
            color=data["color"],
            hp=data["hp"]
        )

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "monster_type": self.monster_type,
            "color": list(self.color),
            "hp": self.hp
        }

    def move(self, occupied, forbidden, grid_w, grid_h, player_pos=None):
        # 50% chance the monster doesn't move at all
        if random.random() < 0.5:
            return

        blocked = set(map(tuple, occupied)) | set(map(tuple, forbidden))

        # Build candidate directions, biased toward player if known
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if player_pos:
            px, py = player_pos
            # Sort so steps toward player are tried first
            directions.sort(key=lambda d: abs((self.x + d[0]) - px) + abs((self.y + d[1]) - py))

        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < grid_w and 0 <= ny < grid_h and (nx, ny) not in blocked:
                self.x = nx
                self.y = ny
                return