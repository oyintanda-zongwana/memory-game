from random import *
from turtle import *
from freegames import path
import time  # To track elapsed time

car = path('car.gif')
tiles = list(range(10)) * 2  # Start with 10 tiles for level 1
state = {'mark': None, 'moves': 0, 'level': 1, 'start_time': None, 'time_per_level': [], 'moves_per_level': []}
hide = []
revealed_tiles = []
level_completed = False
leaderboard = []

def init_game():
    "Initialize game based on the current level."
    global tiles, hide, revealed_tiles, level_completed
    num_tiles = state['level'] * 10  # Increase tile count per level
    tiles = list(range(num_tiles // 2)) * 2  # Update tiles based on level
    shuffle(tiles)  # Shuffle tiles for randomness
    hide = [True] * num_tiles  # Initialize hidden tiles list
    revealed_tiles = []  # Reset revealed tiles list
    level_completed = False  # Reset level completion flag
    state['moves'] = 0  # Reset move counter
    state['start_time'] = time.time()  # Start the timer for the current level

def square(x, y):
    "Draw square with black outline at (x, y)."
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()

def index(x, y):
    "Convert (x, y) coordinates to tiles index."
    return int((x + 200) // 50 + ((y + 150) // 50) * 8)

def xy(count):
    "Convert tiles count to (x, y) coordinates."
    return (count % 8) * 50 - 200, (count // 8) * 50 - 150

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
    "Complete the current level and move to the next or finish the game."
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
            state['level'] += 1  # Move to the next level
            ontimer(init_game, 1000)  # Wait for 1 second before starting next level

def show_results():
    "Display results after all levels are completed."
    clear()
    for level in range(1, 6):
        goto(-200, 150 - 30 * level)
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
    goto(0, 0)
    shape(car)
    stamp()

    for count in range(len(tiles)):  # Adjust tile drawing based on the number of tiles
        x, y = xy(count)
        if hide[count]:
            square(x, y)
        else:
            up()
            goto(x + 2, y)
            color('black')
            write(tiles[count], font=('Arial', 30, 'normal'))

    # Draw moves and timer
    elapsed_time = time.time() - state['start_time']
    up()
    goto(-180, 160)
    color('black')
    write(f"Level: {state['level']}", font=('Arial', 14, 'normal'))
    goto(-180, 140)
    write(f"Moves: {state['moves']}", font=('Arial', 14, 'normal'))
    goto(100, 160)
    write(f"Time: {elapsed_time:.2f}s", font=('Arial', 14, 'normal'))

    update()
    ontimer(draw, 100)

init_game()
setup(420, 370, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
