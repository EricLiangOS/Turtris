# -----import statements-----
import random
import turtle
import leaderboard
import time


# -----game configuration----

# Leaderboard configurations
leaderboard_file_name = "leaderboard_file.txt"
leaderboard_values = []
score = 0
username = input("Username: ")

grid_width = 10
grid_height = 24

# Variable that determines if the game can continue
continue_game = False

# Variable that checks if you have recently swapped (To prevent infinite swaos)
have_swapped = False

# Set up 10 by 24 grid (Number corresponds to color, 0 is empty)
grid = []
for i in range(grid_height):
    row = []
    for j in range(grid_width):
        row.append(0)
    grid.append(row)

# Set up 5 by 6 storage grid (Similar to actual grid)
storage = []
for i in range(5):
    row = []
    for j in range(6):
        row.append(0)
    storage.append(row)

# Set up 5 by 6 next_block grid (Similar to actual grid)
preview = []
for i in range(5):
    row = []
    for j in range(6):
        row.append(0)
    preview.append(row)

standard_font = ("Times New Roman", 24, "normal")
small_font = ("Times New Roman", 18, "normal")


button_colors = ["orangered", "gold", "chartreuse"]
button_names = ["Blitz Mode", "Normal Mode", "Turtle Mode"]

# Configurations for the 3 gamemodes
blitz_speed = 0.05
blitz_multiplier = 2.5
normal_speed = 0.1
normal_multiplier = 1.75
turtle_speed = 0.2
turtle_multiplier = 1

mode_speeds = [blitz_speed, normal_speed, turtle_speed]
mode_multiplyers = [blitz_multiplier, normal_multiplier, turtle_multiplier]


# Different shapes (Numbers represent color)
shapes = [[[1, 1, 1, 1]], [[2, 0, 0], [2, 2, 2]], [[0, 0, 3], [3, 3, 3]], [[4, 4], [
    4, 4]], [[0, 5, 5], [5, 5, 0]], [[0, 6, 0], [6, 6, 6]], [[7, 7, 0], [0, 7, 7]]]

block = random.choice(shapes)
next_block = random.choice(shapes)
block_x = 5
block_y = 0

# -----initialize turtles-----

# Set up screen configurations
wn = turtle.Screen()
wn.tracer(False)
wn.bgcolor("dimgrey")
wn.setup(500, 700)
wn.title("TURTRIS")

pen = turtle.Turtle()
pen.speed(0)
pen.penup()
pen.hideturtle()
pen.shape("square")
pen.color("white")

storage_pen = turtle.Turtle()
storage_pen.speed(0)
storage_pen.penup()
storage_pen.hideturtle()
storage_pen.shape("square")
storage_pen.color("white")

preview_pen = turtle.Turtle()
preview_pen.speed(0)
preview_pen.penup()
preview_pen.hideturtle()
preview_pen.shape("square")
preview_pen.color("white")

temp_button = turtle.Turtle()
temp_button.speed(0)
temp_button.shapesize(7.6)
temp_button.shape("square")

home_button = turtle.Turtle()
home_button.setpos(175, 300)
home_button.color("yellow")
home_button.shape("square")
home_button.shapesize(2.5)


