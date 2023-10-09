import pygame
import grid 
import constants
import jsonParse
import obstacle
import math
from path_finding import hamiltonian
from robot import robot
from robot.position import Position, RobotPosition
from robot.direction import Direction
from buttons import draw_button, handle_button_click, visitedSquares, draw_text_button
from run_algo import run_algo

pygame.init()
# Set up fonts
font = pygame.font.Font(None, 36)
running = True
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Simulation")

case1 = '''{
  "cat": "obstacles",
  "value": {
    "obstacles": [
      {"x": 1, "y": 6, "id": 1, "d": 4},
      {"x": 4, "y": 6, "id": 2, "d": 4},
      {"x": 19, "y": 10, "id": 3, "d": 6},
      {"x": 4, "y": 10, "id": 4, "d": 0},
      {"x": 4, "y": 19, "id": 5, "d": 2},
      {"x": 19, "y": 19, "id": 6, "d": 6},
      {"x": 14, "y": 14, "id": 7, "d": 4}
    ],
    "mode": "0"
  }
}'''

case2 = '''{
  "cat": "obstacles",
  "value": {
    "obstacles": [
      {"x": 5, "y": 5, "id": 1, "d": 4}
    ],
    "mode": "0"
  }
}'''

case3 = '''{
  "cat": "obstacles",
  "value": {
    "obstacles": [
      {"x": 1, "y": 18, "id": 1, "d": 4},
      {"x": 6, "y": 12, "id": 2, "d": 0},
      {"x": 10, "y": 7, "id": 3, "d": 2},
      {"x": 15, "y": 16, "id": 4, "d": 4},
      {"x": 19, "y": 9, "id": 5, "d": 6},
      {"x": 13, "y": 2, "id": 6, "d": 6}
    ],
    "mode": "0"
  }
}'''


result = jsonParse.parse_json(case2)

obstacles = jsonParse.convert_json(screen, result)

#buttons
button_list = constants.BUTTON_LIST


grid = grid.Grid(screen,obstacles)
robot = robot.Robot(screen,grid, 0, 0)
print()
# hamiltonian = hamiltonian.Hamiltonian(robot,grid)
# hamiltonian.get_path()
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
