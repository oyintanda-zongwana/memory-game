from random import shuffle
from turtle import *
from freegames import path
import time  # To track elapsed time

# Images for each level - using car.gif from freegames package for all levels
car = path('car.gif')  # This is the only image available in freegames
level_images = [car] * 5  # Use the same image for all levels since it's the only one available
tiles = list(range(10)) * 2  # Start with 10 tiles for level 1
state = {'mark': None, 'moves': 0, 'level': 1, 'start_time': None, 'time_per_level': [], 'moves_per_level': []}
hide = []
revealed_tiles = []
level_completed = False
leaderboard = []

TILE_SIZE = 50  # Tile size
TILE_SPACING = 10  # Space between tiles for neatness
MAX_COLUMNS = 6  # Max number of tiles in a row

def init_game():
    "Initialize game based on the current level."
    global tiles, hide, revealed_tiles, level_completed, car
    num_tiles = state['level'] * 10  # Increase tile count per level
    tiles = list(range(num_tiles // 2)) * 2  # Update tiles based on level
    shuffle(tiles)  # Shuffle tiles for randomness
    hide = [True] * num_tiles  # Initialize hidden tiles list
    revealed_tiles = []  # Reset revealed tiles list
    level_completed = False  # Reset level completion flag
    state['moves'] = 0  # Reset move counter
    state['start_time'] = time.time()  # Start the timer for the current level
    
    # Load the image once at the start
    if state['level'] == 1:
        addshape(car)  # Load the image only once

def square(x, y):
    "Draw square with black outline at (x, y)."
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(TILE_SIZE)
        left(90)
    end_fill()

def index(x, y):
    "Convert (x, y) coordinates to tiles index."
    column = int((x + 300) // (TILE_SIZE + TILE_SPACING))
    row = int((y + 250) // (TILE_SIZE + TILE_SPACING))
    spot = column + row * MAX_COLUMNS
    if 0 <= spot < len(tiles):  # Check if the spot is valid
        return spot
    return None

def xy(count):
    "Convert tiles count to (x, y) coordinates."
    x = (count % MAX_COLUMNS) * (TILE_SIZE + TILE_SPACING) - 300
    y = (count // MAX_COLUMNS) * (TILE_SIZE + TILE_SPACING) - 250
    return x, y

def hide_tiles():
    "Hide the two tiles if they don't match."
    global revealed_tiles
    for tile in revealed_tiles:
        hide[tile] = True
    revealed_tiles = []

def tap(x, y):
    "Update mark and hidden tiles based on tap."
    global revealed_tiles

    spot = index(x, y)
    if spot is None:  # Check if the spot is valid
        return

    if len(revealed_tiles) == 2:
        return

    if hide[spot]:
        revealed_tiles.append(spot)
        hide[spot] = False
        state['moves'] += 1  # Increment move counter

        if len(revealed_tiles) == 2:
            tile1, tile2 = revealed_tiles
            if tiles[tile1] != tiles[tile2]:
                ontimer(hide_tiles, 500)
            else:
                revealed_tiles = []

            # Check if all tiles are revealed
            if all(not hidden for hidden in hide):
                complete_level()

def complete_level():
    "Complete the current level and show the image for 2 seconds."
    global level_completed
    if not level_completed:
        level_completed = True
        elapsed_time = time.time() - state['start_time']  # Calculate elapsed time
        state['time_per_level'].append(elapsed_time)
        state['moves_per_level'].append(state['moves'])

        if state['level'] == 5:  # If level 5 is completed, show win screen
            clear()
            goto(0, 0)
            write("You Win!", align="center", font=('Arial', 36, 'bold'))
            show_results()
        else:
            # Show the image for 2 seconds
            ontimer(show_image, 500)

def next_level():
    "Move to the next level."
    if state['level'] < 5:  # Ensure levels only go up to 5
        state['level'] += 1  # Increase level
        init_game()  # Initialize the new level
    else:
        show_results()  # If all levels are done, show results

def show_image():
    "Reveal the full image for 2 seconds, then move to the next level."
    clear()
    goto(0, 0)
    shape(car)  # Use the car shape
    stamp()
    update()

    # Move to the next level after showing the image
    ontimer(next_level, 2000)

def show_results():
    "Display results after all levels are completed."
    clear()
    for level in range(1, 6):
        goto(-300, 150 - 30 * level)
        write(f"Level {level}: Time: {state['time_per_level'][level-1]:.2f}s, Moves: {state['moves_per_level'][level-1]}", font=('Arial', 12, 'normal'))
    ask_for_name()

def ask_for_name():
    "Prompt the player to enter their name for the leaderboard if they meet the requirements."
    name = textinput("Leaderboard", "Congratulations! Enter your name for the leaderboard:")
    if name:
        leaderboard.append((name, sum(state['time_per_level']), sum(state['moves_per_level'])))
        display_leaderboard()

def display_leaderboard():
    "Display the leaderboard."
    clear()
    leaderboard.sort(key=lambda x: (x[1], x[2]))  # Sort by time, then by moves
    goto(0, 150)
    write("Leaderboard", align="center", font=('Arial', 24, 'bold'))
    for rank, (name, time_taken, moves) in enumerate(leaderboard[:5], 1):
        goto(0, 150 - rank * 30)
        write(f"{rank}. {name} - Time: {time_taken:.2f}s, Moves: {moves}", align="center", font=('Arial', 14, 'normal'))

def draw():
    "Draw image, tiles, timer, and moves."
    clear()

    for count in range(len(tiles)):  # Adjust tile drawing based on the number of tiles
        x, y = xy(count)
        if hide[count]:
            square(x, y)
        else:
            up()
            goto(x + TILE_SPACING // 2, y)
            color('black')
            write(tiles[count], font=('Arial', 30, 'normal'))

    # Draw moves and timer outside the game area
    elapsed_time = time.time() - state['start_time']
    up()
    goto(-300, 250)
    color('black')
    write(f"Level: {state['level']}", font=('Arial', 18, 'normal'))
    goto(-300, 220)
    write(f"Moves: {state['moves']}", font=('Arial', 18, 'normal'))
    goto(200, 250)
    write(f"Time: {elapsed_time:.2f}s", font=('Arial', 18, 'normal'))

    update()
    ontimer(draw, 100)

# Adjust window size for more spacing
setup(700, 600, 370, 0)
hideturtle()
tracer(False)
init_game()
onscreenclick(tap)
draw()
done()