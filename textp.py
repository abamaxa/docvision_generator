import curses
import curses.textpad

stdscr = curses.initscr()
# don't echo key strokes on the screen
curses.noecho()
# read keystrokes instantly, without waiting for enter to ne pressed
curses.cbreak()
# enable keypad mode
stdscr.keypad(1)
stdscr.clear()
stdscr.refresh()
win = curses.newwin(5, 60, 5, 10)
tb = curses.textpad.Textbox(win)
text = tb.edit()
curses.beep()
win.addstr(4,1,text.encode('utf_8'))
