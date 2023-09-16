import time
from commands.turn_command import TurnCommand
from commands.straight_command import StraightCommand
from commands.scan_command import ScanCommand
from robot.robot import Robot
import pygame
from grid import Grid
import constants
from buttons import get_covered_slant_squares, get_covered_turn_squares
from robot.turn_type import TurnType
from path_finding.hamiltonian import Hamiltonian
from robot.direction import Direction



def run_algo(robot,  grid, step_size = 10):
    robot.setCurrentPos(constants.ROBOT_SAFETY_DISTANCE, constants.ROBOT_SAFETY_DISTANCE, Direction.TOP)
    hamiltonian = Hamiltonian(robot,grid)
    hamiltonian.get_path()
    commands = hamiltonian.commands
    clock = pygame.time.Clock()
    visitedSquares = constants.INIT_VISITED
    robot.setCurrentPos(0, 0, Direction.TOP)

    robot.draw_robot() 
    for command in commands:
        if isinstance(command, TurnCommand):
            init = robot.get_current_pos()
            clock.tick(4)
            if command.type_of_turn == TurnType.SMALL:
                visitedSquares += get_covered_slant_squares(robot.get_current_pos(), command.reverse)
            elif command.type_of_turn == TurnType.MEDIUM:
                pass
                # visitedSquares += get_covered_turn_squares(robot.get_current_pos(), command.reverse)
            robot.turn(command.type_of_turn, command.left, command.right, command.reverse)
            grid.draw_grid(visitedSquares)
            robot.draw_robot()
            visitedSquares += [(init.x + i*step_size, init.y + j*step_size) for i in range(3) for j in range(3)]
            pygame.display.update()
        
        elif isinstance(command, StraightCommand):
            forwardCount = 0
            while forwardCount < abs(command.dist):
                clock.tick(4)
                init = robot.get_current_pos()
                if command.dist>0:
                    robot.straight(10)
                elif command.dist<0:
                    robot.straight(-10)

                forwardCount += 10
                grid.draw_grid(visitedSquares)
                robot.draw_robot()
                visitedSquares += [(init.x + i*step_size, init.y + j*step_size) for i in range(3) for j in range(3)]
                pygame.display.update()

        elif isinstance(command, ScanCommand):
            robot.draw_robot(True)
            clock.tick(2)
            pygame.display.update()




    return 