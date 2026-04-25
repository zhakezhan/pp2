import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pro Paint: Geometry Edition")
    
    # Main drawing surface
    canvas = pygame.Surface((800, 600))
    canvas.fill((255, 255, 255))
    
    clock = pygame.time.Clock()
    
    # Brush/Tool State
    radius = 15
    # Modes: brush, rect, circle, square, right_tri, equi_tri, rhombus, eraser
    mode = 'brush' 
    current_color = (0, 0, 255) # Default Blue
    start_pos = None
    
    # Palette configuration
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "black": (0, 0, 0),
        "yellow": (255, 255, 0),
        "purple": (128, 0, 128),
        "orange": (255, 165, 0)
    }

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                # Hotkeys for Tools
                if event.key == pygame.K_1: mode = 'brush'
                if event.key == pygame.K_2: mode = 'rect'
                if event.key == pygame.K_3: mode = 'circle'
                if event.key == pygame.K_4: mode = 'square'
                if event.key == pygame.K_5: mode = 'right_tri'
                if event.key == pygame.K_6: mode = 'equi_tri'
                if event.key == pygame.K_7: mode = 'rhombus'
                if event.key == pygame.K_8: mode = 'eraser'

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1. Check Color Selection (Top UI bar)
                if mouse_pos[1] < 50:
                    for i, (name, col) in enumerate(colors.items()):
                        rect = pygame.Rect(10 + i * 40, 10, 30, 30)
                        if rect.collidepoint(mouse_pos):
                            current_color = col
                            # Usually switch back to brush when color is picked
                            if mode == 'eraser': mode = 'brush'
                else:
                    # 2. Start drawing if on canvas
                    if event.button == 1:
                        start_pos = mouse_pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    # Finalize shape on the permanent canvas
                    if mode == 'rect':
                        draw_rect(canvas, current_color, start_pos, mouse_pos)
                    elif mode == 'circle':
                        draw_circle(canvas, current_color, start_pos, mouse_pos)
                    elif mode == 'square':
                        draw_square(canvas, current_color, start_pos, mouse_pos)
                    elif mode == 'right_tri':
                        draw_right_tri(canvas, current_color, start_pos, mouse_pos)
                    elif mode == 'equi_tri':
                        draw_equi_tri(canvas, current_color, start_pos, mouse_pos)
                    elif mode == 'rhombus':
                        draw_rhombus(canvas, current_color, start_pos, mouse_pos)
                    
                    start_pos = None

        # Logic for continuous tools (Brush and Eraser)
        if pygame.mouse.get_pressed()[0] and mouse_pos[1] > 50:
            if mode == 'brush':
                pygame.draw.circle(canvas, current_color, mouse_pos, radius)
            elif mode == 'eraser':
                pygame.draw.circle(canvas, (255, 255, 255), mouse_pos, radius * 2)

        # --- DRAWING ---
        screen.blit(canvas, (0, 0))
        
        # Draw Preview (Thin lines) while dragging the mouse
        if start_pos and mouse_pos[1] > 50:
            if mode == 'rect':
                draw_rect(screen, current_color, start_pos, mouse_pos, 1)
            elif mode == 'circle':
                draw_circle(screen, current_color, start_pos, mouse_pos, 1)
            elif mode == 'square':
                draw_square(screen, current_color, start_pos, mouse_pos, 1)
            elif mode == 'right_tri':
                draw_right_tri(screen, current_color, start_pos, mouse_pos, 1)
            elif mode == 'equi_tri':
                draw_equi_tri(screen, current_color, start_pos, mouse_pos, 1)
            elif mode == 'rhombus':
                draw_rhombus(screen, current_color, start_pos, mouse_pos, 1)

        # Draw the User Interface (UI)
        draw_ui(screen, colors, current_color, mode)
        
        pygame.display.flip()
        clock.tick(120)

# --- SHAPE DRAWING FUNCTIONS ---

def draw_rect(surf, color, start, end, width=3):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w, h = abs(start[0]-end[0]), abs(start[1]-end[1])
    pygame.draw.rect(surf, color, (x, y, w, h), width)

def draw_circle(surf, color, start, end, width=3):
    rad = int(((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5)
    pygame.draw.circle(surf, color, start, rad, width)

def draw_square(surf, color, start, end, width=3):
    # For a square, we use the larger delta to determine side length
    side = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
    # Adjust position based on drag direction
    x = start[0] if end[0] > start[0] else start[0] - side
    y = start[1] if end[1] > start[1] else start[1] - side
    pygame.draw.rect(surf, color, (x, y, side, side), width)

def draw_right_tri(surf, color, start, end, width=3):
    # A right triangle uses the drag start, drag end, and a 90deg intersection
    points = [start, end, (start[0], end[1])]
    pygame.draw.polygon(surf, color, points, width)

def draw_equi_tri(surf, color, start, end, width=3):
    # Calculate side length based on distance
    side = math.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)
    height = (math.sqrt(3)/2) * side
    # Points calculated relative to start position
    p1 = start
    p2 = (start[0] + side, start[1])
    p3 = (start[0] + side/2, start[1] - height)
    pygame.draw.polygon(surf, color, [p1, p2, p3], width)

def draw_rhombus(surf, color, start, end, width=3):
    # Calculate the bounding box and find the midpoints of each side
    x1, y1 = start
    x2, y2 = end
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    # Connect top, right, bottom, and left midpoints
    points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
    pygame.draw.polygon(surf, color, points, width)

# --- UI FUNCTION ---

def draw_ui(screen, colors, current_color, mode):
    # Background panel
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, 800, 50))
    
    # Color Boxes
    for i, (name, col) in enumerate(colors.items()):
        pygame.draw.rect(screen, col, (10 + i * 40, 10, 30, 30))
        if col == current_color:
            pygame.draw.rect(screen, (255, 255, 255), (10 + i * 40, 10, 30, 30), 2)
            
    # Tool Info Text
    font = pygame.font.SysFont("Arial", 14)
    info_text = f"MODE: {mode.upper()} | 1-Brush, 2-Rect, 3-Circle, 4-Square, 5-RightTri, 6-EquiTri, 7-Rhombus, 8-Eraser"
    info = font.render(info_text, True, (0, 0, 0))
    screen.blit(info, (300, 18))

if __name__ == "__main__":
    main()