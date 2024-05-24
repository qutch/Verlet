import pygame
from pygame import gfxdraw
import random as r

pygame.init()


screen_height = 720
screen_width = 1280
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((33, 33, 33))
clock = pygame.time.Clock()

running = True

while running:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(0, 50):
                pygame.draw.circle(screen, "white", (r.randint(0, 1280), r.randint(0, 720)), 10)
    
    
    pygame.display.update()
    clock.tick(60)