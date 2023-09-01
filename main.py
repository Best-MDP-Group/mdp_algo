import pygame
import grid 
import constants
import obstacle
import math
from path_finding import hamiltonian
from robot import robot
from robot.position import Position, RobotPosition
from robot.direction import Direction

pygame.init()
running = True
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Simulation")

# Create a Grid object
obstacles = [obstacle.Obstacle(screen,Position(50,50, Direction.TOP),1), 
obstacle.Obstacle(screen,Position(90,90, Direction.BOTTOM),2),
obstacle.Obstacle(screen,Position(40,180, Direction.BOTTOM),3),
obstacle.Obstacle(screen,Position(120,150, Direction.RIGHT),4),
obstacle.Obstacle(screen,Position(150,40, Direction.LEFT),5), 
obstacle.Obstacle(screen,Position(190,190, Direction.LEFT),6) ]

grid = grid.Grid(screen,obstacles)
robot = robot.Robot(grid)
hamiltonian = hamiltonian.Hamiltonian(robot,grid)
hamiltonian.compute_path()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((224, 235, 235))
    
    grid.draw_grid()

    pygame.display.update()
