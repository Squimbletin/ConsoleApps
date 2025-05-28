import curses
import time

# Console Sand Simulation
# This program simulates falling sand in a terminal window using the curses library.
# It allows users to summon sand grains by clicking the left mouse button.
# The sand grains will fall down, and if blocked, they will fall diagonally to the left or right.
# The simulation runs continuously until the user presses 'q' to quit.
# 0 = empty space
# 1 = sand grain

def simulation(screen): #simulates the falling sand
    height = len(screen) # Get the height of the screen
    width = len(screen[0]) if height > 0 else 0 # Get the width of the screen

    # Process each row from bottom to top
    for y in range(height - 2, -1, -1):
        for x in range(width): # Process each column in the row
            if screen[y][x] == 1: # If there's a sand grain at (x, y)
                #check if it can fall down
                if screen[y + 1][x] is None:
                    screen[y][x] = None
                    screen[y + 1][x] = 1
                #check if can fall Diagonal right if blocked below
                elif (
                    x + 1 < width and y - 1 >= 0 and
                    screen[y + 1][x] == 1 and
                    screen[y + 1][x + 1] is None and
                    screen[y - 1][x] is None
                ):
                    screen[y][x] = None #reset the current position
                    screen[y + 1][x + 1] = 1 #move the sand grain down and to the right
                #check if can fall Diagonal left if blocked below
                elif (
                    x - 1 >= 0 and y - 1 >= 0 and
                    screen[y + 1][x] == 1 and
                    screen[y + 1][x - 1] is None and
                    screen[y - 1][x] is None
                ):
                    screen[y][x] = None #reset the current position
                    screen[y + 1][x - 1] = 1 #move the sand grain down and to the left

def main(stdscr): # Main function to Summon sand
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION) # Enable mouse events
    curses.curs_set(0) # Hide the cursor
    curses.start_color() # Initialize colours
    stdscr.clear() # Clear the screen
    stdscr.refresh() # Refresh the screen to apply changes


    # Initialize colours to cycle through
    colors = [curses.COLOR_YELLOW, curses.COLOR_RED, curses.COLOR_GREEN,
              curses.COLOR_CYAN, curses.COLOR_MAGENTA, curses.COLOR_BLUE]
    
    #cycle through colors
    for idx, color in enumerate(colors, start=1):
        curses.init_pair(idx, color, curses.COLOR_BLACK)
    color_index = 0

    stdscr.nodelay(True) # I think this makes it so that getch() doesn't block

    height, width = stdscr.getmaxyx() # Get the initial height and width of the screen
    screen = [[None for _ in range(width)] for _ in range(height)] # make an array to represent the screen

    # Initialize mouse state
    mouse_down = False
    mouse_x, mouse_y = 0, 0

    while True: # Main loop to handle input and update the screen

        #insure the user can resize the window without breaking everything
        new_height, new_width = stdscr.getmaxyx()
        if new_height != height or new_width != width:
            height, width = new_height, new_width
            screen = [[None for _ in range(width)] for _ in range(height)]

        key = stdscr.getch() # Get user input

        if key == ord('q'): # Quit the program if 'q' is pressed
            break
        if key == ord('r'): # Reset the screen if 'r' is pressed
            screen = [[None for _ in range(width)] for _ in range(height)]
        elif key == curses.KEY_MOUSE: #SUMMON SAND WHEN MOUSE PRESSED
            try:
                _, x, y, _, bstate = curses.getmouse() #Get mouse position and button state
                if bstate & curses.BUTTON1_PRESSED: # If left button is pressed
                    mouse_down = True # Set mouse down state
                    mouse_x, mouse_y = x, y # Update mouse position
                elif bstate & curses.BUTTON1_RELEASED: # If left button is released
                    mouse_down = False # Reset mouse down state
                else:
                    # If button is still held and mouse moved
                    if mouse_down:
                        mouse_x, mouse_y = x, y
            except curses.error: # Handle any curses errors stopping stupid crashes
                pass

        if mouse_down: # If the mouse is down, summon sand
            for dy in range(-1, 2): # Loop through a 3x3 area around the mouse position
                for dx in range(-1, 2): 
                    if dx * dx + dy * dy <= 1: # Check if within a 1 unit radius
                        ny, nx = mouse_y + dy, mouse_x + dx # Check the new position
                        if 0 <= ny < height and 0 <= nx < width: # Ensure within bounds
                            screen[ny][nx] = 1 # NEW SAND GRAIN

        simulation(screen) #run the simulation

        stdscr.clear() # Clear the screen before drawing

        for y in range(height): # DRAW IN THE SAND 
            for x in range(width): 
                if screen[y][x] == 1: # If there's a sand grain at (x, y)
                    color_pair = curses.color_pair(((x + y) % len(colors)) + 1)  # Cycle through colors based on position
                    try:
                        stdscr.attron(color_pair) # Set the color for the sand grain
                        stdscr.addstr(y, x, "o") # Draw the sand grain (o)
                        stdscr.attroff(color_pair) # Turn off the color attribute
                    except curses.error: # Handle any curses errors to prevent crashes
                        pass
        stdscr.refresh() # Refresh the screen to show changes
        time.sleep(0.01) # Sleep to control the speed of the simulation
curses.wrapper(main) # Start the curses application
