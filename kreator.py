import pygame
import tkinter as tk
from tkinter import filedialog
import os
import sys

GRID_SIZE = 16
CELL_SIZE = 30
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
COLOR_PALETTE = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 0, 0), (255, 255, 255)]

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 60))
pygame.display.set_caption("Kreator Pikselowego Awatara")
sound_click = pygame.mixer.Sound("C:/Users/48660/Desktop/Click.mp3")
font = pygame.font.SysFont(None, 24)

grid = [[(255, 255, 255) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_color = COLOR_PALETTE[0]

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, grid[y][x], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (200, 200, 200), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_palette():
    for i, color in enumerate(COLOR_PALETTE):
        pygame.draw.rect(screen, color, (i * 40, SCREEN_SIZE + 10, 30, 30))
        pygame.draw.rect(screen, (0, 0, 0), (i * 40, SCREEN_SIZE + 10, 30, 30), 2)

def get_cell(pos):
    x, y = pos
    if y < SCREEN_SIZE:
        return x // CELL_SIZE, y // CELL_SIZE
    return None

def save_avatar():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if not file_path:
        return

    avatar_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = grid[y][x]
            if color != (255, 255, 255):  
                avatar_surface.set_at((x, y), (*color, 255))  
            else:
                avatar_surface.set_at((x, y), (0, 0, 0, 0))  

def count_colored():
    return sum(1 for row in grid for color in row if color != (255, 255, 255))

running = True
while running:
    screen.fill((220, 220, 220))
    draw_grid()
    draw_palette()

    info_text = font.render(f"Kolor: {current_color} | Pokolorowane: {count_colored()}", True, (0, 0, 0))
    screen.blit(info_text, (10, SCREEN_SIZE + 45))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            cell = get_cell(pos)
            if cell:
                x, y = cell
                if event.button == 1:
                    grid[y][x] = current_color
                    sound_click.play()
                elif event.button == 3:
                    grid[y][x] = (255, 255, 255)
                    sound_click.play()
            else:
                for i, color in enumerate(COLOR_PALETTE):
                    if i * 40 <= pos[0] <= i * 40 + 30 and SCREEN_SIZE + 10 <= pos[1] <= SCREEN_SIZE + 40:
                        current_color = color
                        break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_avatar()

    pygame.display.flip()

pygame.quit()
