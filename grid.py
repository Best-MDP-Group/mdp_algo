import constants    
from robot.position import Position

class Grid:
    def __init__(self, obstacles):
        self.obstacles = obstacles

    def copy(self):
        """
        Return a copy of the grid.
        """

        grid_copy = Grid(self.obstacles)
        
        return grid_copy

    def is_valid(self, pos: Position, yolo=False):
        """
        Check if a current position can be here.
        """
        # Check if current position is at an obstacle.
        if any(obstacle.is_safe(pos, yolo) for obstacle in self.obstacles):
            # print("Obstacle")
            return False

        # Check if we are out of grid bounds
        if (pos.y < constants.CELL_LENGTH or pos.y >= constants.GRID_SIZE*10 - constants.CELL_LENGTH) or (pos.x < constants.CELL_LENGTH or pos.x >= constants.GRID_SIZE*10 - constants.CELL_LENGTH):

            # print(pos.y < constants.CELL_LENGTH, pos.y >= constants.GRID_SIZE*10 - constants.CELL_LENGTH)
            # print(pos.x < constants.CELL_LENGTH, pos.x >= constants.GRID_SIZE*10 - constants.CELL_LENGTH)
                        
            # print("Out of bounds " + str(pos.x) + " " + str(pos.y))
            return False
        return True