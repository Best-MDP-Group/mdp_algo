import math
from typing import List, Tuple

from robot.position import RobotPosition
from robot.direction import Direction
from robot.turn_type import TurnType
from commands.command import Command
from commands.straight_command import StraightCommand
from commands.turn_command import TurnCommand

from grid import Grid

def __init__(self, grid, brain, start: RobotPosition, end: RobotPosition, yolo):
        # We use a copy of the grid rather than use a reference
        # to the exact grid.
        self.grid: Grid = grid.copy()
        self.brain = brain  # the Hamiltonian object

        self.start = start  # starting robot position (with direction)
        self.end = end  # target ending position (with direction)
        # self.yolo = yolo

def get_neighbours(self, pos: RobotPosition) -> List[Tuple[Tuple, RobotPosition, int, Command]]:
        """
        Get movement neighbours from this position.
        Note that all values in the Position object (x, y, direction) are all with respect to the grid!
        We also expect the return Positions to be with respect to the grid.
        """
        # We assume the robot will move by 10 when travelling straight, while moving a fixed x and y value when turning
        # a fix distance of 10 when travelling straight.
        neighbours = []
        # print(f"{pos.x},{pos.y}: checking neighbors")

        # Check travel straights.
        straight_dist = 10
        straight_commands = [
            StraightCommand(straight_dist),
            StraightCommand(-straight_dist)
        ]

        for command in straight_commands:
            # Check if doing this command does not bring us to any invalid position.
            after, p = self.check_valid_command(command, pos)
            if after:
                neighbours.append((after, p, straight_dist, command))

        # Check turns
        # SOME HEURISTIC VALUE (need to account for turns travelling more also!)
        # will be adjusted on type of turn. 90 degree turn is lower cost than small turn
        turn_penalty = 100
        turn_commands = [  # type of turn, Left, Right, Reverse
            TurnCommand(TurnType.SMALL, True, False,
                        False),  # L SMALL turn, forward
            TurnCommand(TurnType.MEDIUM, True, False,
                        False),  # L MEDIUM turn, forward
            # TurnCommand(TurnType.LARGE, True, False, False),  # L LARGE turn, forward
            TurnCommand(TurnType.SMALL, True, False,
                        True),  # L SMALL turn, reverse
            TurnCommand(TurnType.MEDIUM, True, False,
                        True),  # L MEDIUM turn, reverse
            # TurnCommand(TurnType.LARGE, True, False, True),  # L LARGE turn, reverse
            TurnCommand(TurnType.SMALL, False, True,
                        False),  # R SMALL turn, forward
            TurnCommand(TurnType.MEDIUM, False, True,
                        False),  # R MEDIUM turn, forward
            # TurnCommand(TurnType.LARGE, False, True, False),  # R LARGE turn, forward
            TurnCommand(TurnType.SMALL, False, True,
                        True),  # R SMALL turn, reverse
            TurnCommand(TurnType.MEDIUM, False, True,
                        True),  # R MEDIUM turn, reverse
            # TurnCommand(TurnType.LARGE, False, True, True),  # R LARGE turn, reverse
        ]

        for c in turn_commands:
            # Check if doing this command does not bring us to any invalid position.
            after, p = self.check_valid_command(c, pos)

            if after:
                # print(f"{pos.x},{pos.y}: possible turns -> {c}")
                if c.get_type_of_turn == TurnType.SMALL:
                    turn_penalty = 100 if not self.yolo else 20
                elif c.get_type_of_turn == TurnType.MEDIUM:
                    turn_penalty = 50 if not self.yolo else 0
                neighbours.append((after, p, turn_penalty, c))

        # print("neighbours are:")
        # print(neighbours)
        return neighbours