# -----game functions--------
def home_screen():
    global leaderboard_values, score, speed, active_multiplyer, active_button, standard_font, small_font, stored_block, continue_game, have_swapped, grid, storage, preview, go_home, grid_width, grid_height

    wn.clear()
    pen.clear()
    storage_pen.clear()
    preview_pen.clear()
    wn.bgcolor("dimgrey")
    wn.tracer(False)

    pen.penup()
    pen.color("white")
    temp_button.penup()
    pen.setpos(0, 270)
    pen.write("TURTRIS", move=True, align="center", font=standard_font)

    # Default values
    leaderboard_values = []
    score = 0
    have_swapped = False
    continue_game = False
    go_home = True

    # Default settings
    speed = normal_speed
    active_multiplyer = normal_multiplier
    active_button = "Normal Mode"

    stored_block = None

    # Set up all the grids
    # Set up 10 by 24 grid (Number corresponds to color, 0 is empty)
    grid = []
    for i in range(grid_height):
        row = []
        for j in range(grid_width):
            row.append(0)
        grid.append(row)

    # Set up 5 by 6 storage grid (Similar to actual grid)
    storage = []
    for i in range(5):
        row = []
        for j in range(6):
            row.append(0)
        storage.append(row)

    # Set up 5 by 6 next_block grid (Similar to actual grid)
    preview = []
    for i in range(5):
        row = []
        for j in range(6):
            row.append(0)
        preview.append(row)
    # Create the buttons for the gamemodes and trigger them when clicked
    for i in range(3):
        temp_button.color(button_colors[i])
        temp_button.penup()
        temp_button.sety(145-i*190)
        temp_button.stamp()

        wn.onclick(lambda x, y: button_pressed(x, y))

        pen.setpos(0, 225-i*190)
        pen.write(button_names[i], move=False, align="center", font=small_font)


def button_pressed(x_coor, y_coor):
    global mode_multiplyers, mode_speeds, button_names, active_multiplyer, active_button, speed, continue_game, go_home

    # Check if home_button is pressed
    if x_coor < 200 and x_coor > 150:
        if y_coor < 325 and y_coor > 275:
            home_screen()
            go_home = True
            return

    if continue_game:
        return False

    button_index = -1

    #Assigns intdexes to the buttons so certain pressed buttons will have certain triggers
    if x_coor < 74 and x_coor > -74:
        if y_coor < 211 and y_coor > 60:
            button_index = 0
        elif y_coor < 20 and y_coor > -130:
            button_index = 1
        elif y_coor < -170 and y_coor > -320:
            button_index = 2

    #Senses a button has been pressed and will begin the game (Assigns difficulty stats here)
    if button_index > -1:
        wn.clear()
        wn.bgcolor("dimgrey")

        pen.setpos(-67, 280)
        pen.write("TURTRIS", move=True, align="left", font=standard_font)

        active_button = button_names[button_index]
        speed = mode_speeds[button_index]
        active_multiplyer = mode_multiplyers[button_index]

        # Event Handlers
        wn.onkeypress(lambda: left(), "a")
        wn.onkeypress(lambda: right(), "d")
        wn.onkeypress(lambda: rotate(), "w")
        wn.onkeypress(lambda: speed_down(), "s")
        wn.onkeypress(lambda: swap_blocks(), "r")
        wn.onkeypress(lambda: drop(), "space")
        # Alternative Controls
        wn.onkeypress(lambda: left(), "Left")
        wn.onkeypress(lambda: right(), "Right")
        wn.onkeypress(lambda: rotate(), "Up")
        wn.onkeypress(lambda: speed_down(), "Down")
        wn.onkeypress(lambda: swap_blocks(), ".")
        wn.onkeypress(lambda: drop(), "/")

        continue_game = True
        wn.tracer(False)
        actual_game()

#Creates new block by picking new shape and resetting position
def new_block():
    global block_y, block_x, block, next_block, shapes

    block = next_block
    next_block = random.choice(shapes)
    draw_next_block()
    block_x = 5
    block_y = 0

#Blocks have overflowed
def game_over():
    global leaderboard_file_name, score, active_button
    wn.clear()
    wn.bgcolor("dimgrey")
    home_button.stamp()
    home_button.color("white")
    home_button.sety(250)
    home_button.write("Home", move=False, align="center", font=small_font)
    home_button.sety(300)
    home_button.color("yellow")
    # Get the new leaderboard_values
    made_leaderboard = leaderboard.update_leaderboard(
        leaderboard_file_name, leaderboard_values, username, int(score), active_button)
    # Draw leaderboard values
    leaderboard.draw_leaderboard(
        made_leaderboard, leaderboard_file_name, pen, int(score))

    # See if home button has been pressed
    wn.onclick(lambda x, y: button_pressed(x, y))

