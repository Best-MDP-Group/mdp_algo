import pygame
import grid 
import constants
import obstacle
import math

pygame.init()
running = True
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Simulation")

# Create a Grid object
obstacles = [obstacle.Obstacle(screen,0,1, math.pi/2), obstacle.Obstacle(screen,5,5, 0),obstacle.Obstacle(screen,9,9, -math.pi/2),obstacle.Obstacle(screen,12,12, math.pi),obstacle.Obstacle(screen,3,17, -math.pi/2) ]

grid = grid.Grid(screen,obstacles)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((224, 235, 235))
    
    grid.draw_grid()
    

    pygame.display.update()
