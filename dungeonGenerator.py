import random

# import matplotlib.pyplot as plt
# import numpy as np


def generate_room(
    size, open_top=False, open_bottom=False, open_left=False, open_right=False
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
    if random.random() < 0.30:  # 30% chance to have monsters
        monsters_placed = 0
        while monsters_placed < 3:
            x = random.randint(1, size - 2)
            y = random.randint(1, size - 2)
            if room[x][y] == 0:
                room[x][y] = 3
                monsters_placed += 1

    return room


def generate_dungeon(rows, cols):
    dungeon = []
    for row in range(rows):
        row_of_rooms = []
        for col in range(cols):
            # Determine openings based on position in the grid
            open_top = row > 0
            open_bottom = row < rows - 1
            open_left = col > 0
            open_right = col < cols - 1
            room = generate_room(10, open_top, open_bottom, open_left, open_right)
            row_of_rooms.append(room)

        # Combine rooms into dungeon
        for i in range(10):  # Adjusted to match room size
            dungeon_row = []
            for room in row_of_rooms:
                dungeon_row.extend(room[i])
            dungeon.append(dungeon_row)

    # Ensure the bottom row of the dungeon has no openings
    for j in range(len(dungeon[-1])):
        dungeon[-1][j] = 1  # Set the entire bottom row to wall

    return dungeon


# # Generate the dungeon with 5 rows and 7 columns of rooms
# dungeon = generate_dungeon(5, 7)

# # Convert dungeon data to a NumPy array for easier manipulation with matplotlib
# dungeon_array = np.array(dungeon)

# # Define a color map: 0 -> white (free space), 1 -> black (wall), 3 -> red (monster)
# cmap = plt.cm.colors.ListedColormap(["white", "black", "red"])
# bounds = [0, 0.9, 1.9, 3.1]  # Boundaries for colors
# norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

# # Create an Axes instance
# fig, ax = plt.subplots(figsize=(12, 10))
# im = ax.imshow(dungeon_array, cmap=cmap, norm=norm)

# # Create a color bar
# plt.colorbar(im, ax=ax, ticks=[0, 1, 3], orientation="vertical")

# # Set the plot title and remove axis ticks
# ax.set_title("Dungeon Map")
# ax.axis("off")  # Turn off axis numbers and ticks
# plt.show()