#Redraws score
def update_score(score):
    pen.goto(-127.5, 255)
    pen.color("white")
    pen.write("Score: " + str(int(score)), move=False,
              align="left", font=standard_font)

#Checks if any rows are filled or if game is over
def update_grid():
    global grid, score, active_multiplyer, continue_game

    for i in range(len(grid)):
        filled = True

        for j in range(len(grid[0])):

            # Check if row is filled
            if grid[i][j] == 0:
                filled = False

        if filled:
            score += 10 * active_multiplyer
            # This way, values received in a single turn can increase exponentially
            active_multiplyer += 0.5
            update_score(score)

            # Move rest of grid downwards
            grid.pop(i)
            grid.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ])

    # Check if game over:
    for i in range(2):
        for j in range(4, 8):
            if grid[i][j] != 0:
                continue_game = False
                return
    continue_game = True

# Function that redraws grid after every block
def draw_grid():
    global grid
    pen.clear()
    top = 225
    left = -170

    colors = ["black", "lightblue", "blue",
              "darkorange", "yellow", "lime", "purple", "red"]

    for i in range(len(grid)):

        for j in range(len(grid[i])):
            i_pos = top - (i * 22)
            j_pos = left + (j * 22)

            pen.color(colors[grid[i][j]])
            pen.setpos(j_pos, i_pos)
            pen.stamp()

# Function that redraws the container
def draw_storage():
    global storage
    storage_pen.clear()
    top = 120
    left = 100

    colors = ["dimgrey", "lightblue", "blue",
              "darkorange", "yellow", "lime", "purple", "red"]

    for i in range(len(storage)):

        for j in range(len(storage[i])):
            i_pos = top - (i * 22)
            j_pos = left + (j * 22)

            storage_pen.color(colors[storage[i][j]])
            storage_pen.setpos(j_pos, i_pos)
            storage_pen.stamp()

# Function that redraws the next block container
def draw_next_block():
    global preview, next_block
    preview_pen.clear()
    top = -100
    left = 100

    # First clear space
    preview = []
    for i in range(5):
        row = []
        for j in range(6):
            row.append(0)
        preview.append(row)

    # Put next block into position
    for i in range(len(next_block)):
        for j in range(len(next_block[0])):
            preview[i+1][j+2] = next_block[i][j]

    # Actual drawing part of the grid
    colors = ["dimgrey", "lightblue", "blue",
              "darkorange", "yellow", "lime", "purple", "red"]

    for i in range(len(preview)):

        for j in range(len(preview[i])):
            i_pos = top - (i * 22)
            j_pos = left + (j * 22)

            preview_pen.color(colors[preview[i][j]])
            preview_pen.setpos(j_pos, i_pos)
            preview_pen.stamp()


# Function to swap blocks between storage and main game
def swap_blocks():
    global block_x, block, storage, stored_block, have_swapped, block_y

    if have_swapped:
        return
    temp_block = block

    clear_previous()

    if not stored_block:
        new_block()
        update_grid()
    else:
        block = stored_block
        block_y = 0
        block_x = 5
        clear_previous_storage()

    stored_block = temp_block

    update_grid()
    update_storage()
    have_swapped = True

# All the functions regarding movement
def clear_previous():
    global grid, block_x, block_y, block

    for i in range(len(block)):
        for j in range(len(block[0])):

            if(block[i][j] != 0):
                grid[i + block_y][j + block_x] = 0

# Essentially wipe clean the storage grid
def clear_previous_storage():
    global storage, stored_block

    for i in range(5):
        row = []
        for j in range(6):
            row.append(0)
            storage[i] = row

#Moves x-position left
def left():
    global grid, block_x, block, grid_height, block_y

    # Check if block can fit in the left side
    if block_x > 0 and can_move_down() and block_y < grid_height - 2:
        if grid[block_y][block_x - 1] == 0:
            clear_previous()
            block_x -= 1
            time.sleep(0.0003)

