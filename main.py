from random import *
from turtle import *
from freegames import path

car = path('car.gif')
tiles = list(range(20)) * 2
state = {'mark': None}
hide = [True] * 40
revealed_tiles = []  # List to keep track of currently revealed tiles

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
    return int((x + 200) // 50 + ((y + 150) // 50) * 8)  # Adjust y-offset to fit 5 rows

def xy(count):
    "Convert tiles count to (x, y) coordinates."
    return (count % 8) * 50 - 200, (count // 8) * 50 - 150  # Adjust y-offset for 5 rows

def hide_tiles():
    "Hide the two tiles if they don't match."
    global revealed_tiles
    for tile in revealed_tiles:
        hide[tile] = True  # Hide them again
    revealed_tiles = []  # Reset the revealed tiles list

def tap(x, y):
    "Update mark and hidden tiles based on tap."
    global revealed_tiles

    spot = index(x, y)

    if len(revealed_tiles) == 2:  # Prevent revealing more than two tiles at once
        return

    if hide[spot]:  # Only allow tap on hidden tiles
        revealed_tiles.append(spot)  # Add the revealed tile to the list
        hide[spot] = False  # Temporarily show the tile

        if len(revealed_tiles) == 2:  # When two tiles are revealed
            tile1, tile2 = revealed_tiles
            if tiles[tile1] != tiles[tile2]:  # If they don't match, hide them after a delay
                ontimer(hide_tiles, 500)  # 500ms delay to hide the unmatched tiles
            else:
                revealed_tiles = []  # Clear the revealed list if they match

def draw():
    "Draw image and tiles."
    clear()
    goto(0, 0)
    shape(car)
    stamp()

    for count in range(40):  # Iterate only over 40 tiles
        x, y = xy(count)
        if hide[count]:
            square(x, y)  # Draw a hidden square
        else:
            up()
            goto(x + 2, y)
            color('black')
            write(tiles[count], font=('Arial', 30, 'normal'))  # Show tile value if revealed

    update()
    ontimer(draw, 100)

shuffle(tiles)
setup(420, 370, 370, 0)  # Adjust window height for 5 rows
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
