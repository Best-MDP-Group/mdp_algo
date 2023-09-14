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

# Create a Grid object
obstacles = [obstacle.Obstacle(screen,Position(50,50, Direction.TOP),1), 
obstacle.Obstacle(screen,Position(90,90, Direction.BOTTOM),2),
obstacle.Obstacle(screen,Position(40,180, Direction.BOTTOM),3),
obstacle.Obstacle(screen,Position(120,150, Direction.RIGHT),4),
obstacle.Obstacle(screen,Position(150,40, Direction.LEFT),5), 
obstacle.Obstacle(screen,Position(190,190, Direction.LEFT),6) ]


# parse frm JSON
# json_str = '{"cat":"obstacles","value":{"obstacles":[{"x":7,"y":14,"id":1,"d":0},{"x":15,"y":8,"id":2,"d":6},{"x":4,"y":3,"id":3,"d":2},{"x":9,"y":7,"id":4,"d":4}],"mode":"0"}}'
# result = jsonParse.parse_json(json_str)

# obstacles = jsonParse.convert_json(screen, result)

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
        draw_button(screen, button['path'], button['x'], button['y'], button['width'], button['height'], (0, 128, 255), (0, 0, 255))
    draw_text_button(screen, constants.START_BUTTON)

    # if count == 0:
        
        # robot.draw_robot()
        # count = run_algo(robot, hamiltonian.commands, grid, count)

    grid.draw_grid(visitedSquares)
    robot.draw_robot()
    pygame.display.update()
