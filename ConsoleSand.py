import curses
import time

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

        if mouse_down:
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx * dx + dy * dy <= 1:
                        ny, nx = mouse_y + dy, mouse_x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            screen[ny][nx] = 1

        simulation(screen)

        stdscr.clear()
        for y in range(height):
            for x in range(width):
                if screen[y][x] == 1:
                    color_pair = curses.color_pair(((x + y) % len(colors)) + 1)
                    try:
                        stdscr.attron(color_pair)
                        stdscr.addstr(y, x, "o")
                        stdscr.attroff(color_pair)
                    except curses.error:
                        pass
        stdscr.refresh()
        time.sleep(0.01)

curses.wrapper(main)
