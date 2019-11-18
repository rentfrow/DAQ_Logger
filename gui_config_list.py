#!/usr/ben/env python3
"""
List config directory using ncurses
for windows ncurse support install windows-ncurses
    pip install windows-ncurses
"""

import time
import curses


def list_config_dir():
    """List the contents of the config directory
    """
    config_path = "./config/"
    config_files = os.listdir(config_path)
    for file in config_files:
        print(file)
    return config_files


def main(stdscr):
    # Check if color can be displayed
    if curses.has_colors():
        print("can do colors")
    else:
        print("can't do colors")

    # disable cursor blinking
    curses.curs_set(0)

    # get height and width of screen
    h, w = stdscr.getmaxyx()

    # create a new color scheme
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)

    # text to be written in center
    text = "Hello, world!"

    # find coordinates for centered text
    x = w//2 - len(text)//2
    y = h//2

    # set color scheme
    stdscr.addstr(y, x, text)

    # unset color scheme
    stdscr.attroff(curses.color_pair(1))

    # update the screen
    stdscr.refresh()

    time.sleep(3)

    # write something on the screen
    stdscr.addstr(1, 1, "|---------------|")
    stdscr.addstr(2, 1, "| Hello, world! |")
    stdscr.addstr(3, 1, "|---------------|")


    # update the screen
    stdscr.refresh()

    # wait for 3 seconds
    time.sleep(3)

    # clear the screen
    stdscr.clear()


if __name__ == "__main__":
    curses.wrapper(main)