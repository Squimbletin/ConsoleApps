import curses
import time

def simulation(screen):
    height = len(screen)
    width = len(screen[0]) if height > 0 else 0

    for y in range(height - 2, -1, -1):
        for x in range(width):
            if screen[y][x] == 1:
                # Fall straight down
                if screen[y + 1][x] is None:
                    screen[y][x] = None
                    screen[y + 1][x] = 1
                # Diagonal right if blocked below
                elif (
                    x + 1 < width and y - 1 >= 0 and
                    screen[y + 1][x] == 1 and
                    screen[y + 1][x + 1] is None and
                    screen[y - 1][x] is None
                ):
                    screen[y][x] = None
                    screen[y + 1][x + 1] = 1
                # Diagonal left if blocked below
                elif (
                    x - 1 >= 0 and y - 1 >= 0 and
                    screen[y + 1][x] == 1 and
                    screen[y + 1][x - 1] is None and
                    screen[y - 1][x] is None
                ):
                    screen[y][x] = None
                    screen[y + 1][x - 1] = 1

def main(stdscr):
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.curs_set(0)
    curses.start_color()
    stdscr.clear()
    stdscr.refresh()

    colors = [curses.COLOR_YELLOW, curses.COLOR_RED, curses.COLOR_GREEN,
              curses.COLOR_CYAN, curses.COLOR_MAGENTA, curses.COLOR_BLUE]
    for idx, color in enumerate(colors, start=1):
        curses.init_pair(idx, color, curses.COLOR_BLACK)
    color_index = 0

    stdscr.nodelay(True)

    height, width = stdscr.getmaxyx()
    screen = [[None for _ in range(width)] for _ in range(height)]

    mouse_down = False
    mouse_x, mouse_y = 0, 0

    while True:
        new_height, new_width = stdscr.getmaxyx()
        if new_height != height or new_width != width:
            height, width = new_height, new_width
            screen = [[None for _ in range(width)] for _ in range(height)]

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_MOUSE:
            try:
                _, x, y, _, bstate = curses.getmouse()
                if bstate & curses.BUTTON1_PRESSED:
                    mouse_down = True
                    mouse_x, mouse_y = x, y
                elif bstate & curses.BUTTON1_RELEASED:
                    mouse_down = False
                else:
                    # If button is still held and mouse moved
                    if mouse_down:
                        mouse_x, mouse_y = x, y
            except curses.error:
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
