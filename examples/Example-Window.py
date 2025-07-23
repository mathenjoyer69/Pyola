from pyola.input import get_mouse_position
from pyola.window import Window
from pyola.renderer import clear
from pyola.shapes import Rectangle
import time

win = Window(800, 600, "Pyola Demo")
rect = Rectangle(100, 100, 200, 100, color=(1, 0, 0))

while win.running:
    clear((0.1, 0.1, 0.1))
    mouse_x, mouse_y = get_mouse_position()
    rect.x, rect.y = mouse_x - rect.width//2, mouse_y - rect.height//2
    rect.draw()
    win.update()
    time.sleep(1 / 60)

win.close()
