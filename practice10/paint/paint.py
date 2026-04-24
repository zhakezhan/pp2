import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pro Paint: Shape & Color Edition")
    
    # Основной холст для рисования
    canvas = pygame.Surface((800, 600))
    canvas.fill((255, 255, 255))
    
    clock = pygame.time.Clock()
    
    # Состояние кисти
    radius = 15
    mode = 'brush' # brush, rect, circle, eraser
    current_color = (0, 0, 255) # Синий по умолчанию
    start_pos = None
    
    # Настройка цветов для палитры (Color Selection)
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "black": (0, 0, 0),
        "yellow": (255, 255, 0),
        "purple": (128, 0, 128)
    }

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                # Горячие клавиши для инструментов
                if event.key == pygame.K_1: mode = 'brush'
                if event.key == pygame.K_2: mode = 'rect'
                if event.key == pygame.K_3: mode = 'circle'
                if event.key == pygame.K_4: mode = 'eraser'

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1. Проверяем, не нажал ли пользователь на выбор цвета (Color Selection)
                if mouse_pos[1] < 50: # Если клик в верхней части экрана (палитра)
                    for i, (name, col) in enumerate(colors.items()):
                        rect = pygame.Rect(10 + i * 40, 10, 30, 30)
                        if rect.collidepoint(mouse_pos):
                            current_color = col
                            mode = 'brush' # При смене цвета переключаемся на кисть
                else:
                    # 2. Если клик на холсте — начинаем рисовать фигуру
                    if event.button == 1:
                        start_pos = mouse_pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    # Рисуем фигуру окончательно на холсте
                    if mode == 'rect':
                        draw_rect(canvas, current_color, start_pos, mouse_pos)
                    elif mode == 'circle':
                        draw_circle(canvas, current_color, start_pos, mouse_pos)
                    start_pos = None

        # Логика для кисти и ластика (непрерывно)
        if pygame.mouse.get_pressed()[0] and mouse_pos[1] > 50:
            if mode == 'brush':
                pygame.draw.circle(canvas, current_color, mouse_pos, radius)
            elif mode == 'eraser':
                pygame.draw.circle(canvas, (255, 255, 255), mouse_pos, radius * 2)

        # --- ОТРИСОВКА ---
        screen.blit(canvas, (0, 0))
        
        # Превью фигуры, пока тянем мышь
        if start_pos and mouse_pos[1] > 50:
            if mode == 'rect':
                draw_preview_rect(screen, current_color, start_pos, mouse_pos)
            elif mode == 'circle':
                draw_preview_circle(screen, current_color, start_pos, mouse_pos)

        # Отрисовка палитры (UI)
        draw_ui(screen, colors, current_color, mode)
        
        pygame.display.flip()
        clock.tick(120)

# Функции отрисовки фигур
def draw_rect(surf, color, start, end):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w, h = abs(start[0]-end[0]), abs(start[1]-end[1])
    pygame.draw.rect(surf, color, (x, y, w, h), 3)

def draw_circle(surf, color, start, end):
    rad = int(((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5)
    pygame.draw.circle(surf, color, start, rad, 3)

# Функции для превью (пунктир или тонкая линия)
def draw_preview_rect(surf, color, start, end):
    pygame.draw.rect(surf, color, (start[0], start[1], end[0]-start[0], end[1]-start[1]), 1)

def draw_preview_circle(surf, color, start, end):
    rad = int(((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5)
    pygame.draw.circle(surf, color, start, rad, 1)

# Интерфейс выбора цвета
def draw_ui(screen, colors, current_color, mode):
    # Фон панели управления
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, 800, 50))
    
    # Квадратики цветов
    for i, (name, col) in enumerate(colors.items()):
        pygame.draw.rect(screen, col, (10 + i * 40, 10, 30, 30))
        if col == current_color: # Подсветка выбранного цвета
            pygame.draw.rect(screen, (255, 255, 255), (10 + i * 40, 10, 30, 30), 2)
            
    # Текст текущего режима
    font = pygame.font.SysFont("Arial", 16)
    info = font.render(f"Mode: {mode.upper()} | 1-Brush, 2-Rect, 3-Circle, 4-Eraser", True, (0, 0, 0))
    screen.blit(info, (300, 15))

if __name__ == "__main__":
    main()