#Moves x-position right
def right():
    global grid, block_x, block, grid_height

    # Check if block can fit in the right side
    if block_x < grid_height - len(block[0]) and can_move_down() and block_y < grid_height - 2:
        if grid[block_y][block_x + len(block[0])] == 0:
            clear_previous()
            block_x += 1
            time.sleep(0.0003)

#Checks for any collisions with blocks below
def can_move_down():
    global grid, block_x, block

    movable = True
    for j in range(len(block[0])):
        for i in range(len(block)):
            # Check if squares below are filled
            if(block[i][j] != 0):
                if i+1 < len(block) and block[i+1][j] != 0:
                    continue
                if (block_y + i < 23) and (grid[block_y + i+1][j + block_x] != 0):
                    movable = False
                    break
    return movable

#Decreases y-coordinate by 1 if can move down
def speed_down():
    global block_y, score, active_multiplyer, block, grid_height

    # Repeat procedure to move block down if possible
    if block_y != grid_height - len(block) and can_move_down():
        clear_previous()
        block_y += 1
        draw_block()
        score += 0.25*active_multiplyer

#Continually moves down until collision is detected or hits the ground
def drop():
    global block_y, score, active_multiplyer, block, grid_height

    # Repeat procedure to move block down if possible until not possible
    while block_y != grid_height - len(block) and can_move_down():
        clear_previous()
        block_y += 1
        draw_block()
        score += 1.5 * active_multiplyer

#Rotates block 90 degrees
def rotate():
    global block, block_x

    clear_previous()
    rotated_block = []
    for i in range(len(block[0])):
        new_row = []

        for j in range(len(block)-1, -1, -1):

            new_row.append(block[j][i])
        rotated_block.append(new_row)

    right_side = block_x + len(rotated_block[0])
    if right_side < len(grid[0]):
        block = rotated_block
    time.sleep(0.0007)

#Draws the block onto its new position in the grid based on x and y coordinates
def draw_block():
    global grid, block_x, block_y, block

    for i in range(len(block)):
        for j in range(len(block[0])):
            if(block[i][j] != 0) and (block_y + i >= 0):
                grid[block_y + i][block_x + j] = block[i][j]

# Similar to update_grid and draw_block, replaces the old storage w/ new one
def update_storage():
    global storage, stored_block

    for i in range(len(stored_block)):
        for j in range(len(stored_block[0])):
            storage[i+1][j+2] = stored_block[i][j]

#Loop that keeps running until game over and loads the leaderboard
def actual_game():
    global block_x, block_y, score, speed, continue_game, have_swapped, small_font, go_home, grid_height

    new_block()
    home_button.stamp()
    home_button.color("white")
    home_button.sety(250)
    home_button.write("Home", move=False, align="center", font=small_font)
    home_button.sety(300)
    home_button.color("yellow")
    go_home = False

    while continue_game:
        wn.onclick(lambda x, y: button_pressed(x, y))

        # Main game loop
        wn.update()
        # See if home button has been pressed
        if go_home:
            return
        # Check if it's at the bottom
        if block_y == grid_height - len(block):
            have_swapped = False
            new_block()
            update_grid()
        # Check if it has blocks beneath
        elif can_move_down():
            # The block is able to move down
            # Erase the current shape
            clear_previous()

            # Move the shape downwards
            block_y += 1

            # Draw the shape again
            draw_block()

        # This line means the block has touched the blocks below
        else:
            have_swapped = False
            new_block()
            update_grid()

        # Draw the screen
        draw_grid()
        draw_storage()
        update_score(score)
        if go_home:
            return    
        storage_pen.color("white")
        storage_pen.setpos(158, 140)
        storage_pen.write("Stored Block", move=False,
                          align="center", font=small_font)

        preview_pen.color("white")
        preview_pen.setpos(158, -80)
        preview_pen.write("Next Block", move=False,
                          align="center", font=small_font)

        # Speed delay up a little bit
        speed = speed*0.998
        time.sleep(speed)

    if not go_home:
        game_over()


wn.listen()

# -----events----------------
#Triggers the home screen which can lead to the games
home_screen()


wn.update()
wn.mainloop()
