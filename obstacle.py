import pygame
import math
import constants
from robot.position import Position, RobotPosition
from robot.direction import Direction

class Obstacle:
    def __init__(self, screen, position,number):
        self.position = position
        self.target = self.get_robot_position()
        self.screen = screen
        self.number = number
        
    def get_robot_position(self):

        # bottom left corner edge case
        # we add 10 to prevent the robot from going too close to the boundary for image facing top and right!
        if self.position.y == 0 and self.position.x == 0:
            if self.position.direction == Direction.TOP:
                return RobotPosition(self.position.x + 10,
                                     self.position.y + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     Direction.BOTTOM)
            elif self.position.direction == Direction.BOTTOM:
                return RobotPosition(self.position.x,
                                     self.position.y - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     Direction.TOP)
            elif self.position.direction == Direction.LEFT:
                return RobotPosition(self.position.x - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     self.position.y, Direction.RIGHT)
            else:
                return RobotPosition(self.position.x + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     self.position.y + 10, Direction.LEFT)

        # top left corner edge case!
        elif self.position.y == 190 and self.position.x == 0:
            if self.position.direction == Direction.TOP:
                return RobotPosition(self.position.x,
                                     self.position.y + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     Direction.BOTTOM)
            elif self.position.direction == Direction.BOTTOM:
                return RobotPosition(self.position.x + 10,
                                     self.position.y - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     Direction.TOP)
            elif self.position.direction == Direction.LEFT:
                return RobotPosition(self.position.x - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     self.position.y, Direction.RIGHT)
            else:
                return RobotPosition(self.position.x + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     self.position.y - 10, Direction.LEFT)

        # top right edge case
        elif self.position.y == 190 and self.position.x == 190:
            if self.position.direction == Direction.TOP:
                return RobotPosition(self.position.x,
                                     self.position.y + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     Direction.BOTTOM)
            elif self.position.direction == Direction.BOTTOM:
                return RobotPosition(self.position.x - 10,
                                     self.position.y - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     Direction.TOP)
            elif self.position.direction == Direction.LEFT:
                return RobotPosition(self.position.x - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     self.position.y - 10, Direction.RIGHT)
            else:
                return RobotPosition(self.position.x + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     self.position.y, Direction.LEFT)

        # bottom right edge case!
        elif self.position.y == 0 and self.position.x == 190:
            if self.position.direction == Direction.TOP:
                return RobotPosition(self.position.x - 10,
                                     self.position.y + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     Direction.BOTTOM)
            elif self.position.direction == Direction.BOTTOM:
                return RobotPosition(self.position.x,
                                     self.position.y - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     Direction.TOP)
            elif self.position.direction == Direction.LEFT:
                return RobotPosition(self.position.x - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     self.position.y + 10, Direction.RIGHT)
            else:
                return RobotPosition(self.position.x + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     self.position.y, Direction.LEFT)
        # cases where the obstacle is placed at the bottom of the field but not at the bottom left or right edge
        elif self.position.y == 0:
            if self.position.direction == Direction.TOP:
                return RobotPosition(self.position.x,
                                     self.position.y + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     Direction.BOTTOM)
            elif self.position.direction == Direction.BOTTOM:
                return RobotPosition(self.position.x,
                                     self.position.y - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     Direction.TOP)
            elif self.position.direction == Direction.LEFT:
                return RobotPosition(self.position.x - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     self.position.y + 10, Direction.RIGHT)
            else:
                return RobotPosition(self.position.x + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     self.position.y + 10, Direction.LEFT)

        # cases where obstacle is placed at top of the field but not at the top left or right edges
        elif self.position.y == 190:
            if self.position.direction == Direction.TOP:
                return RobotPosition(self.position.x,
                                     self.position.y + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     Direction.BOTTOM)
            elif self.position.direction == Direction.BOTTOM:
                return RobotPosition(self.position.x,
                                     self.position.y - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     Direction.TOP)
            elif self.position.direction == Direction.LEFT:
                return RobotPosition(self.position.x - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     self.position.y - 10, Direction.RIGHT)
            else:
                return RobotPosition(self.position.x + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     self.position.y - 10, Direction.LEFT)

        # cases where obstacle is placed at left side of field but not at bottom or top left
        elif self.position.x == 0:
            if self.position.direction == Direction.TOP:
                return RobotPosition(self.position.x + 10,
                                     self.position.y + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     Direction.BOTTOM)
            elif self.position.direction == Direction.BOTTOM:
                return RobotPosition(self.position.x + 10,
                                     self.position.y - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     Direction.TOP)
            elif self.position.direction == Direction.LEFT:
                return RobotPosition(self.position.x - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     self.position.y+10, Direction.RIGHT)
            else:
                return RobotPosition(self.position.x + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     self.position.y, Direction.LEFT)

        # cases where obstacle is placed at right side of field but not at bottom or top right
        elif self.position.x == 190:
            if self.position.direction == Direction.TOP:
                return RobotPosition(self.position.x - 10,
                                     self.position.y + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     Direction.BOTTOM)  # weakness
            elif self.position.direction == Direction.BOTTOM:
                return RobotPosition(self.position.x - 10,
                                     self.position.y - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     Direction.TOP)  # weakness
            elif self.position.direction == Direction.LEFT:
                return RobotPosition(self.position.x - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     self.position.y, Direction.RIGHT)
            else:
                return RobotPosition(self.position.x + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     self.position.y, Direction.LEFT)
        # all other locations can be freely accessed via the 4 sides, no need to account for being close to the edges
        else:
            if self.position.direction == Direction.TOP:
                return RobotPosition(self.position.x,
                                     self.position.y + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     Direction.BOTTOM)
            elif self.position.direction == Direction.BOTTOM:
                return RobotPosition(self.position.x,
                                     self.position.y - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     Direction.TOP)
            elif self.position.direction == Direction.LEFT:
                return RobotPosition(self.position.x - constants.OBSTACLE_SAFETY_MARGIN*2 - constants.OBSTACLE_LENGTH,
                                     self.position.y, Direction.RIGHT)
            else:
                return RobotPosition(self.position.x + constants.OBSTACLE_SAFETY_MARGIN*2 + constants.OBSTACLE_LENGTH,
                                     self.position.y, Direction.LEFT)


    def draw_obstacle(self):
        # Starting X and Y positions of the grid
        grid_start_x = constants.TOP_BOTTOM_MARGIN
        grid_start_y = constants.TOP_BOTTOM_MARGIN
        
        # Calculating the position of the obstacle on the screen
        new_x = grid_start_x + (self.position.x // 10) * constants.CELL_SIZE
        new_y = grid_start_y + (constants.GRID_SIZE - (self.position.y // 10) - 1) * constants.CELL_SIZE

        pygame.draw.rect(self.screen, constants.BLUE, (new_x, new_y, constants.CELL_SIZE, constants.CELL_SIZE), 2)

        # Draw Direction 
        if self.position.get_dir() == Direction.RIGHT:  # East
            pygame.draw.line(self.screen, constants.PINK, (new_x + constants.CELL_SIZE, new_y + 1),
                            (new_x + constants.CELL_SIZE, new_y + constants.CELL_SIZE - 1), 2)
        elif self.position.get_dir() == Direction.TOP:  # North
            pygame.draw.line(self.screen, constants.PINK, (new_x + 1, new_y),
                            (new_x + constants.CELL_SIZE - 1, new_y), 2)
        elif self.position.get_dir() == Direction.LEFT:  # West
            pygame.draw.line(self.screen, constants.PINK, (new_x, new_y + 1),
                            (new_x, new_y + constants.CELL_SIZE - 1), 2)
        elif self.position.get_dir() == Direction.BOTTOM:  # South
            pygame.draw.line(self.screen, constants.PINK, (new_x + 1, new_y + constants.CELL_SIZE),
                     (new_x + constants.CELL_SIZE - 1, new_y + constants.CELL_SIZE), 2)


        # Draw Obstacle Number
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.number), True, (0,0,255))
        text_rect = text.get_rect()
        text_rect.center = (new_x + constants.CELL_SIZE // 2, new_y + constants.CELL_SIZE // 2)
        self.screen.blit(text, text_rect)