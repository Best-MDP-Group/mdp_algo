import datetime
import timer
from commands.straight_command import StraightCommand
from commands.command import Command
from robot.direction import Direction
from robot.position import RobotPosition
from path_finding.hamiltonian import Hamiltonian
from commands.turn_command import TurnCommand
import constants

class Robot:
    def __init__(self, grid, x, y):
        self.pos = RobotPosition(constants.ROBOT_SAFETY_DISTANCE, constants.ROBOT_SAFETY_DISTANCE, Direction.TOP, 90)
        self._start_copy = self.pos.copy()
        self.hamiltonian = Hamiltonian(self, grid)
        self.path_hist = []
        self.__current_command = 0
        self.printed = False
        self.x = x
        self.y = y
            
    ##------------
    def get_current_pos(self):
        return self.pos

    def __str__(self):
        return f"robot is at {self.pos}"

    def setCurrentPos(self, x, y, direction):
        self.pos.x = x
        self.pos.y = y 
        self.pos.direction = direction

    def setCurrentPosTask2(self, x, y, direction):
        self.pos.x = constants.TASK2_LENGTH - constants.GRID_CELL_LENGTH - (x * 10)
        self.pos.y = y * 10
        self.pos.direction = direction

    def start_algo_from_position(self, grid):
        self.pos = self.get_current_pos()
        self._start_copy = self.pos.copy()
        self.hamiltonian = Hamiltonian(self, grid)
        self.path_hist = []
        self.__current_command = 0
        self.printed = False

    def convert_all_commands(self):
        return [command.convert_to_message() for command in self.hamiltonian.commands]

    def turn(self, type_of_command, left, right, rev):
        TurnCommand(type_of_command, left, right, rev).move(self.pos)

    def straight(self, dist):
        StraightCommand(dist).move(self.pos)

    def update(self):
        if len(self.path_hist) == 0 or self.pos.xy_pygame() != self.path_hist[-1]:
            self.path_hist.append(self.pos.xy_pygame())

        if self.__current_command >= len(self.hamiltonian.commands):
            return

        if self.hamiltonian.commands[self.__current_command].total_ticks == 0:
            self.__current_command += 1
            if self.__current_command >= len(self.hamiltonian.commands):
                return

        command: Command = self.hamiltonian.commands[self.__current_command]
        command.process_one_tick(self)

        if command.ticks <= 0:
            print(f"Finished processing {command}, {self.pos}")
            self.__current_command += 1
            if self.__current_command == len(self.hamiltonian.commands) and not self.printed:
                total_time = sum(command.time for command in self.hamiltonian.commands)
                total_time = round(total_time)
                print(f"All commands took {datetime.timedelta(seconds=total_time)}")
                self.printed = True
                timer.Timer.end_timer()