def check_valid_command(self, command: Command, p: RobotPosition):
        """
        Checks if a command will bring a point into any invalid position.

        If invalid, we return None for both the resulting grid location and the resulting position.
        """
        # Check specifically for validity of turn command. Robot should not exceed the grid or hit the obstacles
        p = p.copy()

        if isinstance(command, TurnCommand):
            p_c = p.copy()
            command.apply_on_pos(p_c)

            # make sure that the final position is a valid one
            if not (self.grid.check_valid_position(p_c, self.yolo)):
                # print("Not valid position: ", p_c.x, p_c.y, p_c.direction)
                return None, None

            # if positive means the new position is to the right, else to the left side
            diff_in_x = p_c.x - p.x
            # if positive means the new position is on top of old position, else otherwise
            diff_in_y = p_c.y - p.y

            # additional check for medium turn
            # extraCheck = 1 if diff_in_x <= 30 and diff_in_y <= 30 else 0
            extraCheck = 0
            # print(f"{p.x},{p.y} ; {command} - extraCheck: {extraCheck}")

            # displace to top right
            if diff_in_y > 0 and diff_in_x > 0:
                if p.direction == Direction.TOP or p.direction == Direction.BOTTOM:
                    for y in range(0, abs(diff_in_y // 10) + extraCheck):
                        temp = p.copy()
                        temp.y += (y + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            # print(f"{p.x},{p.y} ; {command} - Position after not valid: ",
                            #       p_c.x, p_c.y, p_c.direction)
                            return None, None
                    for x in range(0, abs(diff_in_x // 10) + extraCheck):
                        temp = p_c.copy()
                        temp.x -= (x + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                else:  # rest of the directions
                    for y in range(0, abs(diff_in_y // 10) + extraCheck):
                        temp = p_c.copy()
                        temp.y -= (y + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                    for x in range(0, abs(diff_in_x // 10) + extraCheck):
                        temp = p.copy()
                        temp.x += (x + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
            # displace to top left
            elif diff_in_x < 0 and diff_in_y > 0:
                if p.direction == Direction.TOP or p.direction == Direction.BOTTOM:
                    for y in range(0, abs(diff_in_y // 10) + extraCheck):
                        temp = p.copy()
                        temp.y += (y + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                    for x in range(0, abs(diff_in_x // 10) + extraCheck):
                        temp = p_c.copy()
                        temp.x += (x + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                else:
                    for y in range(0, abs(diff_in_y // 10) + extraCheck + 1):
                        temp = p_c.copy()
                        temp.y -= (y + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                    for x in range(0, abs(diff_in_x // 10) + extraCheck):
                        temp = p.copy()
                        temp.x -= (x + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
            # displace to bottom left
            elif diff_in_x < 0 and diff_in_y < 0:
                if p.direction == Direction.LEFT or p.direction.RIGHT:
                    for y in range(0, abs(diff_in_y // 10) + extraCheck):
                        temp = p_c.copy()
                        temp.y += (y + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                    for x in range(0, abs(diff_in_x // 10) + extraCheck):
                        temp = p.copy()
                        temp.x -= (x + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                else:
                    for y in range(0, abs(diff_in_y // 10) + extraCheck):
                        temp = p.copy()
                        temp.y -= (y + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                    for x in range(0, abs(diff_in_x // 10) + extraCheck):
                        temp = p_c.copy()
                        temp.x += (x + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
            else:  # diff_in_x > 0 , diff_in_y < 0
                if p.direction == Direction.RIGHT or p.direction == Direction.LEFT:
                    for y in range(0, abs(diff_in_y // 10) + extraCheck):
                        temp = p_c.copy()
                        temp.y += (y + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                    for x in range(0, abs(diff_in_x // 10) + extraCheck):
                        temp = p.copy()
                        temp.x += (x + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                else:
                    for y in range(0, abs(diff_in_y // 10) + extraCheck):
                        temp = p.copy()
                        temp.y -= (y + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None
                    for x in range(0, abs(diff_in_x // 10) + extraCheck):
                        temp = p_c.copy()
                        temp.x -= (x + 1) * 10
                        if not (self.grid.check_valid_position(
                                temp, self.yolo)):
                            return None, None

        command.apply_on_pos(p)

        if self.grid.check_valid_position(p) and (
                after := p.xy()+(p.get_dir(),)):
            return after, p
        return None, None

def distance_heuristic(self, curr_pos: RobotPosition):
        """
        Measure the difference in distance between the provided position and the
        end position.
        """
        dx = abs(curr_pos.x - self.end.x)
        dy = abs(curr_pos.y - self.end.y)
        return math.sqrt(dx ** 2 + dy ** 2)

def direction_heuristic(self, curr_pos: RobotPosition):
        """
        If not same direction as my target end position, incur penalty!
        """
        if self.end.direction == curr_pos.direction.value:
            return 0
        else:
            return 10