from math import *
import glfw
import time
import pyola

class Entry:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.base_color = (130/255, 130/255, 130/255)
        self.active_color = (170/255, 170/255, 170/255)
        self.entry_rect = pyola.shapes.Rectangle(x, y, width, height)
        self.text = ''
        self.active = False
        self.was_pressed = False
        self.last_keys = set()

    def draw(self):
        color = self.active_color if self.active else self.base_color
        self.entry_rect.color = color
        self.entry_rect.draw()

    def handle_event(self):
        mx, my = pyola.input.get_mouse_position()
        now_pressed = pyola.input.is_mouse_button_pressed(glfw.MOUSE_BUTTON_LEFT)

        if pyola.input.collide_pos(self.entry_rect, (mx, my)):
            if now_pressed and not self.was_pressed:
                self.active = not self.active  # toggle only once when click starts

        self.was_pressed = now_pressed  # store current state for next frame

    def handle_keyboard(self):
        if not self.active:
            return

        # Handle Enter and Backspace via polling
        if pyola.input.is_key_pressed(glfw.KEY_BACKSPACE):
            if glfw.KEY_BACKSPACE not in self.last_keys:
                self.text = self.text[:-1]

        if pyola.input.is_key_pressed(glfw.KEY_ENTER):
            if glfw.KEY_ENTER not in self.last_keys:
                self.active = False

        # Handle typed characters via char callback
        for char in pyola.input.get_typed_chars():
            self.text += char

        self.last_keys = {
            key for key in [glfw.KEY_BACKSPACE, glfw.KEY_ENTER]
            if pyola.input.is_key_pressed(key)
        }
        print(self.text)

class Graph:
    def __init__(self):
        self.screen = pyola.window.Window(800, 600)
        self.offset = [0, 0]
        self.last_mouse_pos = (0, 0)
        self.dragging = False
        self.entry = Entry(20, 20, 200, 40)

    def run(self):
        while self.screen.running:
            pyola.renderer.clear((0, 0, 0))
            if pyola.input.is_mouse_button_pressed(glfw.MOUSE_BUTTON_RIGHT):
                if not self.dragging:
                    self.dragging = True
                    self.last_mouse_pos = pyola.input.get_mouse_position()
                else:
                    mouse_x, mouse_y = pyola.input.get_mouse_position()
                    dx = mouse_x - self.last_mouse_pos[0]
                    dy = mouse_y - self.last_mouse_pos[1]
                    self.offset[0] += dx
                    self.offset[1] += dy
                    self.last_mouse_pos = (mouse_x, mouse_y)
            else:
                self.dragging = False
            self.entry.handle_event()
            self.entry.handle_keyboard()

            try:
                self.draw_func(self.entry.text)
            except (SyntaxError, NameError, TypeError, AttributeError, IndexError, OverflowError):
                pass
            self.draw()
            self.entry.draw()
            self.screen.update()

        self.screen.close()

    def draw(self):
        width, height = self.screen.width, self.screen.height
        ox, oy = self.offset
        #horizontal line
        line1 = pyola.shapes.Line((0, height//2 + oy), (width, height//2 + oy))
        #vertical line
        line2 = pyola.shapes.Line((width//2 + ox, 0), (width//2 + ox, height))
        #horizontal lines
        lines = []
        for i in range(0, height, 100):
            line = pyola.shapes.Line((0, i + oy % 100), (width, i + oy % 100), color=(0.4, 0.4, 0.4))
            lines.append(line)
        for i in range(0, width, 100):
            line = pyola.shapes.Line((i + ox % 100, 0), (i + ox % 100, height), color=(0.4, 0.4, 0.4))
            lines.append(line)

        for line in lines:
            line.draw()
        line1.draw()
        line2.draw()

    def draw_func(self, func):
        center = (self.screen.width//2 + self.offset[0], self.screen.height//2 + self.offset[1])
        points = []
        scale_factor = 20
        parts = func.split(":")#':' separates the function from the scaling factor
        function = parts[0]
        if len(parts) > 1:
            try:
                scale_factor = float(parts[1])
            except ValueError:
                pass
        for i in range(-1500, 1500, 1):
            x = i/15
            temp_function = function.replace('X', f'({x})')
            try:
                y = eval(temp_function)
            except ZeroDivisionError:
                y = nan
            screen_x = center[0] + x * scale_factor
            screen_y = center[1] - y * scale_factor
            circle = pyola.shapes.Circle(screen_x, screen_y, 1, color=(1, 0, 0))
            points.append(circle)

        #for point in points:
        #    point.draw()
        for i in range(len(points)-1):
            startpos = (points[i].x, points[i].y)
            endpos = (points[i+1].x, points[i+1].y)
            line = pyola.shapes.Line(startpos, endpos, color=(1, 0, 0))
            line.draw()

g = Graph()
g.run()