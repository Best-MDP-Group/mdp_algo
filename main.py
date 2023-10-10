import pygame
import grid 
import constants
import utils
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


# RPI Connection
server_ip = "192.168.31.31"
server_port = 8001  

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
print("Waiting to Connect to RPI")
client_socket.connect((server_ip, server_port))

print("Connected to RPI")

# Receiving data from RPI
data = client_socket.recv(2048)
print(f"Received: {data.decode('utf-8')}")

# Decoding data from RPI
obs = data.decode('utf-8')
print(f"Received: {data}")

# Initialising Simulator to visualise Obstacles received
pygame.init()
font = pygame.font.Font(None, 36)
running = True
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.RESIZABLE)
button_list = constants.BUTTON_LIST
pygame.display.set_caption("Simulation")

# Parsing obstacle data and initialising Obstacle objects
result = utils.parse_json(obs)
obstacles = utils.convert_json(screen, result)

# Initialising Grid and Robot instances
grid = grid.Grid(screen,obstacles)
robot = robot.Robot(screen,grid, 0, 0)

# Set Robot position according to safety margins
robot.setCurrentPos(constants.ROBOT_SAFETY_DISTANCE, constants.ROBOT_SAFETY_DISTANCE, Direction.TOP)

# Initialise Hamiltonian class and get shortest path
hamiltonian = hamiltonian.Hamiltonian(robot,grid)
hamiltonian.get_path()

# Parse commands to be sent to RPI as command strings
commands_str = utils.get_commands(hamiltonian.commands)

# Splitting of S-Turn for STM
atomic_commands_str = utils.get_atomic_commands(hamiltonian.commands)

# Chaining consecutive Straights to improve efficiency
chained_atomic_commands_str = utils.chain_commands(atomic_commands_str.split(','))

# Converting commands to JSON format for RPI
rpi_commands = {
  "target": "STM", 
  "cat": "path",
  "value": {
    "commands": chained_atomic_commands_str
  },

}

# Sending commands to RPI
rpi_commands_json = json.dumps(rpi_commands)
print(rpi_commands)
client_socket.send(rpi_commands_json.encode('utf-8'))


# Start loop for Pygame Instance
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

    grid.draw_grid(visitedSquares)
    robot.draw_robot()
    pygame.display.update()

    
