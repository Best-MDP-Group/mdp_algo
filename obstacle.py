import pygame
import math
import constants

class Obstacle:
    def __init__(self, screen, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.screen = screen

    def draw_obstacle(self):
        # Starting X and Y positions of the grid
        grid_start_x = constants.TOP_BOTTOM_MARGIN
        grid_start_y = constants.TOP_BOTTOM_MARGIN
        
        # Calculating the position of the obstacle on the screen
        new_x = grid_start_x + self.x * constants.CELL_SIZE
        new_y = grid_start_y + (constants.GRID_SIZE - self.y - 1) * constants.CELL_SIZE

        pygame.draw.rect(self.screen, constants.BLUE, (new_x, new_y, constants.CELL_SIZE, constants.CELL_SIZE), 2)

        # Draw direction 
        if math.isclose(self.direction, 0):  # East
            pygame.draw.line(self.screen, constants.PINK, (new_x + constants.CELL_SIZE, new_y + 1),
                            (new_x + constants.CELL_SIZE, new_y + constants.CELL_SIZE - 1), 2)
        elif math.isclose(self.direction, math.pi/2):  # North
            pygame.draw.line(self.screen, constants.PINK, (new_x + 1, new_y),
                            (new_x + constants.CELL_SIZE - 1, new_y), 2)
        elif math.isclose(self.direction, math.pi):  # West
            pygame.draw.line(self.screen, constants.PINK, (new_x, new_y + 1),
                            (new_x, new_y + constants.CELL_SIZE - 1), 2)
        elif math.isclose(self.direction,  -math.pi / 2):  # South
            pygame.draw.line(self.screen, constants.PINK, (new_x + 1, new_y + constants.CELL_SIZE),
                     (new_x + constants.CELL_SIZE - 1, new_y + constants.CELL_SIZE), 2)


