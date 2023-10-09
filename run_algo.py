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


def chain_commands(commands):
    chained = []
    i = 0

    while i < len(commands):
        command = commands[i]

        if command.startswith('SF') or command.startswith('SB'):
            direction = 1 if command[1] == 'F' else -1
            total_value = direction * int(command[2:])
            i += 1

            while i < len(commands) and (commands[i].startswith('SF') or commands[i].startswith('SB')):
                next_direction = 1 if commands[i][1] == 'F' else -1
                total_value += next_direction * int(commands[i][2:])
                i += 1

            prefix = 'SF' if total_value > 0 else 'SB'

            # If total value is 2 digits, we add a 0 in front of it, if total value is 1 digit, we add two 0s in front of it

            if total_value < 10:
                chained_command = f"{prefix}00{abs(total_value)}"
            elif total_value < 100:
                chained_command = f"{prefix}0{abs(total_value)}"
            else:
                chained_command = f"{prefix}{abs(total_value)}"
            
            # If the total_value is 0, we skip adding it
            if total_value == 0:
                continue
            
            chained.append(chained_command)
        else:
            chained.append(command)
            i += 1

    return ','.join(chained)

def get_commands(commands):
  output = []
  
  for command in commands:
    output.append(command.rpi_message())

  return ','.join(output)

# RF090: RF090 + SB005
# RB090: RB090 + SB005

# LF090: LF090 + SB005
# LB090: LB090 + SB005

# JF000 : RF034 + LF034 + SF010
# JB000 : RB034 + LB034 + SB015

# KF000 : LF034 + RF034 + SF010
# KB000 : LB034 + RB034 + SB015

def get_atomic_commands(commands):
  output = []
  
  for command in commands:
    # if the command is of type TurnCommand, and the type_of_turn is SMALL, then we need to split it into 4 commands
    if isinstance(command, TurnCommand):
        if (command.rpi_message() == "RF090"):
            output.append("RF090")
            output.append("SB005")
        if (command.rpi_message() == "RB090"):
            output.append("RB090")
            output.append("SB005")
        if (command.rpi_message() == "LF090"):
            output.append("LF090")
            output.append("SB005")
        if (command.rpi_message() == "LB090"):
            output.append("LB090")
            output.append("SB005")     
        if (command.rpi_message() == "JF000"):
            output.append("RF034")
            output.append("LF034")
            output.append("SF010")
        if (command.rpi_message() == "KF000"):
            output.append("LF034")
            output.append("RF034")
            output.append("SF010")
        if (command.rpi_message() == "JB000"):
            output.append("RB034")
            output.append("LB034")
            output.append("SB015")
        if (command.rpi_message() == "KB000"):
            output.append("LB034")
            output.append("RB034")
            output.append("SB015")
    
    else:
      output.append(command.rpi_message())

    
  return ','.join(output)

def get_command_for_movement(command):
    if isinstance(command, StraightCommand):
        if command.dist > 0:
            return './images/Forward.png'
        elif command.dist < 0:
            return './images/Reverse.png'
    elif isinstance(command, TurnCommand):
        turn_type = command.type_of_turn
        left = command.left
        right = command.right
        reverse = command.reverse
        
        if turn_type == TurnType.SMALL:
            if left and not right and not reverse:
                return './images/JockeyForwardLeft.png'
            elif not left and right and not reverse:
                return './images/JockeyForwardRight.png'
            elif left and not right and reverse:
                return './images/JockeyReverseLeft.png'
            elif not left and right and reverse:
                return './images/JockeyReverseRight.png'
        elif turn_type == TurnType.MEDIUM:
            if left and not right and not reverse:
                return './images/ForwardLeft.png'
            elif not left and right and not reverse:
                return './images/ForwardRight.png'
            elif left and not right and reverse:
                return './images/ReverseLeft.png'
            elif not left and right and reverse:
                return './images/ReverseRight.png'
    
    # If no matching command is found, return None
    return None



def run_algo(robot,  grid, step_size = 10):
    robot.setCurrentPos(constants.ROBOT_SAFETY_DISTANCE, constants.ROBOT_SAFETY_DISTANCE, Direction.TOP)
    hamiltonian = Hamiltonian(robot,grid)
    hamiltonian.get_path()
    commands = hamiltonian.commands
    commands_for_rpi = get_commands(commands)
    commands_for_rpi_atomic = get_atomic_commands(commands)
    chained_commands = chain_commands(commands_for_rpi_atomic.split(','))
    print(commands_for_rpi,"Default Commands")
    print('-' * 40,)
    print(commands_for_rpi_atomic, "Atomic Commands")
    print('-' * 40)
    print(chained_commands, "Chained Consecutive Straights")
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
            new_x, new_y = robot.draw_robot()

            button_image_path = get_command_for_movement(command)
            button_image = pygame.image.load(button_image_path)
            button_image = pygame.transform.scale(button_image, (30, 30))
            grid.screen.blit(button_image, (new_x,new_y))

            visitedSquares += [(init.x + i*step_size, init.y + j*step_size) for i in range(3) for j in range(3)]
            pygame.display.update()
        
        elif isinstance(command, StraightCommand):
            init = robot.get_current_pos()
            forwardCount = 0
            
            button_image_path = get_command_for_movement(command)
            button_image = pygame.image.load(button_image_path)
            button_image = pygame.transform.scale(button_image, (30, 30))
            

            while forwardCount < abs(command.dist):
                clock.tick(4)
                init = robot.get_current_pos()
                if command.dist>0:
                    robot.straight(10)
                elif command.dist<0:
                    robot.straight(-10)

                forwardCount += 10
                grid.draw_grid(visitedSquares)
                new_x, new_y = robot.draw_robot()
                grid.screen.blit(button_image, (new_x, new_y))
                visitedSquares += [(init.x + i*step_size, init.y + j*step_size) for i in range(3) for j in range(3)]
                pygame.display.update()

        elif isinstance(command, ScanCommand):
            robot.draw_robot(True)
            clock.tick(2)
            pygame.display.update()




    return 