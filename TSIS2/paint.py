import sys
import pygame
from datetime import datetime
from tools import (
    PencilTool, LineTool, RectTool, CircleTool, SquareTool,
    RightTriTool, EquiTriTool, RhombusTool, FillTool, TextTool, EraserTool
)

#Window / Layout
WIN_W,  WIN_H  = 900, 660
TOOLBAR_H      = 90          # two-row toolbar
CANVAS_H       = WIN_H - TOOLBAR_H

#Colours
WHITE  = (255,255,255)
BLACK  = (  0,  0,  0)
GRAY   = (210,210,210)
DGRAY  = (130,130,130)
LGRAY  = (240,240,240)
ACCENT = ( 50,120,220)

PALETTE = [
    (  0,  0,  0),(255,255,255),(180,180,180),(100,100,100),
    (255,  0,  0),(180,  0,  0),(255,165,  0),(255,255,  0),
    (  0,255,  0),(  0,128,  0),(  0,220,220),(  0,  0,255),
    (  0,  0,160),(128,  0,128),(255,  0,255),(255,182,193),
]

#Brush sizes
SIZES = {1: 2, 2: 5, 3: 10}

#Tool registry
TOOL_MAP = {
    "pencil":   PencilTool,
    "line":     LineTool,
    "rect":     RectTool,
    "circle":   CircleTool,
    "square":   SquareTool,
    "right_tri":RightTriTool,
    "equi_tri": EquiTriTool,
    "rhombus":  RhombusTool,
    "fill":     FillTool,
    "text":     TextTool,
    "eraser":   EraserTool,
}

KEY_TO_TOOL = {
    pygame.K_p: "pencil",
    pygame.K_l: "line",
    pygame.K_r: "rect",
    pygame.K_c: "circle",
    pygame.K_q: "square",
    pygame.K_t: "right_tri",
    pygame.K_e: "equi_tri",
    pygame.K_h: "rhombus",
    pygame.K_f: "fill",
    pygame.K_x: "text",
    pygame.K_w: "eraser",
}

#Toolbar button
class Btn:
    def __init__(self, rect, label):
        self.rect  = pygame.Rect(rect)
        self.label = label

    def draw(self, surf, font, active=False, swatch=None):
        bg = ACCENT if active else LGRAY
        pygame.draw.rect(surf, bg, self.rect, border_radius=5)
        pygame.draw.rect(surf, DGRAY, self.rect, 1, border_radius=5)
        if swatch is not None:
            inner = self.rect.inflate(-4,-4)
            pygame.draw.rect(surf, swatch, inner)
            if swatch == (255,255,255):
                pygame.draw.rect(surf, DGRAY, inner, 1)
        else:
            tc = WHITE if active else BLACK
            t  = font.render(self.label, True, tc)
            surf.blit(t, t.get_rect(center=self.rect.center))

    def hit(self, pos):
        return self.rect.collidepoint(pos)


#Build toolbar buttons
def build_toolbar():
    """Return (tool_buttons dict, size_buttons dict, palette list)."""
    tool_rows = [
        # row 0
        [("pencil","Pencil"),("line","Line"),
         ("rect","Rect"),("circle","Circle"),("square","Square")],
        # row 1
        [("right_tri","R.Tri"),("equi_tri","E.Tri"),("rhombus","Rhombus"),
         ("fill","Fill"),("text","Text"),("eraser","Eraser")],
    ]
    BW, BH, GAP, STARTX = 80, 34, 4, 6
    tool_btns = {}
    for row, items in enumerate(tool_rows):
        for col, (name, label) in enumerate(items):
            x = STARTX + col * (BW + GAP)
            y = 4 + row * (BH + 4)
            tool_btns[name] = Btn((x, y, BW, BH), label)

    # Size buttons (right of tool grid)
    SX = STARTX + 6 * (BW + GAP) + 10
    size_btns = {}
    for i, (k, lbl) in enumerate([(1,"S"),(2,"M"),(3,"L")]):
        size_btns[k] = Btn((SX + i*38, 26, 34, 34), lbl)

    # Palette (two rows of 8)
    PX = SX + 3*38 + 12
    pal = []
    for i, col in enumerate(PALETTE):
        r, c = divmod(i, 8)
        rect = (PX + c*28, 4 + r*28, 24, 24)
        pal.append((Btn(rect, ""), col))

    return tool_btns, size_btns, pal


#Save
def save_canvas(canvas):
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"canvas_{ts}.png"
    pygame.image.save(canvas, name)
    print(f"[PyPaint] Saved → {name}")
    return name


