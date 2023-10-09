import pygame
import grid 
import constants
import jsonParse
import obstacle
import math
import socket
import time
from path_finding import hamiltonian
from robot import robot
from robot.position import Position, RobotPosition
from robot.direction import Direction
from buttons import draw_button, handle_button_click, visitedSquares, draw_text_button
from run_algo import run_algo
import json


# Send the Commands to RPI
# RPI Connection
# Configure the client
server_ip = "192.168.31.31"  # Replace with your PC's IP address
server_port = 8001  # Use the same port number as on your PC

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
print("Waiting to Connect to RPI")
client_socket.connect((server_ip, server_port))

print("Connected")

data = client_socket.recv(2048)

print(f"Received: {data.decode('utf-8')}")

obs = data.decode('utf-8')
print(f"Received: {data}")

pygame.init()
# Set up fonts
font = pygame.font.Font(None, 36)
running = True
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Simulation")

# # Create a Grid object
# obstacles = [obstacle.Obstacle(screen,Position(50,50, Direction.TOP),1), 
# obstacle.Obstacle(screen,Position(90,90, Direction.BOTTOM),2),
# obstacle.Obstacle(screen,Position(40,180, Direction.BOTTOM),3),
# obstacle.Obstacle(screen,Position(120,150, Direction.RIGHT),4),
# obstacle.Obstacle(screen,Position(150,40, Direction.LEFT),5), 
# obstacle.Obstacle(screen,Position(190,190, Direction.LEFT),6) ]

# test1 = '{"cat":"obstacles","value":{"obstacles":[{"x":7,"y":14,"id":1,"d":0},{"x":15,"y":8,"id":2,"d":6},{"x":4,"y":3,"id":3,"d":2},{"x":9,"y":7,"id":4,"d":4}],"mode":"0"}}'

# test2 = '''{
#   "cat": "obstacles",
#   "value": {
#     "obstacles": [
#       {"x": 1, "y": 17, "id": 1, "d": 4},
#       {"x": 6, "y": 1, "id": 2, "d": 0},
#       {"x": 14, "y": 3, "id": 3, "d": 6},
#       {"x": 10, "y": 12, "id": 4, "d": 2},
#       {"x": 17, "y": 15, "id": 5, "d": 6},
#       {"x": 4, "y": 8, "id": 6, "d": 4},
#       {"x": 19, "y": 19, "id": 7, "d": 6},
#       {"x": 12, "y": 10, "id": 8, "d": 6}
#     ],
#     "mode": "0"
#   }
# }
# '''

# test3 = '''{
#   "cat": "obstacles",
#   "value": {
#     "obstacles": [
#       {"x": 5, "y": 9, "id": 1, "d": 4},
#       {"x": 7, "y": 14, "id": 2, "d": 6},
#       {"x": 12, "y": 9, "id": 3, "d": 2},
#       {"x": 15, "y": 15, "id": 4, "d": 4},
#       {"x": 15, "y": 4, "id": 5, "d": 6}
#     ],
#     "mode": "0"
#   }
# }
# '''


result = jsonParse.parse_json(obs)
obstacles = jsonParse.convert_json(screen, result)

#buttons
button_list = constants.BUTTON_LIST


grid = grid.Grid(screen,obstacles)
robot = robot.Robot(screen,grid, 0, 0)
print()
# hamiltonian = hamiltonian.Hamiltonian(robot,grid)
robot.setCurrentPos(0, 0, Direction.TOP)


# hamiltonian.get_path()
robot.setCurrentPos(constants.ROBOT_SAFETY_DISTANCE, constants.ROBOT_SAFETY_DISTANCE, Direction.TOP)
hamiltonian = hamiltonian.Hamiltonian(robot,grid)
hamiltonian.get_path()

# RF090: RF090 + SB005
# RB090: RB090 + SB005

# LF090: LF090 + SB005
# LB090: LB090 + SB005

# JF000 : RF034 + LF034 + SF010
# JB000 : RB034 + LB034 + SB015

# KF000 : LF034 + RF034 + SF010
# KB000 : LB034 + RB034 + SB015

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

commands_str = get_commands(hamiltonian.commands)
atomic_commands_str = get_atomic_commands(hamiltonian.commands)
chained_atomic_commands_str = chain_commands(atomic_commands_str.split(','))

# "target": "AND"
rpi_commands = {
  "target": "STM", 
  "cat": "path",
  "value": {
    "commands": chained_atomic_commands_str
  },

}

rpi_commands_json = json.dumps(rpi_commands)

print(rpi_commands)

client_socket.send(rpi_commands_json.encode('utf-8'))

robot.setCurrentPos(0, 0, Direction.TOP)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                handle_button_click(event.pos, robot, button_list)
                if (constants.START_BUTTON['x'] <= mouse_x <= constants.START_BUTTON['x'] + constants.START_BUTTON['width'] and
                    constants.START_BUTTON['y'] <= mouse_y <= constants.START_BUTTON['y'] + constants.START_BUTTON['height']):
                    run_algo(robot, grid)
                

    screen.fill((224, 235, 235))
    for button in button_list:
        draw_button(screen, button['path'], button['x'], button['y'], button['width'], button['height'], (169,169,169),(128, 128, 128))
    draw_text_button(screen, constants.START_BUTTON)

    # if count == 0:
        
        # robot.draw_robot()
        # count = run_algo(robot, hamiltonian.commands, grid, count)

    grid.draw_grid(visitedSquares)
    robot.draw_robot()
    pygame.display.update()

    
