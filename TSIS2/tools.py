import pygame
import math
from collections import deque


def make_rect(p1, p2):
    x = min(p1[0], p2[0])
    y = min(p1[1], p2[1])
    w = abs(p2[0] - p1[0])
    h = abs(p2[1] - p1[1])
    return pygame.Rect(x, y, w, h)


class BaseTool:
    def on_mouse_down(self, canvas, pos, color, size): pass
    def on_mouse_move(self, canvas, pos, color, size): pass
    def on_mouse_up(self,   canvas, pos, color, size): pass
    def preview(self, surface, pos, color, size):      pass


#Pencil
class PencilTool(BaseTool):
    def __init__(self):
        self.last_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.last_pos = pos
        pygame.draw.circle(canvas, color, pos, max(1, size // 2))

    def on_mouse_move(self, canvas, pos, color, size):
        if self.last_pos:
            pygame.draw.line(canvas, color, self.last_pos, pos, size)
        self.last_pos = pos

    def on_mouse_up(self, canvas, pos, color, size):
        self.last_pos = None


#Straight Line
class LineTool(BaseTool):
    def __init__(self):
        self.start = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.start = pos

    def on_mouse_up(self, canvas, pos, color, size):
        if self.start:
            pygame.draw.line(canvas, color, self.start, pos, size)
        self.start = None

    def preview(self, surface, pos, color, size):
        if self.start:
            pygame.draw.line(surface, color, self.start, pos, size)


#Rectangle
class RectTool(BaseTool):
    def __init__(self): self.start = None
    def on_mouse_down(self, canvas, pos, color, size): self.start = pos
    def on_mouse_up(self, canvas, pos, color, size):
        if self.start: _draw_rect(canvas, color, self.start, pos, size)
        self.start = None
    def preview(self, surface, pos, color, size):
        if self.start: _draw_rect(surface, color, self.start, pos, size)


#Circle
class CircleTool(BaseTool):
    def __init__(self): self.start = None
    def on_mouse_down(self, canvas, pos, color, size): self.start = pos
    def on_mouse_up(self, canvas, pos, color, size):
        if self.start: _draw_circle(canvas, color, self.start, pos, size)
        self.start = None
    def preview(self, surface, pos, color, size):
        if self.start: _draw_circle(surface, color, self.start, pos, size)


#Square
class SquareTool(BaseTool):
    def __init__(self): self.start = None
    def on_mouse_down(self, canvas, pos, color, size): self.start = pos
    def on_mouse_up(self, canvas, pos, color, size):
        if self.start: _draw_square(canvas, color, self.start, pos, size)
        self.start = None
    def preview(self, surface, pos, color, size):
        if self.start: _draw_square(surface, color, self.start, pos, size)


#Right Triangle
class RightTriTool(BaseTool):
    def __init__(self): self.start = None
    def on_mouse_down(self, canvas, pos, color, size): self.start = pos
    def on_mouse_up(self, canvas, pos, color, size):
        if self.start: _draw_right_tri(canvas, color, self.start, pos, size)
        self.start = None
    def preview(self, surface, pos, color, size):
        if self.start: _draw_right_tri(surface, color, self.start, pos, size)


#Equilateral Triangle
class EquiTriTool(BaseTool):
    def __init__(self): self.start = None
    def on_mouse_down(self, canvas, pos, color, size): self.start = pos
    def on_mouse_up(self, canvas, pos, color, size):
        if self.start: _draw_equi_tri(canvas, color, self.start, pos, size)
        self.start = None
    def preview(self, surface, pos, color, size):
        if self.start: _draw_equi_tri(surface, color, self.start, pos, size)


#Rhombus
class RhombusTool(BaseTool):
    def __init__(self): self.start = None
    def on_mouse_down(self, canvas, pos, color, size): self.start = pos
    def on_mouse_up(self, canvas, pos, color, size):
        if self.start: _draw_rhombus(canvas, color, self.start, pos, size)
        self.start = None
    def preview(self, surface, pos, color, size):
        if self.start: _draw_rhombus(surface, color, self.start, pos, size)


#Flood Fill
class FillTool(BaseTool):
    def on_mouse_down(self, canvas, pos, color, size):
        flood_fill(canvas, pos, color)


def flood_fill(canvas, start, new_color):
    x, y = int(start[0]), int(start[1])
    w, h = canvas.get_size()
    if not (0 <= x < w and 0 <= y < h):
        return
    target  = canvas.get_at((x, y))[:3]
    new_rgb = tuple(new_color[:3])
    if target == new_rgb:
        return
    queue   = deque([(x, y)])
    visited = {(x, y)}
    while queue:
        cx, cy = queue.popleft()
        canvas.set_at((cx, cy), new_color)
        for nx, ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)):
            if (nx,ny) not in visited and 0<=nx<w and 0<=ny<h:
                if canvas.get_at((nx, ny))[:3] == target:
                    visited.add((nx, ny))
                    queue.append((nx, ny))


