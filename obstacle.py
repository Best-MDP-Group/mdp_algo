import math
import constants
from robot.position import Position, RobotPosition
from robot.direction import Direction

class Obstacle:
    def __init__(self, position,number):
        self.position = position
        self.target = self.get_robot_position()
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


    def is_safe(self, position, yolo):
        """
        Checks whether a given position is within the safety boundary of this obstacle.
        If yes, means it can potentially hit the obstacle. We should avoid being inside the boundary
        """

        x_range, y_range = [], []

        x_range = [position.x - constants.CELL_LENGTH,
                   position.x, position.x + constants.CELL_LENGTH]
        y_range = [position.y - constants.CELL_LENGTH,
                   position.y, position.y + constants.CELL_LENGTH]

        for x in x_range:
            for y in y_range:
                # cross
                if yolo == 1 and not (position.x == x or position.y == y):
                    continue

                # 1x1
                if yolo == 2 and not (position.x == x and position.y == y):
                    continue

                diffX = abs(self.position.x - x)
                diffY = abs(self.position.y - y)

                if (diffY < constants.OBSTACLE_SAFETY_MARGIN + 1) and \
                        (diffX < constants.OBSTACLE_SAFETY_MARGIN + 1):
                    return True

        return False