import pygame
import constants    

class Grid:
    def __init__(self, screen, obstacles):
        self.screen = screen
        self.obstacles = obstacles
        

    def draw_grid(self):
        grid_start_x, grid_start_y = constants.TOP_BOTTOM_MARGIN, constants.TOP_BOTTOM_MARGIN
        grid_end_x, grid_end_y = grid_start_x + constants.GRID_PIXEL_SIZE, grid_start_y + constants.GRID_PIXEL_SIZE
        for i in range(constants.GRID_SIZE + 1):
            start_x = grid_start_x + i * constants.CELL_SIZE
            start_y = grid_start_y + i * constants.CELL_SIZE
            color = (0, 0, 0)
            if i == 0 or i == constants.GRID_SIZE:
                color = (255, 0, 0)
            pygame.draw.line(self.screen, color, (start_x, grid_start_y), (start_x, grid_end_y))
            pygame.draw.line(self.screen, color, (grid_start_x, start_y), (grid_end_x, start_y))
        for obstacle in self.obstacles:
            obstacle.draw_obstacle()