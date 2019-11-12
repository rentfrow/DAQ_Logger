#!/usr/ben/env python3
"""
List config directory using ncurses
for windows ncurse support install windows-ncurses
    pip install windows-ncurses
"""

import time
import curses


def main(stdscr):
    # disable cursor blinking
    curses.curs_set(0)

    # get height and width of screen


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