#Text Tool
class TextTool(BaseTool):
    def __init__(self):
        self.active = False
        self.pos    = None
        self.text   = ""
        self.font   = pygame.font.SysFont("Arial", 22)

    def on_mouse_down(self, canvas, pos, color, size):
        self.active = True
        self.pos    = pos
        self.text   = ""

    def add_char(self, ch):
        if self.active:
            self.text += ch

    def backspace(self):
        if self.active and self.text:
            self.text = self.text[:-1]

    def confirm(self, canvas, color):
        if self.active and self.pos and self.text:
            surf = self.font.render(self.text, True, color)
            canvas.blit(surf, self.pos)
        self._reset()

    def cancel(self):
        self._reset()

    def _reset(self):
        self.active = False
        self.text   = ""
        self.pos    = None

    def preview(self, surface, pos, color, size):
        if self.active and self.pos:
            surf = self.font.render(self.text + "|", True, color)
            surface.blit(surf, self.pos)


#Eraser
class EraserTool(BaseTool):
    def __init__(self):
        self.last_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.last_pos = pos
        pygame.draw.circle(canvas, (255,255,255), pos, size * 2)

    def on_mouse_move(self, canvas, pos, color, size):
        if self.last_pos:
            pygame.draw.line(canvas, (255,255,255), self.last_pos, pos, size * 4)
        self.last_pos = pos

    def on_mouse_up(self, canvas, pos, color, size):
        self.last_pos = None

    def preview(self, surface, pos, color, size):
        pygame.draw.circle(surface, (160,160,160), pos, size * 2, 1)


#Private shape renderers
def _draw_rect(surf, color, start, end, width=3):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w, h = abs(start[0]-end[0]), abs(start[1]-end[1])
    if w > 0 and h > 0:
        pygame.draw.rect(surf, color, (x, y, w, h), width)

def _draw_circle(surf, color, start, end, width=3):
    rad = int(math.hypot(start[0]-end[0], start[1]-end[1]))
    if rad > 0:
        pygame.draw.circle(surf, color, start, rad, width)

def _draw_square(surf, color, start, end, width=3):
    side = max(abs(start[0]-end[0]), abs(start[1]-end[1]))
    x = start[0] if end[0] >= start[0] else start[0] - side
    y = start[1] if end[1] >= start[1] else start[1] - side
    if side > 0:
        pygame.draw.rect(surf, color, (x, y, side, side), width)

def _draw_right_tri(surf, color, start, end, width=3):
    points = [start, end, (start[0], end[1])]
    pygame.draw.polygon(surf, color, points, width)

def _draw_equi_tri(surf, color, start, end, width=3):
    side = math.hypot(start[0]-end[0], start[1]-end[1])
    if side < 1:
        return
    height = (math.sqrt(3)/2) * side
    p1 = start
    p2 = (start[0] + side, start[1])
    p3 = (start[0] + side/2, start[1] - height)
    pygame.draw.polygon(surf, color, [p1, p2, p3], width)

def _draw_rhombus(surf, color, start, end, width=3):
    x1, y1 = start
    x2, y2 = end
    mid_x  = (x1+x2)/2
    mid_y  = (y1+y2)/2
    points = [(mid_x,y1),(x2,mid_y),(mid_x,y2),(x1,mid_y)]
    pygame.draw.polygon(surf, color, points, width)