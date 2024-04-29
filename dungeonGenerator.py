# dungeonGenerator.py
import random

# import matplotlib.pyplot as plt
# import numpy as np


def generate_room(
    size,
    open_top=False,
    open_bottom=False,
    open_left=False,
    open_right=False,
    cleared_rooms=None,
):
    room = [
        [
            1 if i == 0 or i == size - 1 or j == 0 or j == size - 1 else 0
            for j in range(size)
        ]
        for i in range(size)
    ]

    # Calculate the center of the wall and place two openings
    mid_point = size // 2

    # Openings based on parameters
    if open_top:
        room[0][mid_point - 1] = 0  # Opening left of the center
        room[0][mid_point] = 0  # Opening right of the center
    if open_bottom:
        room[size - 1][mid_point - 1] = 0
        room[size - 1][mid_point] = 0
    if open_left:
        room[mid_point - 1][0] = 0
        room[mid_point][0] = 0
    if open_right:
        room[mid_point - 1][size - 1] = 0
        room[mid_point][size - 1] = 0

    # Randomly decide whether to place monsters in this room
    if (
        cleared_rooms is not None and id(room) not in cleared_rooms
    ):  # Check if the room is cleared
        if random.random() < 0.90:  # 30% chance to have monsters
            monsters_placed = 0
            while monsters_placed < 3:
                x = random.randint(1, size - 2)
                y = random.randint(1, size - 2)
                if room[x][y] == 0:
                    room[x][y] = 3
                    monsters_placed += 1

    return room


def generate_dungeon(rows, cols, cleared_rooms):
    dungeon = []
    total_monsters = 0  # Initialize monster counter
    for row in range(rows):
        row_of_rooms = []
        for col in range(cols):
            # Determine openings based on position in the grid
            open_top = row > 0
            open_bottom = row < rows - 1
            open_left = col > 0
            open_right = col < cols - 1
            room = generate_room(
                6, open_top, open_bottom, open_left, open_right, cleared_rooms
            )
            row_of_rooms.append(room)
            # Count monsters in each room
            for line in room:
                total_monsters += line.count(3)  # Count monsters in this line

        # Combine rooms into dungeon
        for i in range(6):  # Adjusted to match room size
            dungeon_row = []
            for room in row_of_rooms:
                dungeon_row.extend(room[i])
            dungeon.append(dungeon_row)

    # Ensure the bottom row of the dungeon has no openings
    for j in range(len(dungeon[-1])):
        dungeon[-1][j] = 1  # Set the entire bottom row to wall

    return dungeon, total_monsters  # Return the dungeon grid and total monster count