#Main
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Pro Paint")
    clock  = pygame.font.SysFont("Arial", 13, bold=True)   # reuse name below
    clock  = pygame.time.Clock()
    font_s = pygame.font.SysFont("Arial", 12, bold=True)
    font_m = pygame.font.SysFont("Arial", 14)

    # Canvas
    canvas = pygame.Surface((WIN_W, CANVAS_H))
    canvas.fill(WHITE)

    # Tools — one instance each (TextTool must be shared)
    tool_instances = {name: cls() for name, cls in TOOL_MAP.items()}
    #keep a single text instance
    text_tool = tool_instances["text"]

    current_tool     = "pencil"
    current_color    = (0, 0, 255)
    current_size_key = 2
    brush_size       = SIZES[current_size_key]
    drawing          = False
    save_flash       = 0          # frames to show save confirmation

    tool_btns, size_btns, pal_btns = build_toolbar()

    # ── Toolbar draw ────────────────────────────────
    def draw_toolbar():
        pygame.draw.rect(screen, GRAY, (0, 0, WIN_W, TOOLBAR_H))
        pygame.draw.line(screen, DGRAY, (0, TOOLBAR_H-1), (WIN_W, TOOLBAR_H-1))

        for name, btn in tool_btns.items():
            btn.draw(screen, font_s, active=(name == current_tool))

        for k, btn in size_btns.items():
            btn.draw(screen, font_s, active=(k == current_size_key))

        # palette
        for btn, col in pal_btns:
            btn.draw(screen, font_s, swatch=col)
            if col == current_color:
                pygame.draw.rect(screen, ACCENT, btn.rect, 2, border_radius=3)


        # save hint / flash
        if save_flash > 0:
            msg = font_m.render("Saved!", True, (0,160,0))
        else:
            msg = font_m.render("Ctrl+S = Save", True, DGRAY)
        screen.blit(msg, (WIN_W - 180, 56))

        # active tool label bottom-right
        tl = font_s.render(f"Tool: {current_tool.upper()}  Size: {brush_size}px", True, (80,80,80))
        screen.blit(tl, (WIN_W - 240, 76))

    #Event loop
    running = True
    while running:
        clock.tick(60)
        if save_flash > 0:
            save_flash -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Keyboard
            elif event.type == pygame.KEYDOWN:

                # Text tool capture
                if current_tool == "text" and text_tool.active:
                    if event.key == pygame.K_RETURN:
                        text_tool.confirm(canvas, current_color)
                    elif event.key == pygame.K_ESCAPE:
                        text_tool.cancel()
                    elif event.key == pygame.K_BACKSPACE:
                        text_tool.backspace()
                    elif event.unicode and event.unicode.isprintable():
                        text_tool.add_char(event.unicode)
                    continue

                mods = pygame.key.get_mods()

                # Ctrl+S
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    save_canvas(canvas)
                    save_flash = 90
                    continue

                # Tool hotkeys
                if event.key in KEY_TO_TOOL:
                    new_tool = KEY_TO_TOOL[event.key]
                    if new_tool != current_tool:
                        text_tool.cancel()
                    current_tool = new_tool

                # Size hotkeys  (avoid clash with S=save when Ctrl held)
                if not (mods & pygame.KMOD_CTRL):
                    if event.key == pygame.K_1:
                        current_size_key = 1; brush_size = SIZES[1]
                    elif event.key == pygame.K_2:
                        current_size_key = 2; brush_size = SIZES[2]
                    elif event.key == pygame.K_3:
                        current_size_key = 3; brush_size = SIZES[3]

                if event.key == pygame.K_ESCAPE and current_tool == "text":
                    text_tool.cancel()

            #Mouse down
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if my < TOOLBAR_H:
                    # Tool buttons
                    for name, btn in tool_btns.items():
                        if btn.hit(event.pos):
                            if name != current_tool:
                                text_tool.cancel()
                            current_tool = name

                    # Size buttons
                    for k, btn in size_btns.items():
                        if btn.hit(event.pos):
                            current_size_key = k
                            brush_size = SIZES[k]

                    # Palette
                    for btn, col in pal_btns:
                        if btn.hit(event.pos):
                            current_color = col

                else:
                    # Canvas
                    canvas_pos = (mx, my - TOOLBAR_H)
                    drawing = True
                    tool_instances[current_tool].on_mouse_down(
                        canvas, canvas_pos, current_color, brush_size)

            # ── Mouse move ────────────────────────
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    mx, my = event.pos
                    canvas_pos = (mx, my - TOOLBAR_H)
                    tool_instances[current_tool].on_mouse_move(
                        canvas, canvas_pos, current_color, brush_size)

            # ── Mouse up ──────────────────────────
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing:
                    mx, my = event.pos
                    canvas_pos = (mx, my - TOOLBAR_H)
                    tool_instances[current_tool].on_mouse_up(
                        canvas, canvas_pos, current_color, brush_size)
                    drawing = False

        #Render
        screen.blit(canvas, (0, TOOLBAR_H))

        # Preview overlay
        mx, my = pygame.mouse.get_pos()
        if my >= TOOLBAR_H:
            overlay = canvas.copy()
            tool_instances[current_tool].preview(
                overlay, (mx, my - TOOLBAR_H), current_color, brush_size)
            screen.blit(overlay, (0, TOOLBAR_H))

        draw_toolbar()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()